import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Key
MIND_AI_BASE_URL = os.getenv("MIND_AI_BASE_URL")  # API Configuration
# MIND_AI_BASE_URL = "https://beta.mind-ai.io/api"
# MIND_AI_BASE_URL = "https://staging.mind-ai.vercel.app/api"

# Allowed periods for the API calls
ALLOWED_PERIODS = ["day", "week", "twoWeek", "threeWeek", "month"]
