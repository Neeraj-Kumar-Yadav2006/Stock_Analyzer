# Stock Analyzer

AI-powered multi-agent system for automated stock analysis, sentiment evaluation, and report generation.

Built as a collaborative project focusing on **agentic AI architecture**, modular data pipelines, and real-time financial intelligence.

---

## Overview

Stock Analyzer replaces the manual workflow of checking prices, reading news, and writing summaries with an autonomous multi-agent pipeline.

**What it does:**

- Fetches live stock data
- Computes technical indicators (RSI, Moving Average, Volatility)
- Collects and analyzes news sentiment
- Generates trading signals (BUY / SELL / HOLD)
- Produces structured financial reports using LLMs
- Caches results in SQLite for performance
- Serves everything through a FastAPI backend + React dashboard

---

## Architecture

User (React Dashboard)
↓
FastAPI Backend
↓
Orchestrator (Pipeline Controller)
├── Stock Data Agent → yfinance + Database
├── Analysis Agent → RSI, MA14, Volatility
├── News Agent → NewsAPI / fallback
├── Sentiment Agent → LLM + TextBlob fallback
├── Strategy Agent → Rule-based signal
└── Report Agent → LLM structured report
↓
SQLite Database (cache + persistence)

### Agent Responsibilities

| Agent               | Role                                                       |
| ------------------- | ---------------------------------------------------------- |
| **Orchestrator**    | Coordinates the full pipeline, caching, and error handling |
| **Stock Fetcher**   | Live quotes + historical prices (yfinance)                 |
| **Analysis Agent**  | Technical indicators from price series                     |
| **Sentiment Agent** | LLM-first sentiment with rule-based fallback               |
| **Strategy Agent**  | Combines RSI + sentiment into BUY/SELL/HOLD                |
| **Report Agent**    | Generates human-readable financial summary                 |
| **Database Layer**  | SQLite storage for prices, news, sentiment, reports        |

---

## Tech Stack

**Backend**

- Python 3.11+
- FastAPI
- yfinance
- pandas
- TextBlob / OpenRouter (LLM)
- SQLite (modular database layer)

**Frontend**

- React
- Recharts
- Axios

**Infrastructure**

- Uvicorn
- python-dotenv

---

## Project Structure

FIAP/
├── backend/
│ ├── main.py # FastAPI app
│ ├── agents/
│ │ ├── orchestrator.py # Main pipeline
│ │ ├── analysis_agent.py
│ │ ├── sentiment_agent.py
│ │ ├── strategy_agent.py
│ │ ├── report_agent.py
│ │ └── llm_agent.py
│ ├── models/
│ └── utils/
├── data/
│ ├── database_lib/ # SQLite operations
│ ├── stock_fetcher_lib/ # Stock data layer
│ ├── news_fetcher_lib/
│ ├── schema.sql
│ └── config.py
├── tools/
├── frontend/ # React dashboard
├── requirements.txt
└── README.md

## Setup & Run

### 1. Clone & Environment

```bash
git clone git@github.com:Neeraj-Kumar-Yadav2006/Stock_Analyzer.git
cd Stock_Analyzer

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
python -m textblob.download_corpora

2. Environment Variables

Create a .env file in the root:


The system works without API keys using rule-based fallbacks.

3. Initialize Database

python -c "from data.database_lib.manager import DatabaseManager; DatabaseManager().init_DB()"

4. Start Backend
# Recommended on Python 3.12 (Windows)
set PYTHONSAFEPATH=1
python -m uvicorn backend.main:app --port 8000

API docs: http://127.0.0.1:8000/docs
Test endpoint: http://127.0.0.1:8000/analyze/AAPL

5. Start Frontend
cd frontend
npm install
npm start

Open: http://localhost:3000

API Example
Request

GET /analyze/AAPL

Response (simplified)

{
  "ticker": "AAPL",
  "price": 303.42,
  "indicators": {
    "RSI": 56.10,
    "MA14": 299.69,
    "volatility": 0.0258
  },
  "sentiment": {
    "sentiment": "Neutral",
    "score": 0.0,
    "articles_analyzed": 0
  },
  "signal": {
    "signal": "HOLD"
  },
  "news": [],
  "report": "FINANCIAL ANALYSIS REPORT — AAPL ...",
  "chart": [
    { "day": "Tue", "price": 340.08 },
    { "day": "Wed", "price": 338.19 }
  ]
}

Design Decisions

Multi-agent architecture
Clear separation of concerns. Each agent can be improved or replaced independently.
Database as cache + history
First request may be live; subsequent requests can reuse stored prices, news, and sentiment.
LLM with fallbacks
OpenRouter (free models) for summaries and sentiment. Rule-based path when keys or network fail.
Simple strategy layer
RSI + sentiment rules keep the signal logic transparent and easy to explain in interviews.
FastAPI + React
Backend focuses on intelligence; frontend focuses on visualization.


Current Limitations

News depends on external API key (empty news → neutral sentiment)
Strategy is rule-based (not ML-based prediction)
Not financial advice — educational / research use only
Single-ticker analysis (no portfolio view yet)


Future Improvements

LangGraph / proper agent orchestration framework
Vector memory for news history
Multi-ticker portfolio dashboard
Backtesting module
Authentication and rate limiting


Team Contributions

Multi-agent backend & orchestrator — pipeline design, analysis, strategy, LLM integration
Database & data layer — modular SQLite schema and operations
React frontend — dashboard, charts, report display


Disclaimer
This project is for educational and research purposes only.
It does not constitute financial advice.
```
