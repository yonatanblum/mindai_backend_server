import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Key
MIND_AI_AUTH_KEY = os.getenv("MIND_AI_AUTH_KEY")

# Server Configuration
SERVER_HOST = os.getenv("SERVER_HOST", "127.0.0.1")
SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))
