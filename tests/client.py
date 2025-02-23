import requests

# Server configuration
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000
BASE_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"


def fetch_and_print(endpoint: str, params: dict, label: str):
    """
    Generic function to send a request to the FastAPI server and print the bot message.
    Handles empty or invalid JSON responses.
    """
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        try:
            json_response = response.json()
            if not json_response:
                print(f"Error: Received empty response for {label}")
                return
            print(f"\nBot Message ({label}):\n")
            print(json_response.get("message", "No message field in response"))
        except requests.exceptions.JSONDecodeError:
            print(f"Error: Invalid JSON response from {url}")
            print(
                f"Raw response: {response.text[:500]}"
            )  # Show the first 500 characters of the response
    else:
        print(f"Error {response.status_code}: {response.text[:500]}")


def get_top_performing(period: str):
    fetch_and_print("top-performing-kols", {"period": period}, "Top Performing KOLs")


def get_top_gainers(period: str):
    fetch_and_print("top-gainers", {"period": period}, "Top Gainers")


def get_top_mentioned_tokens(period: str):
    fetch_and_print("top-mentioned-tokens", {"period": period}, "Most Mentioned Tokens")


def get_best_call(
    period: str = None, influencer_twitter_username: str = None, coin_symbol: str = None
):
    """
    Fetches and prints the best call from the API.
    """
    params = {
        "period": period,
        "influencerTwitterUserName": influencer_twitter_username,
        "coinSymbol": coin_symbol,
    }
    params = {key: value for key, value in params.items() if value is not None}

    fetch_and_print("best-call", params, "Best Call")


ALLOWED_PERIODS = ["day", "week", "twoWeek", "threeWeek", "month"]

if __name__ == "__main__":
    print("Fetching all data for 'month' period...\n")

    # Test each API endpoint
    # get_top_performing("month")
    # get_top_gainers("month")
    # get_top_mentioned_tokens("month")

    # # Test best-call endpoint with different filters
    # print("\nFetching best call with different filters...\n")
    get_best_call(period="month")
    # get_best_call(influencer_twitter_username="tokenmetricsinc")
    # get_best_call(coin_symbol="btc")
    # get_best_call(period="week", influencer_twitter_username="tokenmetricsinc", coin_symbol="btc")
