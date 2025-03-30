from pydantic import BaseModel, Field
from typing import List, Optional


class TopKolData(BaseModel):
    kolName: str = Field(..., description="The name of the KOL (Key Opinion Leader)")
    avgRoaAtAth: float = Field(..., description="Average ROA at ATH (in %)")
    totalCalls: int = Field(..., description="Total number of calls")
    successRate: float = Field(..., description="Success rate (between 0 and 100)")
    uniqueTokens: int = Field(..., description="Number of unique tokens")


class TopKolsResponse(BaseModel):
    """
    Response model for top performing KOLs.
    """

    message: str
    data: List[TopKolData]
