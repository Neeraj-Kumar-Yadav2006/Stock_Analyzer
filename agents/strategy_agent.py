class StrategyAgent:

    def generate_signal(self, indicators, sentiment):

        rsi = indicators["RSI"]
        sentiment_label = sentiment["sentiment"]

        if rsi < 30 and sentiment_label == "Positive":
            signal = "STRONG BUY"

        elif rsi < 30:
            signal = "BUY"

        elif rsi > 70 and sentiment_label == "Negative":
            signal = "STRONG SELL"

        elif rsi > 70:
            signal = "SELL"

        else:
            signal = "HOLD"

        return {
            "signal": signal
        }