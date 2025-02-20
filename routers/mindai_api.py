from fastapi import APIRouter, HTTPException
from services.mindai.mindai_client import MindAIAPIClient
from services.mindai.format_utils import format_message
from schemas import TopPerformingResponse, InfluencerData
from typing import List

router = APIRouter()
client = MindAIAPIClient()


@router.get("/top-performing-kols/{period}", response_model=TopPerformingResponse)
def get_top_performing(period: str):
    """
    REST API endpoint to fetch top-performing influencers.
    Returns a formatted message for bots along with the full data.
    """
    try:
        data = client.get_top_performing(period)
        structured_data = [InfluencerData(**influencer) for influencer in data]
        message = format_message(period, structured_data)

        return TopPerformingResponse(message=message, data=structured_data)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"External API error: {str(e)}")
