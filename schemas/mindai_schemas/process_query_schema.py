from pydantic import BaseModel


class ProcessQueryResponse(BaseModel):
    message: str


class QueryPayload(BaseModel):
    query_type: str
    params: dict
