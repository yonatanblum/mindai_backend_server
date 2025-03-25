from pydantic import BaseModel, Field
from typing import List, Dict


class TokenRequest(BaseModel):
    chain: int
    amount: int
    tokenName: str
    tokenAddress: str
    tokenSymbol: str
    fdv: float = Field(..., description="Fully Diluted Valuation")


class TokenMessage(BaseModel):
    message: str
    data: Dict


class TokenMessagesResponse(BaseModel):
    messages: List[TokenMessage]
