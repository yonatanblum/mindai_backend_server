import logging
import os


class Logger:
    def __init__(
        self, name: str, log_file: str = "logs/app.log", level: int = logging.INFO
    ):
        # Ensure the logs directory exists
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Configure logging
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # File Handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        # Stream Handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def get_logger(self):
        return self.logger
