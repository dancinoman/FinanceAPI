
from pydantic import BaseModel
from typing import Dict

class StockPriceData(BaseModel):
    """Represents the structure of the intraday stock price data."""
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: int

class TimeSeriesIntraday(BaseModel):
    """Represents the structure of the Alpha Vantage intraday time series response."""
    meta: Dict
    time_series: Dict[str, StockPriceData]

class ErrorResponse(BaseModel):
    """Represents an error response from the API."""
    detail: str
