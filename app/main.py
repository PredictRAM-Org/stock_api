from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
import pandas as pd
from pathlib import Path
from pydantic import BaseModel
from app.utils import filter_stocks

app = FastAPI(
    title="Stock Data API",
    description="API for accessing comprehensive stock market data from Excel",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the stock data from Excel
DATA_PATH = Path(__file__).parent / "data" / "merged_stock_data.xlsx"

def load_stock_data():
    """Load and process Excel data into dictionary format"""
    try:
        df = pd.read_excel(DATA_PATH)
        # Convert NaN to None for JSON compatibility
        df = df.where(pd.notnull(df), None)
        
        # Convert to dictionary with stock symbol as key
        stocks_data = {}
        for _, row in df.iterrows():
            symbol = row.get('Stock Symbol')
            if symbol:
                stocks_data[symbol] = row.to_dict()
        return stocks_data
    except Exception as e:
        raise RuntimeError(f"Error loading Excel data: {str(e)}")

# Load data at startup
stocks_data = load_stock_data()

class StockResponse(BaseModel):
    symbol: str
    data: Dict[str, Any]

class MultiStockResponse(BaseModel):
    stocks: List[StockResponse]

class QueryRequest(BaseModel):
    conditions: List[str]
    limit: Optional[int] = 20

@app.get("/")
def read_root():
    return {"message": "Welcome to the Stock Data API (Excel version)"}

@app.get("/stocks", response_model=MultiStockResponse)
def get_all_stocks():
    """Get all stocks data"""
    return {"stocks": [{"symbol": k, "data": v} for k, v in stocks_data.items()]}

@app.get("/stocks/{symbol}", response_model=StockResponse)
def get_stock_by_symbol(symbol: str):
    """Get data for a specific stock by symbol"""
    if symbol not in stocks_data:
        raise HTTPException(status_code=404, detail="Stock not found")
    return {"symbol": symbol, "data": stocks_data[symbol]}

@app.get("/stocks/industry/{industry}", response_model=MultiStockResponse)
def get_stocks_by_industry(industry: str):
    """Get all stocks in a specific industry"""
    industry_stocks = [
        {"symbol": k, "data": v} 
        for k, v in stocks_data.items() 
        if v.get("Stock Industry", "").lower() == industry.lower()
    ]
    if not industry_stocks:
        raise HTTPException(status_code=404, detail=f"No stocks found in industry: {industry}")
    return {"stocks": industry_stocks}

@app.post("/stocks/query", response_model=MultiStockResponse)
def query_stocks(query: QueryRequest):
    """Query stocks based on multiple conditions"""
    results = filter_stocks(stocks_data, query.conditions, query.limit)
    return {"stocks": results}

@app.get("/industries", response_model=List[str])
def get_all_industries():
    """Get list of all unique industries"""
    industries = set()
    for stock in stocks_data.values():
        if "Stock Industry" in stock and stock["Stock Industry"]:
            industries.add(stock["Stock Industry"])
    return sorted(industries)

@app.get("/reload")
def reload_data():
    """Endpoint to reload data from Excel (for development)"""
    global stocks_data
    stocks_data = load_stock_data()
    return {"message": "Data reloaded successfully", "count": len(stocks_data)}