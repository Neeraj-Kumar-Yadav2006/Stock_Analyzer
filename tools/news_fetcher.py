import os
from dotenv import load_dotenv
from data.news_fetcher_lib.manager import NewsFetcher

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

TICKER_TO_COMPANY = {
    "TSLA": "Tesla", "AAPL": "Apple", "GOOGL": "Google",
    "MSFT": "Microsoft", "AMZN": "Amazon", "NVDA": "NVIDIA",
    "META": "Meta", "NFLX": "Netflix",
}

def get_news(company):
    # Convert ticker to company name
    query = TICKER_TO_COMPANY.get(company.upper(), company)

    fetcher = NewsFetcher(api_key=NEWS_API_KEY)

    # fetch + clean + filter relevance in one call
    articles = fetcher.fetch_and_process(query, days_back=3, page_size=10)

    # Return just headlines for your sentiment agent
    headlines = [a["headline"] for a in articles if a.get("headline")]

    return headlines[:5]


def get_news_full(company):
    """Use this if you want full article data for DB storage."""
    query = TICKER_TO_COMPANY.get(company.upper(), company)
    fetcher = NewsFetcher(api_key=NEWS_API_KEY)
    return fetcher.get_news_with_sentiment_ready(query)