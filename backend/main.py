from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.agents.orchestrator import StockAnalysisPipeline
from backend.models.response_models import StockAnalysisResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = StockAnalysisPipeline()

@app.get("/")
def home():
    return {"message": "AI Financial Stock Analyzer API"}



@app.get("/analyze/{ticker}", response_model=StockAnalysisResponse)
def analyze_stock(ticker: str):
    result = pipeline.run(ticker)
    return result