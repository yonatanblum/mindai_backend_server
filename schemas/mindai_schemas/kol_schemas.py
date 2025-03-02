from pydantic import BaseModel, Field
from typing import List


class InfluencerData(BaseModel):
    influencerTweeterUserName: str
    avgRoaAtAth: float
    totalMentions: int
    successRate: float = Field(
        ..., ge=0, le=100
    )  # Ensure successRate is a valid percentage (0-100)
    uniqueTokens: int


class TopPerformingResponse(BaseModel):
    message: str
    data: List[InfluencerData]
