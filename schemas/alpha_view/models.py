from pydantic import BaseModel, Field


class TokenRequest(BaseModel):
    chain: int
    amount: int
    tokenName: str
    tokenAddress: str
    tokenSymbol: str
    fdv: float = Field(..., description="Fully Diluted Valuation")
