from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class StockResponse(BaseModel):
    symbol: str
    data: Dict[str, Any]

class MultiStockResponse(BaseModel):
    stocks: List[StockResponse]

class QueryRequest(BaseModel):
    conditions: List[str]
    limit: Optional[int] = 20