# schemas/gainer_schemas.py
from pydantic import BaseModel
from typing import List, Optional


class GainerData(BaseModel):
    name: str
    symbol: str
    coinGeckoId: str
    roaAtAth: Optional[float] = None  # Allow missing values
    roa: Optional[float] = None  # Allow missing values
    mentionPrice: float
    mentionDate: str
    twitterUserName: Optional[str] = None  # Allow missing values


class TopGainersResponse(BaseModel):
    message: str
    data: List[List[GainerData]]
