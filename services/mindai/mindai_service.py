from fastapi import HTTPException
from services.mindai.mindai_client import MindAIAPIClient
from services.mindai.format_utils import MessageFormatter
from schemas.kol_schemas import InfluencerData
from schemas.gainer_schemas import GainerData
from schemas.mentioned_tokens_schemas import MentionedTokenData
from typing import List, Type, Union


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
        schema: Type[Union[InfluencerData, GainerData, MentionedTokenData]],
        formatter_function,
    ):
        """
        Fetches data from the API and applies the correct formatting.
        """
        try:
            # Call the appropriate fetch method
            fetch_func = getattr(self.client, fetch_method)
            data = fetch_func(period)

            # Convert to structured Pydantic models
            if isinstance(data, list) and isinstance(
                data[0], list
            ):  # Nested lists (gainers)
                structured_data = [[schema(**item) for item in group] for group in data]
            else:
                structured_data = [schema(**item) for item in data]

            # Format the message using the MessageFormatter class
            message = formatter_function(period, structured_data)

            return {"message": message, "data": structured_data}

        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"External API error: {str(e)}")
