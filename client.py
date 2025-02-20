import requests

# Server configuration
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000
BASE_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"


def get_top_performing(period: str):
    """
    Sends a request to the FastAPI server and prints the bot message.
    """
    url = f"{BASE_URL}/top-performing/{period}"
    response = requests.get(url)

    if response.status_code == 200:
        json_response = response.json()
        print("Bot Message:", json_response["message"])
        print("\nFull Data:")
        for influencer in json_response["data"]:
            print(influencer)
    else:
        print(f"Error {response.status_code}: {response.json()}")


if __name__ == "__main__":
    print("Fetching top-performing influencers for 'day' period...\n")
    get_top_performing("day")
