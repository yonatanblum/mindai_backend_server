from pydantic import BaseModel, Field
from typing import List, Dict, Union, Optional


class TokenRequest(BaseModel):
    chain: Union[int, str] = Field(..., description="Chain ID")
    amount: int = Field(..., description="Number of smart wallets")
    tokenName: str
    tokenAddress: str
    tokenSymbol: str
    fdv: float = Field(..., description="Fully Diluted Valuation")
    chainName: Optional[str] = Field(None, description="Optional chain name")


class TokenMessage(BaseModel):
    message: str
    data: Dict


class TokenMessagesResponse(BaseModel):
    messages: List[TokenMessage]
