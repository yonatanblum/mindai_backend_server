from typing import List

from schemas.mindai_schemas.best_call_schemas import BestCallData
from schemas.mindai_schemas.gainer_schemas import GainerData
from schemas.mindai_schemas.kol_schemas import InfluencerData
from schemas.mindai_schemas.mentioned_tokens_schemas import MentionedTokenData
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
                    "Avg ROA", influencer.avgRoaAtAth, is_percentage=True
                ),
                MessageFormatter._format_field("Total Calls", influencer.totalMentions),
                MessageFormatter._format_field(
                    "Success Rate", round(influencer.successRate, 2), is_percentage=True
                ),  # ✅ Round success rate
                MessageFormatter._format_field(
                    "Unique Tokens", influencer.uniqueTokens
                ),
                "\n",
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
                    "ROA at ATH", first_gainer.roaAtAthInPercentage, is_percentage=True
                ),
                MessageFormatter._format_field(
                    "Current ROA",
                    first_gainer.roaAtCurrentPriceInPercentage,
                    is_percentage=True,
                ),
                MessageFormatter._format_field(
                    "Mentioned by",
                    (
                        f"@{first_gainer.influencerTweeterUserName}"
                        if first_gainer.influencerTweeterUserName
                        else None
                    ),
                ),
                MessageFormatter._format_field(
                    "Mention Date",
                    (
                        first_gainer.mentionDate.split("T")[0]
                        if first_gainer.mentionDate
                        else None
                    ),
                ),
                "\n",
            ]
            message_lines.append(
                "\n".join(filter(None, gainer_lines))
            )  # Remove empty fields

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
