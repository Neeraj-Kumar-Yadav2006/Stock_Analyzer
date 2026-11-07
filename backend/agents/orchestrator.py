from tools.news_fetcher import get_news

from backend.agents.report_agent import ReportAgent
from backend.agents.analysis_agent import AnalysisAgent
from backend.agents.sentiment_agent import SentimentAgent
from backend.agents.strategy_agent import StrategyAgent
from backend.agents.llm_agent import summarize_news

from backend.utils.logger import logger

from data.stock_fetcher_lib.manager import StockFetcher
from data.database_lib.manager import DatabaseManager

from functools import lru_cache
import time
import yfinance as yf


class StockAnalysisPipeline:

    def __init__(self):
        self.analysis_agent = AnalysisAgent()
        self.sentiment_agent = SentimentAgent()
        self.report_agent = ReportAgent()
        self.strategy_agent = StrategyAgent()

        self.fetcher = StockFetcher()

        self.db = DatabaseManager()

        self.sentiment_cache = {}
        self.cache_ttl = 300  # 5 minutes

    @lru_cache(maxsize=50)
    def get_cached_quote(self, ticker):
        logger.info("Using cached stock quote")
        return self.fetcher.get_quote_summary(ticker)

    @lru_cache(maxsize=50)
    def get_cached_ma(self, ticker):
        logger.info("Using cached moving average")
        return self.fetcher.get_moving_average(ticker, days=14)

    def get_cached_sentiment(self, ticker, news):
        current_time = time.time()

        if ticker in self.sentiment_cache:
            data, timestamp = self.sentiment_cache[ticker]
            if current_time - timestamp < self.cache_ttl:
                logger.info("Using cached sentiment")
                return data

        sentiment = self.sentiment_agent.analyze(news)
        self.sentiment_cache[ticker] = (sentiment, current_time)
        return sentiment

    def get_chart_data(self, ticker):
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d")
            chart = []
            for date, row in hist.iterrows():
                close = row.get("Close")
                if close is None or str(close).lower() == "nan":
                    continue
                chart.append({
                    "day": date.strftime("%a"),
                    "price": round(float(close), 2)
                })
            return chart
        except Exception as e:
            logger.error(f"Chart data error: {e}")
            return []

    def run(self, ticker):

        logger.info(f"Starting analysis for {ticker}")

        # ── 1. Get latest stock quote ──────────────────────────
        logger.info("Fetching stock data")
        quote = self.get_cached_quote(ticker)

        from fastapi import HTTPException
        if not quote:
            logger.error(f"No stock data available for {ticker}")
            raise HTTPException(
                status_code=404,
                detail=f"No stock data available for {ticker}"
            )

        # ── 2. Get historical prices ───────────────────────────
        history = self.db.get_price_hist(ticker, limit=60)

        prices = []
        if history and len(history) >= 20:
            prices = [h["price"] for h in history if h.get("price") is not None]
            # Reverse if DB returns newest-first
            if history and history[0].get("id", 0) > history[-1].get("id", 0):
                prices = list(reversed(prices))
            logger.info(f"Using {len(prices)} historical prices from DB")

        if len(prices) < 20:
            logger.info("DB insufficient — fetching live historical prices from yfinance")
            raw = self.fetcher.get_historical_data(ticker, period="3mo")

            prices = []
            for d in (raw or []):
                val = d.get("close", d.get("Close", d.get("price")))
                if val is not None:
                    try:
                        prices.append(float(val))
                    except (TypeError, ValueError):
                        continue

            if len(prices) < 15:
                hist = yf.Ticker(ticker).history(period="3mo")
                prices = [float(x) for x in hist["Close"].dropna().tolist()]

            if len(prices) < 15:
                logger.error(f"Not enough historical data for {ticker}")
                raise HTTPException(
                    status_code=400,
                    detail=f"Not enough historical data for {ticker}"
                )

            for p in prices[-30:]:
                try:
                    self.db.insert_stock_price(symbol=ticker, price=p)
                except Exception:
                    pass

            logger.info(f"Using {len(prices)} live historical prices")

        print("DEBUG prices length:", len(prices))
        print("DEBUG last 5 prices:", prices[-5:] if prices else None)
        # ── 3. Technical analysis ──────────────────────────────
        indicators = self.analysis_agent.analyse(prices)

        if not indicators:
            return {"error": "Indicator calculation failed"}

               # Safe MA14 override — only if we get a real number
        try:
            ma_data = self.get_cached_ma(ticker)
            if ma_data:
                ma_val = ma_data.get("ma_value") or ma_data.get("ma") or ma_data.get("value")
                if ma_val is not None and str(ma_val).lower() != "nan":
                    indicators["MA14"] = float(ma_val)
        except Exception as e:
            logger.warning(f"MA override skipped: {e}")

        # Final guard: if MA14 still missing, compute from prices
        if indicators.get("MA14") is None or str(indicators.get("MA14")).lower() == "nan":
            if len(prices) >= 14:
                indicators["MA14"] = round(sum(prices[-14:]) / 14, 2)

        logger.info(f"Indicators calculated: {indicators}")

        # ── 4. News + Sentiment ────────────────────────────────
        stored_news = self.db.get_news_for_symbol(ticker, limit=10)

        if stored_news:
            logger.info("Using cached news from DB")
            news = [n["headline"] for n in stored_news]
            news_ids = [n["id"] for n in stored_news]

        else:
            logger.info("Fetching fresh news")
            news = get_news(ticker)
            news_ids = []

            for headline in news:
                news_id = self.db.insert_article(
                    symbol=ticker,
                    headline=headline
                )
                if news_id:
                    news_ids.append(news_id)

        sentiment_data = self.db.get_aggregate_sentiment(ticker)

        if sentiment_data and sentiment_data["total_articles"] > 0:
            logger.info("Using stored sentiment from DB")
            sentiment = {
                "sentiment": sentiment_data["overall_sentiment"].capitalize(),
                "score": sentiment_data["sentiment_score"],
                "articles_analyzed": sentiment_data["total_articles"]
            }

        else:
            logger.info("Calculating new sentiment")
            sentiment = self.get_cached_sentiment(ticker, news)

            for news_id in news_ids:
                self.db.insert_sentiment(
                    news_id=news_id,
                    sentiment=sentiment["sentiment"].lower(),
                    confidence=abs(sentiment["score"])
                )

        logger.info(f"Sentiment: {sentiment}")

        # ── 5. Strategy signal ─────────────────────────────────
        signal = self.strategy_agent.generate_signal(indicators, sentiment)
        logger.info(f"Signal: {signal}")

        # ── 6. LLM news summary ────────────────────────────────
        news_summary = summarize_news(
            ticker=ticker,
            headlines=news,
            price=float(quote["price"]),
            signal=signal["signal"] if isinstance(signal, dict) else signal
        )
        logger.info(f"News Summary: {news_summary}")

        # ── 7. Generate report ─────────────────────────────────
        report = self.report_agent.generate(
            ticker,
            float(quote["price"]),
            indicators,
            sentiment,
            signal,
            news_summary
        )

        # ── 8. Save report to DB ───────────────────────────────
        self.db.insert_report(
            symbol=ticker,
            price=quote["price"],
            sentiment_summary=sentiment["sentiment"],
            full_report=report,
            tags=signal["signal"]
        )

        # ── 9. Chart data ──────────────────────────────────────
        chart_data = self.get_chart_data(ticker)

        return {
            "ticker": ticker,
            "price": quote["price"],
            "indicators": indicators,
            "sentiment": sentiment,
            "signal": signal,
            "news": news,
            "report": report,
            "chart": chart_data
        }