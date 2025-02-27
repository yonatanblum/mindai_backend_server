from typing import List
from schemas.mentioned_tokens_schemas import MentionedTokenData
from schemas.kol_schemas import InfluencerData
from schemas.gainer_schemas import GainerData
from schemas.best_call_schemas import BestCallData
from services.mindai.formatting.statistics_calculator import StatisticsCalculator
from services.mindai.formatting.constants import (
    MEDAL_EMOJIS,
    TOP_PERFORMING_KOLS_TITLE,
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
    def format_top_performing_kols(
        period: str, influencers: List[InfluencerData]
    ) -> str:
        """Formats the response message for top-performing KOLs."""
        if not influencers:
            return f"🏆 No top influencers found for {period}."

        message_lines = [TOP_PERFORMING_KOLS_TITLE.format(period=period.capitalize())]

        for i, influencer in enumerate(influencers[:3]):  # Limit to top 3
            medal = MEDAL_EMOJIS[i] if i < len(MEDAL_EMOJIS) else f"#{i+1}."
            influencer_lines = [
                f"{medal} {i+1}. {influencer.influencerTweeterUserName}",
                MessageFormatter._format_field(
                    "Avg ROI", influencer.avgRoaAtAth, is_percentage=True
                ),
                MessageFormatter._format_field("Total Calls", influencer.totalMentions),
                MessageFormatter._format_field(
                    "Success Rate", round(influencer.successRate, 2), is_percentage=True
                ),  # ✅ Round success rate
                MessageFormatter._format_field(
                    "Unique Tokens", influencer.uniqueTokens
                ),
            ]
            message_lines.append("\n".join(filter(None, influencer_lines)))

        return "\n".join(message_lines)

    @staticmethod
    def format_top_gainers(period: str, gainers: List[List[GainerData]]) -> str:
        """Formats the response message for top gainers."""
        if not gainers:
            return f"📈 No top gainers found for {period}."

        message_lines = [TOP_GAINERS_TITLE.format(period=period.capitalize())]

        for i, group in enumerate(gainers[:3]):  # Limit to top 3 groups
            if not group:
                continue

            first_gainer = group[0]
            gainer_lines = [
                f"🔹 {i+1}. {first_gainer.name} ({first_gainer.symbol.upper()})",
                MessageFormatter._format_field(
                    "ROI at ATH", first_gainer.roaAtAth, is_percentage=True
                ),
                MessageFormatter._format_field(
                    "Current ROI", first_gainer.roa, is_percentage=True
                ),
                MessageFormatter._format_field(
                    "Mentioned by", first_gainer.twitterUserName
                ),
            ]
            message_lines.append("\n".join(filter(None, gainer_lines)))

        return "\n".join(message_lines)

    @staticmethod
    def format_top_mentioned_tokens(
        period: str, tokens: List[MentionedTokenData]
    ) -> str:
        """Formats the response message for most mentioned tokens with market overview."""
        if not tokens:
            return f"📊 No tokens mentioned for {period}."

        overall_roi = StatisticsCalculator.calculate_overall_roi(tokens)
        success_rate = StatisticsCalculator.calculate_success_rate(tokens)
        total_calls = StatisticsCalculator.calculate_total_calls(tokens)
        unique_coins = len(tokens)
        active_kols = sum(token.influencersAmount for token in tokens)
        market_sentiment = StatisticsCalculator.calculate_market_sentiment(tokens)

        message_lines = [TOP_MENTIONED_TOKENS_TITLE.format(period=period.capitalize())]
        market_stats = [
            overall_roi,
            success_rate,
            total_calls,
            unique_coins,
            active_kols,
            market_sentiment,
            overall_roi,
        ]

        for field, value in zip(MARKET_OVERVIEW_FIELDS, market_stats):
            message_lines.append(
                MessageFormatter._format_field(
                    field, value, is_percentage="ROI" in field
                )
            )

        message_lines.append("\n🔥 Trending Coins")
        for token in tokens[:5]:  # Show top 5 trending tokens
            token_lines = [
                f"• ${token.symbol.upper()}",
                MessageFormatter._format_field(
                    "ROI", token.monthlyChange, is_percentage=True
                ),
                MessageFormatter._format_field("Mentions", token.cashTagMentions),
                MessageFormatter._format_field("KOLs", token.influencersAmount),
            ]
            message_lines.append("\n".join(filter(None, token_lines)))

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
                    "ROI", call.roaAtAthInPercentage, is_percentage=True
                ),
                MessageFormatter._format_field(
                    "By",
                    f"@{call.influencerTweeterUserName} ({X_PROFILE_URL.format(username=call.influencerTweeterUserName.strip('@'))})",
                ),
                MessageFormatter._format_field(
                    "Date", call.createdAt.split("T")[0] if call.createdAt else None
                ),
                MessageFormatter._format_field(
                    "View Call",
                    (
                        X_STATUS_URL.format(
                            username=call.influencerTweeterUserName.strip("@"),
                            status_id=call.rawDataId,
                        )
                        if call.rawDataId and call.influencerTweeterUserName
                        else None
                    ),
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
            message_lines.append("\n".join(filter(None, call_lines)))

        return "\n".join(message_lines)
