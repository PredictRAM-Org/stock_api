# stock_apiTest/__init__.py
from .app.main import app  # This exposes the FastAPI app at package level

__version__ = "1.0.0"
__all__ = ["app"]  # Controls what gets imported with 'from stock_apiTest import *'
