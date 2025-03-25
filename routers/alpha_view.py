from fastapi import APIRouter, HTTPException, Query
from schemas.alpha_view.models import TokenRequest, TokenMessage, TokenMessagesResponse
from services.alpha_view.queue_service import (
    enqueue_token_data,
    dequeue_token_data,
    get_token_data_after_timestamp,
    get_all_token_data,
    format_token_message,
)
from typing import List, Optional
from datetime import datetime, timezone, timedelta


router = APIRouter()


@router.post("/enqueue")
def enqueue_token(request: TokenRequest):
    try:
        enqueue_token_data(request)
        return {"status": "success", "message": "Data enqueued successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dequeue", response_model=TokenMessagesResponse)
def dequeue_tokens(clear_queue: bool = False) -> TokenMessagesResponse:
    """
    Retrieve token data from the queue with formatted messages.

    Args:
        clear_queue (bool): If True, clears the queue after retrieving data. Default is False.
    """
    try:
        if clear_queue:
            data = dequeue_token_data()  # Original behavior that clears the queue
        else:
            data = get_all_token_data()  # New behavior that keeps the queue intact

        # Format each token entry as a message
        token_messages = [
            TokenMessage(message=format_token_message(item), data=item) for item in data
        ]

        return TokenMessagesResponse(messages=token_messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tokens-after-timestamp", response_model=TokenMessagesResponse)
def get_tokens_after_timestamp(
    timestamp: Optional[str] = Query(
        None, description="ISO format timestamp (YYYY-MM-DDTHH:MM:SS.sssZ)"
    )
) -> TokenMessagesResponse:
    """
    Retrieve token data added after the specified timestamp with formatted messages.

    If no timestamp is provided, defaults to 1 minute ago.
    """
    try:
        # Default to 1 minute ago if no timestamp provided
        if not timestamp:
            # Get current time and subtract 1 minute
            one_minute_ago = datetime.now(timezone.utc) - timedelta(minutes=1)
            timestamp = one_minute_ago.isoformat()

        # Validate timestamp format
        try:
            datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid timestamp format. Use ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)",
            )

        data = get_token_data_after_timestamp(timestamp)

        # Format each token entry as a message
        token_messages = [
            TokenMessage(message=format_token_message(item), data=item) for item in data
        ]

        return TokenMessagesResponse(messages=token_messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
