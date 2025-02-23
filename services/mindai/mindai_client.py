import requests
from typing import Dict, Optional
from config import MIND_AI_AUTH_KEY
from services.mindai.constants import MIND_AI_BASE_URL


class MindAIAPIClient:
    def __init__(self):
        self.headers = {"x-api-key": MIND_AI_AUTH_KEY}

    def get_top_performing(self, period: str) -> Dict:
        """
        Fetches top-performing influencers based on the specified period.
        """
        endpoint = f"{MIND_AI_BASE_URL}/get-top-performing"
        params = {"period": period}
        response = requests.get(endpoint, params=params, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_top_gainers(self, period: str) -> Dict:
        """
        Fetches top gainers based on the specified period.
        """
        endpoint = f"{MIND_AI_BASE_URL}/get-top-gainers"
        params = {"period": period}
        response = requests.get(endpoint, params=params, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_top_mentioned_tokens(self, period: str) -> Dict:
        """
        Fetches the most mentioned tokens based on the specified period.
        """
        endpoint = f"{MIND_AI_BASE_URL}/get-top-mentioned-tokens"
        params = {"period": period}
        response = requests.get(endpoint, params=params, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_best_call(
        self,
        period: Optional[str] = None,
        influencer_twitter_username: Optional[str] = None,
        coin_symbol: Optional[str] = None,
    ) -> Dict:
        """
        Fetches the best call based on optional filters.
        """
        endpoint = f"{MIND_AI_BASE_URL}/get-best-call"
        params = {
            "sortBy": "RoaAtAth",
            "period": period,
            "influencerTwitterUserName": influencer_twitter_username,
            "coinSymbol": coin_symbol,
        }
        params = {key: value for key, value in params.items() if value is not None}

        response = requests.get(endpoint, params=params, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
