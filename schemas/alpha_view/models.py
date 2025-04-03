from pydantic import BaseModel, Field
from typing import List, Dict, Union


class TokenRequest(BaseModel):
    chain: Union[int, str] = Field(..., description="Chain ID or chain name")
    amount: int = Field(..., description="Number of smart wallets")
    tokenName: str
    tokenAddress: str
    tokenSymbol: str
    fdv: float = Field(..., description="Fully Diluted Valuation")


class TokenMessage(BaseModel):
    message: str
    data: Dict


class TokenMessagesResponse(BaseModel):
    messages: List[TokenMessage]
