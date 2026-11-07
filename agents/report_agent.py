from backend.agents.llm_agent import generate_llm_report

class ReportAgent:

    def generate(self, ticker, price, indicators, sentiment, signal, news_summary=""):
        """Generate report using LLM first, fallback to template"""

        # 🔥 STEP 1: Try LLM
        llm_result = generate_llm_report(
            ticker=ticker,
            price=price,
            change=0,  # you can improve this later
            indicators={
                "rsi": indicators.get("RSI"),
                "ma14": indicators.get("MA14"),
                "volatility": indicators.get("volatility"),
            },
            sentiment=sentiment,
            signal=signal.get("signal") if isinstance(signal, dict) else signal,
            news_summary=news_summary
        )

        if llm_result:
            return llm_result
        
        
        report = f"""
Stock Analysis Report

Ticker: {ticker}
Current Price: ${price}

Technical Indicators
RSI: {round(indicators['RSI'], 2)}
Moving Average (14): {round(indicators['MA14'], 2)}
Volatility: {round(indicators['volatility'], 4)}

Market Sentiment: {sentiment['sentiment']}

Recommendation: {signal['signal']}

Summary:
The stock shows an RSI of {round(indicators['RSI'], 2)}.
Market sentiment is {sentiment['sentiment'].lower()}.
Final recommendation is {signal['signal']}.
"""

        return report