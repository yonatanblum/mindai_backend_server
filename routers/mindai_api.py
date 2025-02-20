from fastapi import APIRouter
from services.mindai.mindai_service import MindAIService
from services.mindai.format_utils import MessageFormatter
from schemas.kol_schemas import TopPerformingResponse, InfluencerData
from schemas.gainer_schemas import TopGainersResponse, GainerData
from schemas.mentioned_tokens_schemas import (
    TopMentionedTokensResponse,
    MentionedTokenData,
)

router = APIRouter()
mindai_service = MindAIService()


@router.get("/top-performing-kols/{period}", response_model=TopPerformingResponse)
def get_top_performing(period: str):
    """
    Fetches top-performing influencers and returns a formatted bot message.
    """
    return mindai_service.fetch_and_format(
        period,
        "get_top_performing",
        InfluencerData,
        MessageFormatter.format_top_performing_kols,
    )


@router.get("/top-gainers/{period}", response_model=TopGainersResponse)
def get_top_gainers(period: str):
    """
    Fetches top gainers and returns a formatted bot message.
    """
    return mindai_service.fetch_and_format(
        period, "get_top_gainers", GainerData, MessageFormatter.format_top_gainers
    )


@router.get("/top-mentioned-tokens/{period}", response_model=TopMentionedTokensResponse)
def get_top_mentioned_tokens(period: str):
    """
    Fetches the most mentioned tokens and returns a formatted bot message.
    """
    return mindai_service.fetch_and_format(
        period,
        "get_top_mentioned_tokens",
        MentionedTokenData,
        MessageFormatter.format_top_mentioned_tokens,
    )
