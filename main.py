from tools.stock_fetcher import get_stock_price
from tools.news_fetcher import get_news


def main():
    symbol = input("Enter stock symbol: ").upper()

    print("\nFetching data...\n")

    price = get_stock_price(symbol)
    news = get_news(symbol)

    if price:
        print(f"Stock: {symbol}")
        print(f"Price: ${price}\n")

    print("Latest News:\n")

    for i, headline in enumerate(news, 1):
        print(f"{i}. {headline}")


if __name__ == "__main__":
    main()