from fastapi import FastAPI
from app.routers import stocks

app = FastAPI(
    title="Stock Data API",
    description="API for accessing comprehensive stock market data",
    version="1.0.0",
)

app.include_router(stocks.router, prefix="/api/v1/stocks", tags=["stocks"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Stock Data API"}
