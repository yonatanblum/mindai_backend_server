# schemas/mindai_schemas/mentioned_tokens_schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional


class MentionedTokenData(BaseModel):
    """Schema for a single mentioned token entry."""

    tokenName: str = Field(..., description="The name of the token")
    tokenSymbol: str = Field(..., description="The symbol of the token")
    tokenCategory: Optional[str] = Field(None, description="Category of the token")
    kolNames: List[str] = Field(
        [], description="Array of KOL names who mentioned the token"
    )
    totalCalls: int = Field(..., description="Total number of mentions for this token")
    uniqueKols: int = Field(
        ..., description="Number of unique KOLs who mentioned this token"
    )
    dailyChange: Optional[float] = Field(
        None, description="Price change in the last 24 hours (in %)"
    )
    weeklyChange: Optional[float] = Field(
        None, description="Price change in the last 7 days (in %)"
    )
    monthlyChange: Optional[float] = Field(
        None, description="Price change in the last 30 days (in %)"
    )


class TopMentionedTokensResponse(BaseModel):
    """Schema for the response containing mentioned tokens."""

    message: str
    data: List[MentionedTokenData]
