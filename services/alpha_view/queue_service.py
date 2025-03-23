from schemas.alpha_view.models import TokenRequest
from utils.file_queue import FileQueue
from typing import List

# Use a shared queue file path
QUEUE_PATH = r"services/alpha_view/alpha_queue.jsonl"

file_queue = FileQueue(QUEUE_PATH)


def enqueue_token_data(token: TokenRequest):
    """Enqueue token data into the queue file with timestamp."""
    data = token.model_dump()  # Updated to use model_dump instead of deprecated dict()
    file_queue.enqueue(data)


def dequeue_token_data() -> List[dict]:
    """Retrieve and clear all queued token data."""
    return file_queue.dequeue_all()
