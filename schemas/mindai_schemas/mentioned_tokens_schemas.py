# schemas/mentioned_tokens_schemas.py
from pydantic import BaseModel
from typing import List, Optional


class MentionedTokenData(BaseModel):
    """Schema for a single mentioned token entry."""

    name: str
    symbol: str
    coinGeckoId: str
    cashTagMentions: int
    influencersAmount: int
    influencersTweeterUsers: List[str]
    dailyChange: Optional[float] = None  # Allow None values
    weeklyChange: Optional[float] = None  # Allow None values
    monthlyChange: Optional[float] = None  # Allow None values


class TopMentionedTokensResponse(BaseModel):
    """Schema for the response containing mentioned tokens."""

    message: str
    data: List[MentionedTokenData]  # Ensure response matches API format
