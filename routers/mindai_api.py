from fastapi import APIRouter, Query, HTTPException
from schemas.mindai_schemas.best_call_schemas import BestCallResponse
from schemas.mindai_schemas.mentioned_tokens_schemas import TopMentionedTokensResponse
from schemas.mindai_schemas.top_gainers_token_schema import TopGainersTokenResponse
from services.mindai.formatting.message_formatter import MessageFormatter
from services.mindai.mindai_service import MindAIService
from schemas.mindai_schemas.kol_schemas import TopPerformingResponse
from schemas.mindai_schemas.process_query_schema import (
    ProcessQueryResponse,
    QueryPayload,
)
from services.mindai.query_processor import process_query as process_query_func
from typing import Optional, List

router = APIRouter()
mindai_service = MindAIService()


@router.get("/top-performing-kols", response_model=TopPerformingResponse)
def get_top_performing(
    period: str = Query(..., description="Time period: day, week, etc.")
):
    """
    Fetches top-performing influencers and returns a formatted bot message.
    """

    # Adapt the formatter to match the new signature
    def adapted_formatter(data):
        return MessageFormatter.format_top_performing_kols(period, data)

    return mindai_service.fetch_and_format(
        "get_top_performing",
        TopPerformingResponse,
        adapted_formatter,
        {"period": period},
    )


@router.get("/top-gainers", response_model=TopGainersTokenResponse)
def get_top_gainers(
    period: int = Query(
        24, description="Filter the time period (1-720 hours) for the data end point"
    ),
    tokenCategory: str = Query(
        "top100", description="Filter calls by the token category"
    ),
    tokensAmount: int = Query(5, description="Number of tokens to return"),
    sortBy: str = Query(
        "RoaAtAth",
        description="Sorting criteria for token calls based on ROA at current price or ROA at ATH",
    ),
    kolsAmount: int = Query(3, description="Number of KOLs to return per token"),
):
    """
    Fetches top gainer tokens based on the specified parameters.
    """
    return mindai_service.get_top_gainers_token(
        period=period,
        tokensAmount=tokensAmount,
        kolsAmount=kolsAmount,
        tokenCategory=tokenCategory,
        sortBy=sortBy,
    )


@router.get("/top-mentioned-tokens", response_model=TopMentionedTokensResponse)
def get_top_mentioned_tokens(
    period: str = Query(..., description="Time period: day, week, etc.")
):
    """
    Fetches the most mentioned tokens and returns a formatted bot message.
    """

    # Adapt the formatter to match the new signature
    def adapted_formatter(data):
        return MessageFormatter.format_top_mentioned_tokens(period, data)

    return mindai_service.fetch_and_format(
        "get_top_mentioned_tokens",
        TopMentionedTokensResponse,
        adapted_formatter,
        {"period": period},
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


@router.post("/process", response_model=ProcessQueryResponse)
async def process_query_endpoint(payload: QueryPayload):
    """
    Processes a query by calling process_query(query_type, params)
    and returns the resulting message in the 'message' field.
    """
    try:
        result = await process_query_func(payload.query_type, payload.params)
        return ProcessQueryResponse(message=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
