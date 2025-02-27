# schemas/best_call_schemas.py
from pydantic import BaseModel
from typing import List, Optional


class BestCallData(BaseModel):
    """Schema for a single best call entry."""

    rawDataId: str
    text: str
    influencerTweeterUserName: str
    name: str
    symbol: str
    coinGeckoId: str
    mentionPrice: Optional[float] = None
    currentPrice: Optional[float] = None
    roaAtCurrentPriceInPercentage: Optional[float] = None
    ath: Optional[float] = None
    roaAtAthInPercentage: Optional[float] = None
    createdAt: Optional[str] = None  # ✅ Updated to use `mentionDate` from API


class BestCallResponse(BaseModel):
    """Schema for the response containing best calls."""

    message: str
    data: List[BestCallData]  # ✅ Ensure response matches API format
