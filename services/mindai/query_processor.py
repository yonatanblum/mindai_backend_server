from utils.logger import Logger
from utils.period_formatter import PeriodConverter
from services.mindai.mindai_service import MindAIService
from schemas.mindai_schemas.mentioned_tokens_schemas import TopMentionedTokensResponse
from schemas.mindai_schemas.top_gainers_token_schema import TopGainersTokenResponse
from schemas.mindai_schemas.top_kols_schema import TopKolsResponse
from services.mindai.formatting.message_formatter import MessageFormatter
from typing import Dict, Any, Tuple, Optional, Callable, Type
from pydantic import BaseModel

logger = Logger(__name__).get_logger()


class MindAIQueryEngine:
    """
    Handles processing of different query types by routing to appropriate handlers.
    """

    def __init__(self):
        self.service = MindAIService()
        self.logger = Logger(__name__).get_logger()

        # Register standard query handlers
        self.standard_query_mapping = {
            "top_mentions": (
                "get_top_mentioned_tokens",
                TopMentionedTokensResponse,
                MessageFormatter.format_top_mentioned_tokens,
            ),
        }

        # Register platform info responses
        self.platform_responses = {
            "launch": "We're fine-tuning everything—launch details will be shared soon. Stay sharp!",
            "update": "Features are rolling out in phases—expect updates regularly. Patience pays!",
            "features": "We track KOL mentions and calculate ROI to show their real impact on tokens.",
            "metrics": "We focus on data-backed insights to give investors clarity in a noisy market.",
            "community": "Join our community to stay updated on the latest features and insights!",
            "general": "We're here to help! Ask me about KOLs, tokens, or market trends.",
        }

    def handle_simple_response(self, query_type: str, params: dict) -> Optional[str]:
        """Handle simple query types with fixed responses."""
        if query_type == "stupid_question":
            question = params.get("question", "").lower()
            return f"🤔 {question}... Really? Ask me something smarter!"

        if query_type == "platform_info":
            response_type = params.get("type", "general")
            return self.platform_responses.get(
                response_type, self.platform_responses["general"]
            )

        return None

    def process_top_gainers(self, params: dict) -> str:
        """Process top gainers query with new parameter format."""
        # Extract period and convert to hours
        period_value = PeriodConverter.extract_period_from_params(params)
        days = PeriodConverter.convert_to_days(period_value)
        period_hours = days * 24

        # Set additional parameters with defaults
        token_category = params.get("tokenCategory", "top100")
        tokens_amount = params.get("tokensAmount", 5)
        kols_amount = params.get("kolsAmount", 3)
        sort_by = params.get("sortBy", "RoaAtAth")

        # Call the top_gainers_token method directly
        response = self.service.get_top_gainers_token(
            period=period_hours,
            tokensAmount=tokens_amount,
            kolsAmount=kols_amount,
            tokenCategory=token_category,
            sortBy=sort_by,
        )
        return response.message

    def process_top_kols(self, params: dict) -> str:
        """Process top KOLs query with new parameter format."""
        # Extract period and convert to hours
        period_value = PeriodConverter.extract_period_from_params(params)
        days = PeriodConverter.convert_to_days(period_value)
        period_hours = days * 24

        # Set additional parameters with defaults
        token_category = params.get("tokenCategory", None)
        kols_amount = params.get("kolsAmount", 3)

        # Call the get_top_kols method directly
        response = self.service.get_top_kols(
            period=period_hours, kolsAmount=kols_amount, tokenCategory=token_category
        )
        return response.message

    def process_standard_query(self, query_type: str, params: dict) -> Optional[str]:
        """Process standard queries using fetch_and_format."""
        if query_type not in self.standard_query_mapping:
            return None

        fetch_method, output_schema, formatter = self.standard_query_mapping[query_type]
        period_value = PeriodConverter.extract_period_from_params(params)

        # Create an adapter for the formatter to match the expected signature
        def adapted_formatter(data):
            return formatter(period_value, data)

        response = self.service.fetch_and_format(
            fetch_method, output_schema, adapted_formatter, {"period": period_value}
        )
        return response.message

    def process_best_call(self, params: dict) -> str:
        """Process best call query."""
        period_value = PeriodConverter.extract_period_from_params(params)
        influencer = params.get("influencerTwitterUserName", None)
        coin_symbol = params.get("coinSymbol", None)
        sort_by = params.get("sortBy", None)

        response = self.service.fetch_best_call(
            period=period_value,
            influencer_twitter_username=influencer,
            coin_symbol=coin_symbol,
            sortBy=sort_by,
        )
        return response.message

    async def process_query(self, query_type: str, params: dict) -> str:
        """
        Process queries by routing to appropriate handler methods.

        Supported query types:
        - "stupid_question" and "platform_info" return fixed responses
        - "top_gainers" is handled by specialized processing
        - "top_kols" is handled by specialized processing
        - "top_mentions" is handled via fetch_and_format
        - "best_call" is handled via fetch_best_call
        """
        try:
            # Try simple responses first
            simple_response = self.handle_simple_response(query_type, params)
            if simple_response:
                return simple_response

            # Handle top_gainers specially
            if query_type == "top_gainers":
                return self.process_top_gainers(params)

            # Handle top_kols specially
            if query_type == "top_kols":
                return self.process_top_kols(params)

            # Try standard queries
            standard_response = self.process_standard_query(query_type, params)
            if standard_response:
                return standard_response

            # Handle best_call query
            if query_type == "best_call":
                return self.process_best_call(params)

            # If query type is not recognized, raise an exception
            raise ValueError(f"Query type '{query_type}' not recognized.")

        except Exception as e:
            self.logger.error(f"Error in process_query: {e}")
            # Raise a new exception that can be caught by the caller
            raise Exception("An error occurred while processing your request.") from e

    @staticmethod
    async def legacy_process_query(query_type: str, params: dict) -> str:
        """
        Legacy method for backward compatibility.

        This static method ensures that existing code that calls process_query
        will continue to work without modification.
        """
        engine = MindAIQueryEngine()
        return await engine.process_query(query_type, params)


# Initialize a singleton instance for use in router
query_engine = MindAIQueryEngine()

# For backward compatibility
process_query = MindAIQueryEngine.legacy_process_query
