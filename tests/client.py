import requests

# Server configuration
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000
BASE_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"


def fetch_and_print(endpoint: str, period: str, label: str):
    """
    Generic function to send a request to the FastAPI server and print the bot message.
    """
    url = f"{BASE_URL}/{endpoint}/{period}"
    response = requests.get(url)

    if response.status_code == 200:
        json_response = response.json()
        print(f"\nBot Message ({label}):\n")
        print(json_response["message"])
    else:
        print(f"Error {response.status_code}: {response.json()}")


def get_top_performing(period: str):
    fetch_and_print("top-performing-kols", period, "Top Performing KOLs")


def get_top_gainers(period: str):
    fetch_and_print("top-gainers", period, "Top Gainers")


def get_top_mentioned_tokens(period: str):
    fetch_and_print("top-mentioned-tokens", period, "Most Mentioned Tokens")


ALLOWED_PERIODS = ["day", "week", "twoWeek", "threeWeek", "month"]
if __name__ == "__main__":
    print("Fetching all data for 'month' period...\n")

    # get_top_performing("month")
    # get_top_gainers("month")
    get_top_mentioned_tokens("month")

    # Uncomment to fetch for all periods
    # for period in ALLOWED_PERIODS:
    #     get_top_performing(period)
    #     get_top_gainers(period)
    #     get_top_mentioned_tokens(period)
