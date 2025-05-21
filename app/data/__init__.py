"""
stock_api.app.data - Package for handling stock data files

Provides data loading functionality for the API
"""

import json
from pathlib import Path

# Define the data file path relative to this package
DATA_FILE = Path(__file__).parent / 'all_stocks.json'

def load_stock_data():
    """Load and return the stock data from JSON file"""
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

__all__ = ['load_stock_data']
