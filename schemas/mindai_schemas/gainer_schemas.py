# schemas/gainer_schemas.py
from pydantic import BaseModel
from typing import List, Optional


class GainerData(BaseModel):
    """Schema for a single gainer entry."""

    rawDataId: str
    text: str
    influencerTweeterUserName: str
    name: str
    symbol: str
    coinGeckoId: str
    mentionPrice: float
    currentPrice: float
    roaAtCurrentPriceInPercentage: Optional[float] = None  # Ensure compatibility
    ath: Optional[float] = None
    roaAtAthInPercentage: Optional[float] = None  # New field name matches API
    mentionDate: str


class TopGainersResponse(BaseModel):
    """Schema for the entire response containing multiple gainer groups."""

    message: str
    data: List[List[GainerData]]  # Nested lists to match API response
