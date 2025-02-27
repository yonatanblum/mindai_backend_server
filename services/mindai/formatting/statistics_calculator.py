from typing import List
from schemas.mentioned_tokens_schemas import MentionedTokenData


class StatisticsCalculator:
    """
    Calculates various statistics required for the Market Overview.
    """

    @staticmethod
    def calculate_overall_roi(tokens: List[MentionedTokenData]) -> float:
        """
        Calculates the overall ROI based on token data.
        """
        if not tokens:
            return 0.00

        roi_values = [
            float(token.monthlyChange) if token.monthlyChange else 0 for token in tokens
        ]
        return sum(roi_values) / len(roi_values) if roi_values else 0.00

    @staticmethod
    def calculate_success_rate(tokens: List[MentionedTokenData]) -> float:
        """
        Calculates the success rate based on token mentions.
        """
        if not tokens:
            return 0.00

        total_mentions = sum(token.cashTagMentions for token in tokens)
        successful_mentions = sum(
            1 for token in tokens if float(token.monthlyChange or 0) > 0
        )

        return (successful_mentions / total_mentions) * 100 if total_mentions else 0.00

    @staticmethod
    def calculate_total_calls(tokens: List[MentionedTokenData]) -> int:
        """
        Calculates the total number of calls (mentions).
        """
        return sum(token.cashTagMentions for token in tokens) if tokens else 0

    @staticmethod
    def calculate_market_sentiment(tokens: List[MentionedTokenData]) -> str:
        """
        Determines market sentiment based on ROI trends.
        """
        positive_changes = sum(
            1 for token in tokens if float(token.monthlyChange or 0) > 0
        )
        negative_changes = sum(
            1 for token in tokens if float(token.monthlyChange or 0) < 0
        )

        if positive_changes > negative_changes:
            return "🟢 Bullish"
        elif negative_changes > positive_changes:
            return "🔴 Bearish"
        else:
            return "⚪ Neutral"
