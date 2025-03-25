import json
from datetime import datetime, timezone
from typing import Dict, List
import threading


class FileQueue:
    """Handles enqueue and dequeue operations to a file-based queue."""

    def __init__(self, path: str):
        self.path = path
        self.lock = threading.Lock()

    def enqueue(self, data: Dict):
        # Use timezone-aware UTC datetime
        data_with_timestamp = {
            **data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        with self.lock, open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(data_with_timestamp) + "\n")

    def dequeue_all(self) -> List[Dict]:
        entries = []
        with self.lock:
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    entries = [json.loads(line.strip()) for line in f if line.strip()]
            except FileNotFoundError:
                pass  # No data yet

            # Clear the file
            open(self.path, "w", encoding="utf-8").close()

        return entries

    def get_entries_after_timestamp(self, timestamp: str) -> List[Dict]:
        """
        Retrieves all entries with timestamps after the specified timestamp.

        Args:
            timestamp (str): ISO format timestamp to filter entries

        Returns:
            List[Dict]: List of entries after the specified timestamp
        """
        entries = []
        try:
            with self.lock, open(self.path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        entry = json.loads(line.strip())
                        if entry.get("timestamp", "") > timestamp:
                            entries.append(entry)
        except FileNotFoundError:
            pass  # No data yet

        return entries

    def dequeue_without_removal(self) -> List[Dict]:
        """
        Retrieves all entries without clearing the file.

        Returns:
            List[Dict]: All entries in the queue
        """
        entries = []
        try:
            with self.lock, open(self.path, "r", encoding="utf-8") as f:
                entries = [json.loads(line.strip()) for line in f if line.strip()]
        except FileNotFoundError:
            pass  # No data yet

        return entries
