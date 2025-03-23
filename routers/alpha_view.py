from fastapi import APIRouter, HTTPException
from schemas.alpha_view.models import TokenRequest
from services.alpha_view.queue_service import enqueue_token_data, dequeue_token_data
from typing import List

router = APIRouter()


@router.post("/enqueue")
def enqueue_token(request: TokenRequest):
    try:
        enqueue_token_data(request)
        return {"status": "success", "message": "Data enqueued successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dequeue")
def dequeue_tokens() -> List[dict]:
    try:
        return dequeue_token_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
