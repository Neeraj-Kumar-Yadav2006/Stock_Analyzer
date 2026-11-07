"""
LLM Agent - Uses FREE OpenRouter API (DeepSeek model)
Set OPENROUTER_API_KEY in your .env file.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-chat:free"


def _call_llm(prompt: str, max_tokens: int = 500) -> str:
    """Internal helper to call OpenRouter API."""
    if not OPENROUTER_API_KEY:
        print("[LLMAgent] WARNING: OPENROUTER_API_KEY not set. Falling back to rule-based.")
        return ""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
    }

    try:
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[LLMAgent] OpenRouter API error: {e}")
        return ""


def summarize_news(ticker: str, headlines: list[str], price: float, signal: str) -> str:
    if not headlines:
        return "No recent news articles found for this stock."

    headlines_text = "\n".join(f"- {h}" for h in headlines[:5])

    prompt = f"""You are a financial analyst. Given the following news headlines for {ticker} stock (current price: ${price}, signal: {signal}), write a concise 4-5 line summary.

Headlines:
{headlines_text}

Write only the summary paragraph."""

    result = _call_llm(prompt, max_tokens=200)

    if not result:
        return f"Recent news for {ticker}: " + " | ".join(headlines[:3])

    return result

def generate_llm_report(
    ticker: str,
    price: float,
    change: float,
    indicators: dict,
    sentiment: dict,
    signal: str,
    news_summary: str,
) -> str:

    prompt = f"""You are a professional financial analyst. Generate a structured report for {ticker}.

Data:
- Price: ${price}
- Change: {change:+.2f}%
- RSI: {indicators.get('rsi', 'N/A')}
- MA14: {indicators.get('ma14', 'N/A')}
- Volatility: {indicators.get('volatility', 'N/A')}
- Sentiment: {sentiment.get('sentiment', 'N/A')}
- Confidence: {sentiment.get('score', 0):.2f}
- Signal: {signal}
- News: {news_summary}

Sections:
1. Executive Summary
2. Technical Analysis
3. Sentiment
4. Risk
5. Recommendation

Keep it concise (200-250 words)."""

    result = _call_llm(prompt, max_tokens=400)

    if not result:
        return _template_report(ticker, price, change, indicators, sentiment, signal, news_summary)

    return result

def _template_report(ticker, price, change, indicators, sentiment, signal, news_summary) -> str:
    rsi = indicators.get("rsi", 50)
    rsi_note = "oversold" if rsi < 30 else "overbought" if rsi > 70 else "neutral"
    direction = "up" if change >= 0 else "down"

    return f"""FINANCIAL ANALYSIS REPORT — {ticker}

EXECUTIVE SUMMARY
{ticker} is trading at ${price:.2f}, {direction} {abs(change):.2f}% today.
Signal: {signal}

TECHNICAL ANALYSIS
RSI: {rsi:.1f} ({rsi_note})
MA14: ${indicators.get('ma14', 0):.2f}
Volatility: {indicators.get('volatility', 0):.4f}

SENTIMENT
{sentiment.get('sentiment', 'Neutral')} (Score: {sentiment.get('score', 0):.2f})

NEWS
{news_summary}

RECOMMENDATION
{signal}
"""


def llm_sentiment(headlines: list[str]) -> dict:
    if not headlines or not OPENROUTER_API_KEY:
        return {}

    headlines_text = "\n".join(f"- {h}" for h in headlines[:5])

    prompt = f"""Analyze sentiment.

Headlines:
{headlines_text}

Format:
sentiment: Positive/Negative/Neutral
score: 0.0-1.0
reason: one sentence"""

    result = _call_llm(prompt, max_tokens=100)

    if not result:
        return {}

    try:
        lines = result.strip().split("\n")
        parsed = {}
        for line in lines:
            if ":" in line:
                k, v = line.split(":", 1)
                parsed[k.strip()] = v.strip()

        return {
            "sentiment": parsed.get("sentiment", "Neutral"),
            "score": float(parsed.get("score", 0.5)),
            "reason": parsed.get("reason", ""),
            "source": "llm",
        }
    except:
        return {}