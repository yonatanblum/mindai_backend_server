from pydantic import BaseModel
from typing import List


class BestCallData(BaseModel):
    text: str
    createdAt: str
    influencerTweeterUserName: str
    symbol: str
    coinGeckoId: str
    rawDataId: str
    mentionPrice: float
    ath: float
    roa: float
    roaAtAthInPercentage: float
    currentPrice: float
    roaAtCurrentPriceInPercentage: float


class BestCallResponse(BaseModel):
    message: str
    data: List[BestCallData]  # ✅ Ensure Pydantic expects a list
