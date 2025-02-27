from fastapi import APIRouter, Query
from services.mindai.formatting.format_utils import MessageFormatter
from services.mindai.mindai_service import MindAIService
from schemas.kol_schemas import TopPerformingResponse
from schemas.gainer_schemas import TopGainersResponse
from schemas.mentioned_tokens_schemas import TopMentionedTokensResponse
from schemas.best_call_schemas import BestCallResponse
from typing import Optional

router = APIRouter()
mindai_service = MindAIService()


@router.get("/top-performing-kols", response_model=TopPerformingResponse)
def get_top_performing(
    period: str = Query(..., description="Time period: day, week, etc.")
):
    """
    Fetches top-performing influencers and returns a formatted bot message.
    """
    return mindai_service.fetch_and_format(
        period,
        "get_top_performing",
        TopPerformingResponse,
        MessageFormatter.format_top_performing_kols,
    )


@router.get("/top-gainers", response_model=TopGainersResponse)
def get_top_gainers(
    period: str = Query(..., description="Time period: day, week, etc.")
):
    """
    Fetches top gainers and returns a formatted bot message.
    """
    return mindai_service.fetch_and_format(
        period,
        "get_top_gainers",
        TopGainersResponse,
        MessageFormatter.format_top_gainers,
    )


@router.get("/top-mentioned-tokens", response_model=TopMentionedTokensResponse)
def get_top_mentioned_tokens(
    period: str = Query(..., description="Time period: day, week, etc.")
):
    """
    Fetches the most mentioned tokens and returns a formatted bot message.
    """
    return mindai_service.fetch_and_format(
        period,
        "get_top_mentioned_tokens",
        TopMentionedTokensResponse,
        MessageFormatter.format_top_mentioned_tokens,
    )


@router.get("/best-call", response_model=BestCallResponse)
def get_best_call(
    period: Optional[str] = Query(None, description="Time period: day, week, etc."),
    influencer_twitter_username: Optional[str] = Query(
        None, description="Twitter username of influencer"
    ),
    coin_symbol: Optional[str] = Query(None, description="Coin symbol"),
):
    """
    Fetches the best call based on optional filters.
    """
    return mindai_service.fetch_best_call(
        period=period,
        influencer_twitter_username=influencer_twitter_username,
        coin_symbol=coin_symbol,
    )
