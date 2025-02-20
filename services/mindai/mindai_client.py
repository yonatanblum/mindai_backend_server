import requests
from typing import List, Dict
from config import MIND_AI_AUTH_KEY
from services.mindai.constants import MIND_AI_BASE_URL, ALLOWED_PERIODS


class MindAIAPIClient:
    def __init__(self):
        self.headers = {"x-api-key": MIND_AI_AUTH_KEY}

    def get_top_performing(self, period: str) -> List[Dict]:
        """
        Fetches top-performing influencers based on the specified period.
        """
        if period not in ALLOWED_PERIODS:
            raise ValueError(
                f"Invalid period. Choose from: {', '.join(ALLOWED_PERIODS)}"
            )

        endpoint = f"{MIND_AI_BASE_URL}/get-top-performing"
        params = {"period": period}
        response = requests.get(endpoint, params=params, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_top_gainers(self, period: str) -> List[List[Dict]]:
        """
        Fetches top gainers based on the specified period.
        """
        if period not in ALLOWED_PERIODS:
            raise ValueError(
                f"Invalid period. Choose from: {', '.join(ALLOWED_PERIODS)}"
            )

        endpoint = f"{MIND_AI_BASE_URL}/get-top-gainers"
        params = {"period": period}
        response = requests.get(endpoint, params=params, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_top_mentioned_tokens(self, period: str) -> List[Dict]:
        """
        Fetches the most mentioned tokens based on the specified period.
        """
        if period not in ALLOWED_PERIODS:
            raise ValueError(
                f"Invalid period. Choose from: {', '.join(ALLOWED_PERIODS)}"
            )

        endpoint = f"{MIND_AI_BASE_URL}/get-top-mentioned-tokens"
        params = {"period": period}
        response = requests.get(endpoint, params=params, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
