from fastapi import FastAPI, HTTPException, Request, Query
from pydantic import BaseModel
from typing import List, Dict
import requests
import time

# Import classes
from app.functions import FunctionStructure  # Assuming this exists

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

class APIStructure:
    REQUEST_HISTORY_PER_IP = {}
    MAX_REQUESTS_PER_MINUTE_PER_IP = 5

    def __init__(self, api_key: str):
        self.app = FastAPI()
        self.setup_routes()
        self.base_url = "https://www.alphavantage.co/query"
        self.api_key = api_key

    def setup_routes(self):
        """
        Setup the API routes with main variables.
        """
        @self.app.get(
            "/stocks/intraday",
            response_model=TimeSeriesIntraday,
            responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
        )
        async def get_intraday_stock_data(
            symbol: List[str] = Query(["AAPL"], description="List of stock symbols (e.g., AAPL, MSFT)"),
            interval: str = Query("5min", description="Time interval (e.g., 1min, 5min, 15min, 30min, 60min)"),
            function: str = Query("TIME_SERIES_INTRADAY", description="Alpha Vantage function"),
            request: Request = None
        ):
            params = {
                "function": function,
                "symbol": ",".join(symbol),
                "apikey": self.api_key,
                "interval": interval,
            }

            used_function = FunctionStructure(function)
            function_param = used_function.function_rules()

            try:
                # Raise issue if limitations symbols are exceeded
                errors = self.handle_errors(function_param, params, symbol, request)
                if errors:
                    raise HTTPException(status_code=400, detail=", ".join(errors))

                # Check cache and fetch data
                if self.cache_allow():
                    pass

                # Execute request
                response = requests.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()

                if "Error Message" in data:
                    raise HTTPException(status_code=400, detail=data["Error Message"])

                time_series_key = f"Time Series ({interval})"
                if not data.get(time_series_key):
                    raise HTTPException(status_code=404, detail=f"No intraday data found for {symbol} at {interval}")

                # Structure the response according to the Pydantic model
                metadata = data.get("Meta Data", {})
                time_series_data = data.get(time_series_key, {})
                formatted_time_series = {}
                for timestamp, values in time_series_data.items():
                    stock_data = StockPriceData(
                        timestamp=timestamp,
                        open=float(values.get("1. open")),
                        high=float(values.get("2. high")),
                        low=float(values.get("3. low")),
                        close=float(values.get("4. close")),
                        volume=int(values.get("5. volume"))
                    )
                    formatted_time_series[timestamp] = stock_data
                formatted_response = TimeSeriesIntraday(
                    meta=metadata,
                    time_series=formatted_time_series
                )

                return formatted_response

            except requests.exceptions.RequestException as e:
                raise HTTPException(status_code=500, detail=f"Error connecting to Alpha Vantage: {e}")
            except HTTPException as e:
                raise e
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

    def cache_allow(self):
        """
        Check if the cache is allowed.
        """
        # Placeholder for cache logic
        return True

    def handle_errors(self, function_param, params, symbols, request=None):
        """
        Handle errors based on function parameters and rate limits.
        """
        errors = []

        # Rate Limiting (Example per IP)
        if request:
            client_ip = request.client.host
            now = time.time()

            if client_ip not in self.REQUEST_HISTORY_PER_IP:
                self.REQUEST_HISTORY_PER_IP[client_ip] = []

            self.REQUEST_HISTORY_PER_IP[client_ip][:] = [
                t for t in self.REQUEST_HISTORY_PER_IP[client_ip] if t > now - 60
            ]

            if len(self.REQUEST_HISTORY_PER_IP[client_ip]) >= self.MAX_REQUESTS_PER_MINUTE_PER_IP:
                errors.append(f"Too many requests from IP {client_ip}. Please try again later.")
                return errors  # Return immediately if rate limited

            self.REQUEST_HISTORY_PER_IP[client_ip].append(now)

        # Check if the number of symbols exceeds the limit
        if "symbol" in function_param and function_param["symbol"] < len(symbols):
            errors.append(f"Exceeded the limit of {function_param['symbol']} symbol(s).")

        # Handle parameter requirements
        if function_param.get("required"):
            for req_param in function_param["required"]:
                if req_param not in params:
                    errors.append(f"Missing required parameter: {req_param}")

        # Check if the time delay limit is exceeded (this might be related to external API limits)
        if "time delay limit" in function_param and function_param["time delay limit"] < 5:
            errors.append(f"Exceeded the time delay limit of {function_param['time delay limit']} seconds.")

        return errors
