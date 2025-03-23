from pydantic import BaseModel, Field
from typing import List, Optional


class InfluencerData(BaseModel):
    influencerTweeterUserName: str
    avgRoaAtAth: float
    totalMentions: int
    successRate: Optional[float] = Field(
        None, ge=0, le=100
    )  # Allow None + validate range when present
    uniqueTokens: int


class TopPerformingResponse(BaseModel):
    message: str
    data: List[InfluencerData]
