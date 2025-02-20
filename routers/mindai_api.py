from fastapi import APIRouter, HTTPException
from services.mindai.mindai_client import MindAIAPIClient
from services.mindai.format_utils import format_message, format_top_gainers_message
from schemas import (
    TopPerformingResponse,
    TopGainersResponse,
    InfluencerData,
    GainerData,
)
from typing import List

router = APIRouter()
client = MindAIAPIClient()


@router.get("/top-performing-kols/{period}", response_model=TopPerformingResponse)
def get_top_performing(period: str):
    """
    Fetches top-performing influencers and returns a formatted bot message.
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


@router.get("/top-gainers/{period}", response_model=TopGainersResponse)
def get_top_gainers(period: str):
    """
    Fetches top gainers and returns a formatted bot message.
    """
    try:
        data = client.get_top_gainers(period)
        structured_data = [[GainerData(**gainer) for gainer in group] for group in data]
        message = format_top_gainers_message(period, structured_data)

        return TopGainersResponse(message=message, data=structured_data)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"External API error: {str(e)}")
