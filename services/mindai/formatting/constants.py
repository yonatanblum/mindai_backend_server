# services/mindai/constants.py

# Emojis
MEDAL_EMOJIS = ["🥇", "🥈", "🥉"]

# Message Templates
TOP_PERFORMING_KOLS_TITLE = "🏆 Top Performing KOLs (Past {period}):\n"
TOP_GAINERS_TITLE = "📈 Top Gainers (Past {period}):\n"
TOP_MENTIONED_TOKENS_TITLE = "📊 Market Overview (Last {period} Days)"
BEST_CALLS_TITLE = "🌟 Best Performing Calls (Past {period}):\n"

# Market Overview Fields
MARKET_OVERVIEW_FIELDS = [
    "Overall ROI",
    "Success Rate",
    "Total Calls",
    "Unique Coins",
    "Active KOLs",
    "Market Sentiment",
    "ROI Change",
]

# URLs
X_PROFILE_URL = "https://x.com/{username}"
X_STATUS_URL = "https://x.com/{username}/status/{status_id}"
COINGECKO_URL = "https://www.coingecko.com/en/coins/{coin_id}"
