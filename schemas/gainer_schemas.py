# schemas/gainer_schemas.py
from pydantic import BaseModel
from typing import List


class GainerData(BaseModel):
    name: str
    roaAtAth: float
    roa: float
    coinGeckoId: str
    symbol: str
    mentionPrice: float
    mentionDate: str
    twitterUserName: str


class TopGainersResponse(BaseModel):
    message: str
    data: List[List[GainerData]]
