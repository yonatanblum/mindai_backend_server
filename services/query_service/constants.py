import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Key for OpenAI
API_KEY = os.getenv("OPEN_AI_KEY")

# Default temperature and model for OpenAI LLM
LLM_TEMPERATURE = 0.2
LLM_MODEL_NAME = "gpt-4o"

# Cache file path
QUERY_CACHE_FILE = "query_cache.json"

# Common phrases mappings (✅ Taken from original file)
COMMON_PHRASES = {
    "hello": ("greeting", {}),
    "hi": ("greeting", {}),
    "gm": ("greeting", {}),
    "hey": ("greeting", {}),
}
