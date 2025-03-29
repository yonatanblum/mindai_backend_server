from pydantic import BaseModel, Field
from typing import List, Optional


class TopGainerToken(BaseModel):
    tokenName: str = Field(..., description="The name of the token")
    tokenSymbol: str = Field(..., description="The symbol of the token")
    tokenCategory: Optional[str] = Field(None, description="Category of the token")
    kolName: str = Field(
        ..., description="The name of the KOL who identified the token"
    )
    callPrice: float = Field(..., description="Price at the time of the call")
    callDate: str = Field(..., description="Date when the call was made")
    roa: float = Field(..., description="Return on Advice (in %)")
    roaAtAth: float = Field(..., description="Return on Advice at All-Time High (in %)")


class TopGainersTokenResponse(BaseModel):
    """
    Response model that supports nested lists of tokens.
    """

    message: str = ""
    data: List[List[TopGainerToken]]
