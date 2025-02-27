from pydantic import BaseModel
from typing import List, Optional


class BestCallData(BaseModel):
    text: str
    createdAt: Optional[str] = None  # Allow missing field
    influencerTweeterUserName: str
    symbol: str
    coinGeckoId: str
    rawDataId: str
    mentionPrice: Optional[float] = None  # Allow missing field
    ath: Optional[float] = None  # Allow missing field
    roa: Optional[float] = None  # Allow missing field
    roaAtAthInPercentage: Optional[float] = None  # Allow missing field
    currentPrice: Optional[float] = None  # Allow missing field
    roaAtCurrentPriceInPercentage: Optional[float] = None  # Allow missing field


class BestCallResponse(BaseModel):
    message: str
    data: List[BestCallData]  # ✅ Ensure Pydantic expects a list
