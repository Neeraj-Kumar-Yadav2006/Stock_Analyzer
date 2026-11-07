from pydantic import BaseModel
from typing import List


class Indicators(BaseModel):
    RSI: float
    MA14: float
    volatility: float


class Sentiment(BaseModel):
    sentiment: str
    score: float
    articles_analyzed: int


class Signal(BaseModel):
    signal: str


class ChartPoint(BaseModel):
    day: str
    price: float


class StockAnalysisResponse(BaseModel):
    ticker: str
    price: float
    indicators: Indicators
    sentiment: Sentiment
    signal: Signal
    news: List[str]
    report: str
    chart: List[ChartPoint]