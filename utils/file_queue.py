import json
from datetime import datetime
from typing import Dict, List
import threading


class FileQueue:
    """Handles enqueue and dequeue operations to a file-based queue."""

    def __init__(self, path: str):
        self.path = path
        self.lock = threading.Lock()

    def enqueue(self, data: Dict):
        data_with_timestamp = {**data, "timestamp": datetime.utcnow().isoformat()}
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
