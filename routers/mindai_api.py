from fastapi import APIRouter, HTTPException
from services.mindai.mindai_client import MindAIAPIClient
from schemas import TopPerformingResponse, InfluencerData
from typing import List

router = APIRouter()
client = MindAIAPIClient()


@router.get("/top-performing/{period}", response_model=TopPerformingResponse)
def get_top_performing(period: str):
    """
    REST API endpoint to fetch top-performing influencers.
    Returns a formatted message for bots along with the full data.
    """
    try:
        data = client.get_top_performing(period)

        if not data:
            message = f"No top influencers found for {period}."
            structured_data = []
        else:
            top_influencer = data[0]  # Take the first influencer as the top one
            message = (
                f"Top influencer for {period}: {top_influencer['influencerTweeterUserName']}, "
                f"Success Rate: {top_influencer['successRate']}%, "
                f"Tokens: {top_influencer['uniqueTokens']}."
            )

            structured_data = [InfluencerData(**influencer) for influencer in data]

        return TopPerformingResponse(message=message, data=structured_data)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"External API error: {str(e)}")
