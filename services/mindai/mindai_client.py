import requests
from typing import Dict, Optional, List
from config import MIND_AI_AUTH_KEY
from services.mindai.constants import MIND_AI_BASE_URL


class MindAIAPIClient:
    def __init__(self):
        self.headers = {"x-api-key": MIND_AI_AUTH_KEY}

    def get_top_gainers_token(
        self,
        period: int = 24,
        tokensAmount: int = 5,
        kolsAmount: int = 3,
        tokenCategory: str = "top100",
        sortBy: str = "RoaAtAth",
    ) -> List[Dict]:
        """
        Fetches top gainer tokens based on the specified parameters.

        Args:
            period (int): Time period in hours (1-720)
            tokensAmount (int): Number of tokens to return
            kolsAmount (int): Number of KOLs per token
            tokenCategory (str): Filter calls by token category
            sortBy (str): Sorting criteria (RoaAtAth, etc.)

        Returns:
            List[Dict]: List of top gainer tokens
        """
        endpoint = f"{MIND_AI_BASE_URL}/v1/top-gainers-token"
        params = {
            "period": period,
            "tokensAmount": tokensAmount,
            "kolsAmount": kolsAmount,
            "tokenCategory": tokenCategory,
            "sortBy": sortBy,
        }

        response = requests.get(endpoint, params=params, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_top_kols(
        self, period: int = 24, kolsAmount: int = 3, tokenCategory: str = None
    ) -> List[Dict]:
        """
        Fetches top performing KOLs based on the specified parameters.

        Args:
            period (int): Time period in hours (1-720)
            kolsAmount (int): Number of KOLs to return
            tokenCategory (str): Filter by token category (top100, top500, lowRank)

        Returns:
            List[Dict]: List of top performing KOLs
        """
        endpoint = f"{MIND_AI_BASE_URL}/v1/top-kols"
        params = {"period": period, "kolsAmount": kolsAmount}

        # Add tokenCategory if provided
        if tokenCategory:
            params["tokenCategory"] = tokenCategory

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
        sortBy: Optional[str] = "RoaAtAth",  # New optional parameter with default
    ) -> Dict:
        endpoint = f"{MIND_AI_BASE_URL}/get-best-call"
        if sortBy is None:
            sortBy = "RoaAtAth"
        params = {
            "sortBy": sortBy,
            "period": period,
            "influencerTwitterUserName": influencer_twitter_username,
            "symbol": coin_symbol,
        }
        # Filter out None and empty string values
        params = {
            key: value for key, value in params.items() if value not in (None, "")
        }

        response = requests.get(endpoint, params=params, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
