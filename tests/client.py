import requests

# Server configuration
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000
BASE_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"


def fetch_and_print(endpoint: str, period: str, label: str):
    """
    Generic function to send a request to the FastAPI server and print the bot message.

    :param endpoint: API endpoint (e.g., 'top-performing-kols', 'top-gainers')
    :param period: Time period ('day', 'week', etc.)
    :param label: Descriptive label for the message (e.g., 'Top Performing KOLs', 'Top Gainers')
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
    """
    Fetch and print the top-performing influencers.
    """
    fetch_and_print("top-performing-kols", period, "Top Performing KOLs")


def get_top_gainers(period: str):
    """
    Fetch and print the top gainers.
    """
    fetch_and_print("top-gainers", period, "Top Gainers")


ALLOWED_PERIODS = ["day", "week", "twoWeek", "threeWeek", "month"]
if __name__ == "__main__":
    print("Fetching top-performing influencers and top gainers for 'month' period...\n")
    get_top_performing("month")
    get_top_gainers("month")

    # Uncomment to fetch for all periods
    # for period in ALLOWED_PERIODS:
    #     get_top_performing(period)
    #     get_top_gainers(period)
