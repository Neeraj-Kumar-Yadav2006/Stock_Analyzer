from backend.agents.market_agent import get_market_data
from backend.agents.news_agent import get_news
from backend.agents.sentiment_agent import get_sentiment

def generate_report(ticker):

    market_data = get_market_data(ticker)
    news_data = get_news(ticker)
    sentiment_data = get_sentiment(news_data)

    final_report = {
        "stock_metrics": market_data,
        "news": news_data,
        "sentiment": sentiment_data,
        "summary": f"{ticker} shows {sentiment_data['label']} sentiment with price {market_data['price']}."
    }

    return final_report