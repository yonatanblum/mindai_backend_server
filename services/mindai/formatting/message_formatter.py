from typing import List

from schemas.mindai_schemas.best_call_schemas import BestCallData
from schemas.mindai_schemas.mentioned_tokens_schemas import MentionedTokenData
from schemas.mindai_schemas.top_gainers_token_schema import TopGainerToken
from schemas.mindai_schemas.top_kols_schema import TopKolData
from services.mindai.formatting.statistics_calculator import StatisticsCalculator
from services.mindai.formatting.constants import (
    MEDAL_EMOJIS,
    TOP_GAINERS_TITLE,
    TOP_MENTIONED_TOKENS_TITLE,
    BEST_CALLS_TITLE,
    MARKET_OVERVIEW_FIELDS,
    X_PROFILE_URL,
    X_STATUS_URL,
    COINGECKO_URL,
)


class MessageFormatter:
    """
    Handles the formatting of response messages for various endpoints.
    """

    @staticmethod
    def _format_field(label: str, value, is_percentage: bool = False) -> str:
        """Helper function to format a field only if the value exists."""
        if value is None:
            return ""
        return (
            f"   • {label}: {value:.2f}%" if is_percentage else f"   • {label}: {value}"
        )

    @staticmethod
    def format_top_gainers_token(
        period: str, gainers: List[List[TopGainerToken]]
    ) -> str:
        """
        Formats the response message for top gainer tokens with nested structure.
        Each token in the nested list represents a group of KOLs mentioning the same token.

        Args:
            period (str): The time period formatted as a readable string
            gainers (List[List[TopGainerToken]]): Nested list of tokens, where inner lists
                                               represent the same token mentioned by different KOLs

        Returns:
            str: Formatted message
        """
        if not gainers:
            return f"📈 No top gainers found for {period}."

        message_lines = [TOP_GAINERS_TITLE.format(period=period.capitalize())]

        for i, token_group in enumerate(gainers[:5]):  # Limit to top 5
            if not token_group:
                continue

            # Get the first token from the group (main representative)
            token = token_group[0]

            # Get unique KOLs who mentioned this token
            kols = set(t.kolName for t in token_group)
            kol_text = ", ".join(list(kols)[:3])  # Show up to 3 KOLs

            # Find highest and lowest call prices
            call_prices = [t.callPrice for t in token_group]
            price_range = (
                f"${min(call_prices):.4f}"
                if min(call_prices) == max(call_prices)
                else f"${min(call_prices):.4f} - ${max(call_prices):.4f}"
            )

            # Format call dates
            call_dates = sorted(t.callDate.split("T")[0] for t in token_group)
            date_text = (
                call_dates[0]
                if len(call_dates) == 1
                else f"{call_dates[0]} to {call_dates[-1]}"
            )

            token_lines = [
                f"🔹 {i+1}. {token.tokenName} ({token.tokenSymbol.upper()})",
                MessageFormatter._format_field(
                    "ROA at ATH", token.roaAtAth, is_percentage=True
                ),
                MessageFormatter._format_field(
                    "Current ROA", token.roa, is_percentage=True
                ),
                MessageFormatter._format_field("Mentions", len(token_group)),
                MessageFormatter._format_field("KOLs", kol_text),
                MessageFormatter._format_field("Call Prices", price_range),
                MessageFormatter._format_field("Dates", date_text),
                "\n",
            ]

            message_lines.append("\n".join(filter(None, token_lines)))

        return "\n".join(message_lines)

    @staticmethod
    def format_top_kols(period: str, kols: List[TopKolData]) -> str:
        """
        Formats the response message for top performing KOLs.

        Args:
            period (str): The time period formatted as a readable string
            kols (List[TopKolData]): List of top performing KOLs

        Returns:
            str: Formatted message
        """
        if not kols:
            return f"🏆 No top KOLs found for {period}."

        message_lines = [f"🏆 Top Performing KOLs (Past {period.capitalize()}):\n"]

        for i, kol in enumerate(kols[:5]):  # Limit to top 5
            medal = MEDAL_EMOJIS[i] if i < len(MEDAL_EMOJIS) else f"#{i+1}."

            kol_lines = [
                f"{medal} {i+1}. {kol.kolName}",
                MessageFormatter._format_field(
                    "Avg ROA at ATH", kol.avgRoaAtAth, is_percentage=True
                ),
                MessageFormatter._format_field("Total Calls", kol.totalCalls),
                MessageFormatter._format_field(
                    "Success Rate", kol.successRate, is_percentage=True
                ),
                MessageFormatter._format_field("Unique Tokens", kol.uniqueTokens),
                "\n",
            ]

            message_lines.append("\n".join(filter(None, kol_lines)))

        return "\n".join(message_lines)

    @staticmethod
    def format_top_mentioned_tokens(
        period: str, tokens: List[MentionedTokenData]
    ) -> str:
        """Formats the response message for most mentioned tokens with market overview."""
        if not tokens:
            return f"📊 No tokens mentioned for {period}."

        # Compute statistics using the new StatisticsCalculator class
        overall_roa = StatisticsCalculator.calculate_overall_roa(tokens)
        # success_rate = StatisticsCalculator.calculate_success_rate(tokens)
        total_calls = StatisticsCalculator.calculate_total_calls(tokens)
        active_kols = sum(token.influencersAmount for token in tokens)
        market_sentiment = StatisticsCalculator.calculate_market_sentiment(tokens)

        message_lines = [
            f"📊 Market Overview (Last {period.capitalize()})\n"
            f"• Overall ROA: {overall_roa:.2f}%\n"
            # f"• Success Rate: {success_rate:.2f}%\n"
            f"• Total Calls: {total_calls}\n"
            f"• Active KOLs: {active_kols}\n"
            f"• Market Sentiment: {market_sentiment}\n"
        ]

        # ROA Change (mocked for now, replace with actual calculation)
        roa_change = overall_roa  # Assuming it's based on overall ROA change
        message_lines.append(f"\n📈 ROA Change: {roa_change:.2f}%\n")

        message_lines.append("\n🔥 Trending Coins")

        for token in tokens[:5]:  # Show top 5 trending tokens
            token_lines = [
                f"• ${token.symbol.upper()}",
                MessageFormatter._format_field(
                    "ROA Change", token.monthlyChange, is_percentage=True
                ),
                MessageFormatter._format_field("Calls", token.cashTagMentions),
                MessageFormatter._format_field("KOLs", token.influencersAmount),
            ]
            message_lines.append(
                "\n".join(filter(None, token_lines))
            )  # Remove empty fields

        return "\n".join(message_lines)

    @staticmethod
    def format_best_call(period: str, best_calls: List[BestCallData]) -> str:
        """Formats the response message for the best-performing calls."""
        if not best_calls:
            return f"🌟 No best-performing calls found for {period}."

        message_lines = [BEST_CALLS_TITLE.format(period=period.capitalize())]

        for i, call in enumerate(best_calls[:3]):  # Limit to top 3
            medal = MEDAL_EMOJIS[i] if i < len(MEDAL_EMOJIS) else f"#{i+1}."

            call_lines = [
                f"{medal} {i+1}. {call.symbol.upper()}",
                MessageFormatter._format_field(
                    "ROA at ATH", call.roaAtAthInPercentage, is_percentage=True
                ),
                MessageFormatter._format_field(
                    "Current ROA",
                    call.roaAtCurrentPriceInPercentage,
                    is_percentage=True,
                ),
                MessageFormatter._format_field(
                    "By",
                    (
                        f"@{call.influencerTweeterUserName}"
                        if call.influencerTweeterUserName
                        else None
                    ),
                ),
                MessageFormatter._format_field(
                    "Date", call.createdAt.split("T")[0] if call.createdAt else None
                ),
                MessageFormatter._format_field(
                    "View on CoinGecko",
                    (
                        COINGECKO_URL.format(coin_id=call.coinGeckoId)
                        if call.coinGeckoId
                        else None
                    ),
                ),
            ]
            message_lines.append(
                "\n".join(filter(None, call_lines))
            )  # Remove empty fields

        return "\n".join(message_lines)
