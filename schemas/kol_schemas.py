# schemas/kol_schemas.py
from pydantic import BaseModel
from typing import List


class InfluencerData(BaseModel):
    influencerTweeterUserName: str
    avgRoaAtAth: float
    totalMentions: int
    successRate: float
    uniqueTokens: int


class TopPerformingResponse(BaseModel):
    message: str
    data: List[InfluencerData]
