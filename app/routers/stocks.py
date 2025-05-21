from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
import json
from pathlib import Path

router = APIRouter()

# Load the stock data
DATA_PATH = Path(__file__).parent.parent / "data" / "all_stocks.json"
with open(DATA_PATH, "r") as f:
    stocks_data = json.load(f)

@router.get("/")
async def get_all_stocks(
    limit: int = Query(100, description="Number of stocks to return"),
    skip: int = Query(0, description="Number of stocks to skip")
):
    """Get all stocks with pagination"""
    return list(stocks_data.values())[skip:skip + limit]

@router.get("/{symbol}")
async def get_stock_by_symbol(symbol: str):
    """Get stock data by symbol"""
    stock = stocks_data.get(symbol.upper())
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock

@router.get("/industry/{industry}")
async def get_stocks_by_industry(
    industry: str,
    limit: int = Query(100, description="Number of stocks to return"),
    skip: int = Query(0, description="Number of stocks to skip")
):
    """Get stocks by industry"""
    filtered = [s for s in stocks_data.values() if s.get("Stock Industry", "").lower() == industry.lower()]
    return filtered[skip:skip + limit]

@router.get("/filter/")
async def filter_stocks(
    cagr_min: Optional[float] = Query(None, description="Minimum CAGR"),
    roe_min: Optional[float] = Query(None, description="Minimum Return on Equity"),
    roi_min: Optional[float] = Query(None, description="Minimum Return on Investment"),
    sharpe_min: Optional[float] = Query(None, description="Minimum Sharpe Ratio"),
    volatility_max: Optional[float] = Query(None, description="Maximum Volatility"),
    dividend_min: Optional[float] = Query(None, description="Minimum Dividend Yield"),
    limit: int = Query(20, description="Number of stocks to return")
):
    """Filter stocks based on various criteria"""
    filtered = []
    
    for stock in stocks_data.values():
        include = True
        
        if cagr_min is not None:
            cagr = stock.get("CAGR", 0)
            if cagr is None or cagr < cagr_min:
                include = False
                
        if roe_min is not None:
            roe = stock.get("Return on Equity (ttm)", stock.get("Return_on_Equity", 0))
            if roe is None or roe < roe_min:
                include = False
                
        if roi_min is not None:
            roi = stock.get("Return_on_Investment", stock.get("ROI", 0))
            if roi is None or roi < roi_min:
                include = False
                
        if sharpe_min is not None:
            sharpe = stock.get("Sharpe Ratio", 0)
            if sharpe is None or sharpe < sharpe_min:
                include = False
                
        if volatility_max is not None:
            volatility = stock.get("Annualized Volatility (%)", stock.get("Volatility", 0))
            if volatility is None or volatility > volatility_max:
                include = False
                
        if dividend_min is not None:
            dividend = stock.get("Dividend_Yield", stock.get("Trailing Annual Dividend Yield", 0))
            if dividend is None or dividend < dividend_min:
                include = False
                
        if include:
            filtered.append(stock)
            if len(filtered) >= limit:
                break
                
    return filtered

@router.get("/query/growth")
async def query_growth_stocks(
    cagr_min: float = Query(15, description="Minimum CAGR"),
    roe_min: float = Query(20, description="Minimum Return on Equity"),
    limit: int = Query(20, description="Number of stocks to return")
):
    """Query for growth stocks with high CAGR and ROE"""
    filtered = []
    
    for stock in stocks_data.values():
        cagr = stock.get("CAGR", 0)
        roe = stock.get("Return on Equity (ttm)", stock.get("Return_on_Equity", 0))
        
        if cagr is not None and roe is not None and cagr > cagr_min and roe > roe_min:
            filtered.append(stock)
            if len(filtered) >= limit:
                break
                
    return filtered

@router.get("/query/defensive")
async def query_defensive_stocks(
    sharpe_min: float = Query(1.2, description="Minimum Sharpe Ratio"),
    volatility_max: float = Query(20, description="Maximum Volatility"),
    dividend_min: float = Query(3, description="Minimum Dividend Yield"),
    limit: int = Query(20, description="Number of stocks to return")
):
    """Query for defensive stocks with good risk metrics and dividends"""
    filtered = []
    
    for stock in stocks_data.values():
        sharpe = stock.get("Sharpe Ratio", 0)
        volatility = stock.get("Annualized Volatility (%)", stock.get("Volatility", 0))
        dividend = stock.get("Dividend_Yield", stock.get("Trailing Annual Dividend Yield", 0))
        
        if (sharpe is not None and volatility is not None and dividend is not None and
            sharpe > sharpe_min and volatility < volatility_max and dividend > dividend_min):
            filtered.append(stock)
            if len(filtered) >= limit:
                break
                
    return filtered