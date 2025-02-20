from typing import List
from schemas import InfluencerData


def format_message(period: str, influencers: List[InfluencerData]) -> str:
    """
    Formats the response message for the bot using the requested template.
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
