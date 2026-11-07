from textblob import TextBlob
import re
import statistics

from backend.agents.llm_agent import llm_sentiment

class SentimentAgent:
    """Generic sentiment analyzer for news headlines"""

    def __init__(self, topic=None):
        self.topic = topic.lower() if topic else None

        # sets are faster than lists for lookup
        self.positive_words = {
            "surge", "growth", "profit", "record", "launch", "upgrade",
            "gain", "rise", "beat", "strong", "improve"
        }

        self.negative_words = {
            "exploit", "lawsuit", "decline", "fraud", "recall", "ban",
            "drop", "loss", "weak", "fall", "cut"
        }

        self.url_pattern = re.compile(r"http\S+")
        self.symbol_pattern = re.compile(r"[^a-zA-Z0-9\s]")

    def clean_text(self, text):
        """Remove URLs and special characters"""
        text = self.url_pattern.sub("", text)
        text = self.symbol_pattern.sub("", text)
        return text.strip().lower()

    def keyword_adjustment(self, text):
        """Adjust polarity using domain keywords"""
        words = set(text.split())

        pos_hits = words & self.positive_words
        neg_hits = words & self.negative_words

        return (0.1 * len(pos_hits)) - (0.1 * len(neg_hits))

    def analyze(self, headlines):
        """Analyze sentiment using LLM first, fallback to rule-based"""

    # 🔥 STEP 1: Try LLM
        llm_result = llm_sentiment(headlines)

        if llm_result:
            return {
            "sentiment": llm_result.get("sentiment", "Neutral"),
            "score": llm_result.get("score", 0.5),
            "articles_analyzed": len(headlines),
            "source": "llm"

        }
        scores = []

        for headline in headlines:

            # Skip non-ascii for safety
            if not headline.isascii():
                continue

            text = self.clean_text(headline)

            # Topic filtering (optional)
            if self.topic and self.topic not in text:
                continue

            polarity = TextBlob(text).sentiment.polarity
            polarity += self.keyword_adjustment(text)

            scores.append(polarity)

        if not scores:
            return {
                "sentiment": "Neutral",
                "score": 0.0,
                "articles_analyzed": 0
            }

        avg_score = statistics.mean(scores)
        median_score = statistics.median(scores)
        final_score = (avg_score + median_score) / 2

        sentiment = (
            "Positive" if final_score > 0.1
            else "Negative" if final_score < -0.1
            else "Neutral"
        )

        return {
            "sentiment": sentiment,
            "score": round(final_score, 3),
            "articles_analyzed": len(scores)
        }