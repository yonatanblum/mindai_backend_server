from pydantic import BaseModel
from typing import List, Optional


class MentionedTokenData(BaseModel):
    name: str
    symbol: str
    coinGeckoId: str
    cashTagMentions: int
    influencersAmount: int
    influencersTweeterUsers: List[str]
    dailyChange: Optional[str]
    weeklyChange: Optional[str]
    monthlyChange: Optional[str]  # Allow None values


class TopMentionedTokensResponse(BaseModel):
    message: str
    data: List[MentionedTokenData]
