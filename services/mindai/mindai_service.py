from fastapi import HTTPException
from schemas.mindai_schemas.best_call_schemas import BestCallData, BestCallResponse
from schemas.mindai_schemas.mentioned_tokens_schemas import (
    MentionedTokenData,
    TopMentionedTokensResponse,
)
from schemas.mindai_schemas.top_gainers_token_schema import (
    TopGainerToken,
    TopGainersTokenResponse,
)
from schemas.mindai_schemas.top_kols_schema import TopKolData, TopKolsResponse
from services.mindai.mindai_client import MindAIAPIClient
from services.mindai.formatting.message_formatter import MessageFormatter
from typing import List, Optional, get_args, Type, Callable, Dict, Any
from pydantic import BaseModel
from utils.period_formatter import PeriodConverter


class MindAIService:
    """
    Handles API requests and response formatting for MindAI endpoints.
    """

    def __init__(self):
        self.client = MindAIAPIClient()

    def fetch_and_format(
        self,
        fetch_method: str,
        output_schema: Type[BaseModel],
        formatter_function: Callable,
        params: Dict[str, Any] = None,
    ):
        """
        Fetches data from the API and applies the correct formatting.
        Automatically detects `data_schema` from `output_schema`.
        Supports dynamic parameters via the params dictionary.

        Args:
            fetch_method (str): Name of the client method to call
            output_schema (Type[BaseModel]): Pydantic schema for the response
            formatter_function: Function to format the processed data
            params (dict, optional): Dictionary of parameters to pass to the fetch method
        """
        try:
            # Get the method from the client
            fetch_func = getattr(self.client, fetch_method)

            # Call the function with parameters if provided
            if params:
                data = fetch_func(**params)
            else:
                data = fetch_func()

            if not data:
                raise HTTPException(
                    status_code=500,
                    detail="No data available for the requested parameters.",
                )

            # Extract `data_schema` dynamically
            data_schema = self.extract_data_schema(output_schema)
            structured_data = self.process_api_response(data, data_schema)

            # Generate formatted message
            message = formatter_function(structured_data)

            # Ensure the response matches `output_schema`
            return output_schema(message=message, data=structured_data)

        except ValueError as e:
            raise HTTPException(
                status_code=400, detail=f"Data validation error: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"External API error: {str(e)}")

    def extract_data_schema(self, output_schema: Type[BaseModel]) -> Type[BaseModel]:
        """
        Extracts the `data` field type from the given output schema.
        Determines whether the schema expects a list or a single object.
        """
        data_field = output_schema.__annotations__.get("data")

        if (
            data_field
            and hasattr(data_field, "__origin__")
            and data_field.__origin__ is list
        ):
            sub_data_type = get_args(data_field)[0]

            if (
                hasattr(sub_data_type, "__origin__")
                and sub_data_type.__origin__ is list
            ):
                return get_args(sub_data_type)[
                    0
                ]  # Extract actual schema (e.g., GainerData)
            return sub_data_type  # Extract list element type (e.g., InfluencerData)

        if data_field is None:
            raise TypeError(
                f"Invalid schema: {output_schema} does not contain a `data` field."
            )

        return data_field  # Return the direct schema if it's not a list

    def process_api_response(self, data, data_schema: Type[BaseModel]):
        """
        Processes API response and converts it into structured Pydantic models.
        Supports List, List[List], and Dict responses.
        """
        # ✅ Handle nested list (List[List[GainerData]])
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
            return [[data_schema(**item) for item in group] for group in data]

        # ✅ Handle flat list (List[GainerData])
        if isinstance(data, list):
            return [data_schema(**item) for item in data]

        # ✅ Handle single dict response (Dict[GainerData])
        if isinstance(data, dict):
            return data_schema(**data)

        raise TypeError(f"Unexpected data format: {type(data)} in API response.")

    def fetch_best_call(
        self,
        period: Optional[str] = None,
        influencer_twitter_username: Optional[str] = None,
        coin_symbol: Optional[str] = None,
        sortBy: Optional[str] = None,
    ) -> BestCallResponse:
        """
        Legacy method for fetching best calls. Consider migrating to fetch_and_format.
        """
        try:
            data = self.client.get_best_call(
                period=period,
                influencer_twitter_username=influencer_twitter_username,
                coin_symbol=coin_symbol,
                sortBy=sortBy,
            )

            if not data:
                raise HTTPException(
                    status_code=404, detail="No best call data available."
                )

            if isinstance(data, dict):
                data = [data]

            structured_data: List[BestCallData] = [
                BestCallData(**item) for item in data
            ]

            message = MessageFormatter.format_best_call(
                period or "N/A", structured_data
            )

            return BestCallResponse(message=message, data=structured_data)

        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"External API error: {str(e)}")

    def get_top_gainers_token(
        self,
        period: int = 24,
        tokensAmount: int = 5,
        kolsAmount: int = 3,
        tokenCategory: str = "top100",
        sortBy: str = "RoaAtAth",
    ) -> TopGainersTokenResponse:
        """
        Fetches top gainer tokens.

        Args:
            period (int): Time period in hours (1-720)
            tokensAmount (int): Number of tokens to return
            kolsAmount (int): Number of KOLs per token
            tokenCategory (str): Filter calls by token category
            sortBy (str): Sorting criteria (RoaAtAth, etc.)

        Returns:
            TopGainersTokenResponse: Processed top gainer tokens with nested structure
        """
        try:
            # Get raw data from the API
            data = self.client.get_top_gainers_token(
                period, tokensAmount, kolsAmount, tokenCategory, sortBy
            )

            if not data:
                raise HTTPException(
                    status_code=404, detail="No top gainer tokens available."
                )

            # Check if we already have a nested list structure
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                # Convert each inner list of dictionaries to a list of TopGainerToken objects
                structured_data = [
                    [TopGainerToken(**item) for item in group] for group in data
                ]
            else:
                # Convert flat list to a list of lists (each inner list has one item)
                structured_data = [[TopGainerToken(**item)] for item in data]

            # Format the period for the message using the PeriodConverter
            formatted_period = PeriodConverter.format_period_text(period)

            # Create a formatted message using the MessageFormatter
            message = MessageFormatter.format_top_gainers_token(
                formatted_period, structured_data
            )

            # Return with formatted message
            return TopGainersTokenResponse(message=message, data=structured_data)

        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"External API error: {str(e)}")

    def get_top_kols(
        self, period: int = 24, kolsAmount: int = 3, tokenCategory: str = None
    ) -> TopKolsResponse:
        """
        Fetches top performing KOLs.

        Args:
            period (int): Time period in hours (1-720)
            kolsAmount (int): Number of KOLs to return
            tokenCategory (str): Filter by token category

        Returns:
            TopKolsResponse: Processed top performing KOLs
        """
        try:
            # Get raw data from the API
            data = self.client.get_top_kols(period, kolsAmount, tokenCategory)

            if not data:
                raise HTTPException(
                    status_code=404, detail="No top performing KOLs available."
                )

            # Convert the data to KOL models
            kol_models = [TopKolData(**item) for item in data]

            # Format the period for the message
            formatted_period = PeriodConverter.format_period_text(period)

            # Create a formatted message using the MessageFormatter
            message = MessageFormatter.format_top_kols(formatted_period, kol_models)

            # Return with formatted message
            return TopKolsResponse(message=message, data=kol_models)

        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"External API error: {str(e)}")

    def get_top_mentioned_tokens(
        self,
        period: int = 24,
        tokensAmount: int = 5,
        kols: bool = True,
        tokenCategory: Optional[str] = None,
    ) -> TopMentionedTokensResponse:
        """
        Fetches the most mentioned tokens.

        Args:
            period (int): Time period in hours (1-720)
            tokensAmount (int): Number of tokens to return
            kols (bool): Include KOL names in the response
            tokenCategory (str, optional): Filter tokens by category

        Returns:
            TopMentionedTokensResponse: Processed top mentioned tokens
        """
        try:
            # Get raw data from the API
            data = self.client.get_top_mentioned_tokens(
                period, tokensAmount, kols, tokenCategory
            )

            if not data:
                raise HTTPException(
                    status_code=404, detail="No mentioned tokens available."
                )

            # Convert the data to token models
            token_models = [MentionedTokenData(**item) for item in data]

            # Format the period for the message
            formatted_period = PeriodConverter.format_period_text(period)

            # Create a formatted message using the MessageFormatter
            message = MessageFormatter.format_top_mentioned_tokens(
                formatted_period, token_models
            )

            # Return with formatted message
            return TopMentionedTokensResponse(message=message, data=token_models)

        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"External API error: {str(e)}")
