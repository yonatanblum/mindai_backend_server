from pydantic import BaseModel, Field
from typing import Dict, Any


class QueryIntent(BaseModel):
    """Pydantic model for structured query output"""

    intent: str = Field(description="The classified intent of the query")
    params: Dict[str, Any] = Field(
        description="Parameters extracted from the query", default_factory=dict
    )


class QueryRequest(BaseModel):
    """Schema for user query input."""

    query: str
