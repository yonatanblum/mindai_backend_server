from typing import List
from schemas.mentioned_tokens_schemas import MentionedTokenData
from schemas.kol_schemas import InfluencerData
from schemas.gainer_schemas import GainerData
from services.mindai.statistics_calculator import StatisticsCalculator


class MessageFormatter:
    """
    Handles the formatting of response messages for various endpoints.
    """

    @staticmethod
    def format_top_performing_kols(
        period: str, influencers: List[InfluencerData]
    ) -> str:
        """
        Formats the response message for top-performing KOLs.
        """
        if not influencers:
            return f"🏆 No top influencers found for {period}."

        medal_emojis = ["🥇", "🥈", "🥉"]
        message_lines = [f"🏆 Top Performing KOLs (Past {period.capitalize()}):\n"]

        for i, influencer in enumerate(influencers[:3]):  # Limit to top 3
            medal = medal_emojis[i] if i < len(medal_emojis) else f"#{i+1}."
            message_lines.append(
                f"{medal} {i+1}. {influencer.influencerTweeterUserName}\n"
                f"   • Avg ROI: {influencer.avgRoaAtAth:.2f}%\n"
                f"   • Total Calls: {influencer.totalMentions}\n"
                f"   • Success Rate: {influencer.successRate:.1f}%\n"
            )

        return "\n".join(message_lines)

    @staticmethod
    def format_top_gainers(period: str, gainers: List[List[GainerData]]) -> str:
        """
        Formats the response message for top gainers.
        """
        if not gainers:
            return f"📈 No top gainers found for {period}."

        message_lines = [f"📈 Top Gainers (Past {period.capitalize()}):\n"]

        for i, group in enumerate(gainers[:3]):  # Limit to top 3 groups
            if not group:
                continue

            first_gainer = group[0]
            message_lines.append(
                f"🔹 {i+1}. {first_gainer.name} ({first_gainer.symbol.upper()})\n"
                f"   • ROI at ATH: {first_gainer.roaAtAth:.2f}%\n"
                f"   • Current ROI: {first_gainer.roa:.2f}%\n"
                f"   • Mentioned by: {first_gainer.twitterUserName}\n"
            )

        return "\n".join(message_lines)

    @staticmethod
    def format_top_mentioned_tokens(
        period: str, tokens: List[MentionedTokenData]
    ) -> str:
        """
        Formats the response message for most mentioned tokens with market overview.
        """
        if not tokens:
            return f"📊 No tokens mentioned for {period}."

        # Compute statistics using the new StatisticsCalculator class
        overall_roi = StatisticsCalculator.calculate_overall_roi(tokens)
        success_rate = StatisticsCalculator.calculate_success_rate(tokens)
        total_calls = StatisticsCalculator.calculate_total_calls(tokens)
        unique_coins = len(tokens)
        active_kols = sum(token.influencersAmount for token in tokens)
        market_sentiment = StatisticsCalculator.calculate_market_sentiment(tokens)

        message_lines = [
            f"📊 Market Overview (Last {period.capitalize()} Days)\n"
            f"• Overall ROI: {overall_roi:.2f}%\n"
            f"• Success Rate: {success_rate:.2f}%\n"
            f"• Total Calls: {total_calls}\n"
            f"• Unique Coins: {unique_coins}\n"
            f"• Active KOLs: {active_kols}\n"
            f"• Market Sentiment: {market_sentiment}\n"
        ]

        # ROI Change (mocked for now, replace with actual calculation)
        roi_change = overall_roi  # Assuming it's based on overall ROI change
        message_lines.append(f"\n📈 ROI Change: {roi_change:.2f}%\n")

        message_lines.append("\n🔥 Trending Coins")

        for token in tokens[:5]:  # Show top 5 trending tokens
            message_lines.append(
                f"• ${token.symbol.upper()}\n"
                f"  ROI: {token.monthlyChange}%\n"
                f"  Mentions: {token.cashTagMentions}\n"
                f"  KOLs: {token.influencersAmount}\n"
            )

        return "\n".join(message_lines)
