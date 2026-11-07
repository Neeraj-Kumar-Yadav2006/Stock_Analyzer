from backend.utils.logger import logger
import pandas as pd

class AnalysisAgent:

    def moving_average(self, prices, window=14):
        series = pd.Series(prices)
        result = series.rolling(window).mean().iloc[-1]
        # fallback to simple mean if not enough data
        return float(result) if not pd.isna(result) else float(series.mean())

    def volatility(self, prices):
        series = pd.Series(prices)
        result = series.pct_change().std()
        return float(result) if not pd.isna(result) else 0.0

    def rsi(self, prices, window=14):
        series = pd.Series(prices)

        # Need at least window+1 points for a valid RSI
        if len(series) < window + 1:
            print(f"[AnalysisAgent] Warning: only {len(series)} prices, need {window+1} for RSI. Using shorter window.")
            window = max(2, len(series) - 1)  # shrink window to fit available data

        delta = series.diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(window).mean()
        avg_loss = loss.rolling(window).mean()

        avg_loss = avg_loss.replace(0, 1e-10)

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        result = rsi.iloc[-1]

        # Final NaN guard — return neutral RSI of 50
        return float(result) if not pd.isna(result) else 50.0
    
    def _validate_prices(self, prices):
        """Internal helper to ensure data integrity."""
        if not isinstance(prices, list) or len(prices) < 2:
            logger.error("AUDIT | AnalysisAgent | Received insufficient data points.")
            return False
        return True

    def analyse(self, prices):
        # Validation Layer 
        if not self._validate_prices(prices):
            return {"error": "Insufficient data"}

        try:
            results = {
                "RSI": self.rsi(prices),
                "MA14": self.moving_average(prices),
                "volatility": self.volatility(prices)
            }
            
            logger.info(f"AUDIT | AnalysisAgent | Success | Output: {results}")
            return results
            
        except Exception as e:
            logger.error(f"AUDIT | AnalysisAgent | Failure | Reason: {str(e)}")
            return {"error": "Calculation exception"}
