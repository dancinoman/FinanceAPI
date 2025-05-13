from fastapi import FastAPI, HTTPException, Request, Query
from typing import List
import requests
import time

# Import classes
from app.exception_handler import ExceptionHandler
from app.pydantic import StockPriceData, TimeSeriesIntraday, ErrorResponse

class APIStructure:

    def __init__(self, api_key: str):
        self.app = FastAPI()
        self.setup_routes()
        self.base_url = "https://www.alphavantage.co/query"
        self.api_key = api_key
        self.cache = {}
        fake_db = {
            "123": {"id": "123", "value": "From DB"}
        }

    def setup_routes(self):
        """
        Setup the API routes with main variables.
        Returns: 
            formatted_response: time series fetched by API and Pydantic tested.
        """
""""        async def get_data_from_cache_or_db(item_id: str):
            # Check cache
            if item_id in cache:
                print("Cache hit")
                return cache[item_id]
            # Check DB
            print("Cache miss, checking DB")
            data = fake_db.get(item_id)
            if data:
                cache[item_id] = data  # Save to cache
                return data
            raise HTTPException(status_code=404, detail="Item not found")""""
         
        @self.app.get("/")
        async def root():
            return {
                "message": "Error no params",
                "testing": "/stocks/intraday?symbol=GOOGL&interval=5min",
                "more info"    : "/docs"
            }
            
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

            used_function = ExceptionHandler(function)
            function_param = used_function.function_rules()

            try:
                # Raise issue if limitations symbols are exceeded
                errors = used_function.handle_errors(function_param, params, symbol, request)
                if errors:
                    raise HTTPException(status_code=400, detail=", ".join(errors))

                # Check cache and fetch data
                if self.manage_cache():
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
                
                # Time series format data
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

    def manage_cache(self):
        """
        Use cache to store date
        """
        
