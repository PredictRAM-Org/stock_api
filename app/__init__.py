"""
stock_api.app - The core package for the Stock Data API

Exposes the main FastAPI application and key components
"""

from .main import app  # Import the FastAPI application instance
from .models import StockResponse, MultiStockResponse, QueryRequest
from .utils import filter_stocks, evaluate_condition

# Define what gets imported with 'from stock_api.app import *'
__all__ = [
    'app',
    'StockResponse',
    'MultiStockResponse',
    'QueryRequest',
    'filter_stocks',
    'evaluate_condition'
]

# Package version
__version__ = '1.0.0'
