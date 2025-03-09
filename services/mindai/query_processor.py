from utils.logger import Logger
from utils.period_converter import PeriodConverter
from services.mindai.mindai_service import MindAIService
from schemas.mindai_schemas.gainer_schemas import TopGainersResponse
from schemas.mindai_schemas.mentioned_tokens_schemas import TopMentionedTokensResponse
from schemas.mindai_schemas.kol_schemas import TopPerformingResponse
from services.mindai.formatting.message_formatter import MessageFormatter

logger = Logger(__name__).get_logger()

# Instantiate the service
mindai_service = MindAIService()


async def process_query(query_type: str, params: dict) -> str:
    """
    Processes queries by reusing MindAIService methods.

    Supported query types:
    - "stupid_question" and "platform_info" return fixed responses.
    - "top_gainers", "top_mentions", "top_kols" are handled via fetch_and_format.
    - "best_calls" and "initial_call" are handled via fetch_best_call.
    """
    try:
        # Simple, direct responses
        if query_type == "stupid_question":
            question = params.get("question", "").lower()
            return f"🤔 {question}... Really? Ask me something smarter!"

        if query_type == "platform_info":
            platform_responses = {
                "launch": "We're fine-tuning everything—launch details will be shared soon. Stay sharp!",
                "update": "Features are rolling out in phases—expect updates regularly. Patience pays!",
                "features": "We track KOL mentions and calculate ROI to show their real impact on tokens.",
                "metrics": "We focus on data-backed insights to give investors clarity in a noisy market.",
                "community": "Join our community to stay updated on the latest features and insights!",
            }
            return platform_responses.get(
                params.get("type", "general"),
                "We're here to help! Ask me about KOLs, tokens, or market trends.",
            )

        # Mapping for queries that use fetch_and_format
        mapping = {
            "top_gainers": (
                "get_top_gainers",
                TopGainersResponse,
                MessageFormatter.format_top_gainers,
            ),
            "top_mentions": (
                "get_top_mentioned_tokens",
                TopMentionedTokensResponse,
                MessageFormatter.format_top_mentioned_tokens,
            ),
            "top_kols": (
                "get_top_performing",
                TopPerformingResponse,
                MessageFormatter.format_top_performing_kols,
            ),
        }
        period_value = PeriodConverter.extract_period_from_params(params)
        if query_type in mapping:
            fetch_method, output_schema, formatter = mapping[query_type]
            response = mindai_service.fetch_and_format(
                period_value, fetch_method, output_schema, formatter
            )
            return response.message

        # Queries handled via fetch_best_call
        if query_type in ["best_call"]:
            influencer = params.get("influencerTwitterUserName", None)
            coin_symbol = params.get("coinSymbol", None)
            sort_by = params.get("sortBy", None)  # New optional sortBy parameter
            response = mindai_service.fetch_best_call(
                period_value, influencer, coin_symbol, sortBy=sort_by
            )
            return response.message

        # If query type is not recognized, raise an exception.
        raise ValueError("Query type not recognized.")
    except Exception as e:
        logger.error(f"Error in process_query: {e}")
        # Raise a new exception that can be caught by the caller.
        raise Exception("An error occurred while processing your request.") from e
