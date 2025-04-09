from schemas.alpha_view.models import TokenRequest
from utils.file_queue import FileQueue
from typing import List, Dict

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


def get_token_data_after_timestamp(timestamp: str) -> List[dict]:
    """Retrieve all token data added after the specified timestamp."""
    return file_queue.get_entries_after_timestamp(timestamp)


def get_all_token_data() -> List[dict]:
    """Retrieve all token data without clearing the queue."""
    return file_queue.dequeue_without_removal()


def format_token_message(item: Dict) -> str:
    """
    Format token data into a message, prioritizing chainName if available.

    Args:
        item (Dict): Token data dictionary

    Returns:
        str: Formatted message string
    """
    # Use chainName if available, otherwise use chain
    chain_display = item.get("chainName") if item.get("chainName") else item["chain"]

    return (
        f"🧠 *Alpha Token Alert!*\n"
        f"• *Token:* ${item['tokenSymbol']}\n"
        f"• *Contract:* `{item['tokenAddress']}`\n"
        f"• *Smart Wallets:* {item['amount']}\n"
        f"• *Chain:* {chain_display}\n"
        f"• *FDV:* ${item['fdv']:,}"
    )
