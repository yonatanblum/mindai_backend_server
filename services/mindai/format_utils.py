from typing import List

from schemas.gainer_schemas import GainerData
from schemas.kol_schemas import InfluencerData


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


def format_top_gainers_message(period: str, gainers: List[List[GainerData]]) -> str:
    """
    Formats the response message for top gainers in a bot-friendly way.
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
