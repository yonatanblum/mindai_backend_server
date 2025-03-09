from fastapi import HTTPException
from schemas.mindai_schemas.best_call_schemas import BestCallData, BestCallResponse
from services.mindai.mindai_client import MindAIAPIClient
from services.mindai.formatting.message_formatter import MessageFormatter
from typing import List, Optional, get_args, Type
from pydantic import BaseModel


class MindAIService:
    """
    Handles API requests and response formatting for MindAI endpoints.
    """

    def __init__(self):
        self.client = MindAIAPIClient()

    def fetch_and_format(
        self,
        period: str,
        fetch_method: str,
        output_schema: Type[BaseModel],
        formatter_function,
    ):
        """
        Fetches data from the API and applies the correct formatting.
        Automatically detects `data_schema` from `output_schema`.
        Supports `List[GainerData]`, `List[List[GainerData]]`, and `Dict` responses.
        """
        try:
            fetch_func = getattr(self.client, fetch_method)
            data = fetch_func(period)

            if not data:
                raise HTTPException(
                    status_code=404, detail="No data available for this period."
                )

            # ✅ Extract `data_schema` dynamically
            data_schema = self.extract_data_schema(output_schema)
            structured_data = self.process_api_response(data, data_schema)

            # ✅ Generate formatted message
            message = formatter_function(period, structured_data)

            # ✅ Ensure the response matches `output_schema`
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
        if isinstance(data, list) and isinstance(data[0], list):
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
        sortBy: Optional[str] = None,  # New parameter
    ) -> BestCallResponse:
        try:
            data = self.client.get_best_call(
                period=period,
                influencer_twitter_username=influencer_twitter_username,
                coin_symbol=coin_symbol,
                sortBy=sortBy,  # Pass sortBy along
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
