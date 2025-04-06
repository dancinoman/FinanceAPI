from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List
import requests

# Import classes
from functions import FunctionStructure

class APIStructure:
    def __init__(self, api_key: str, function: str, symbols: List[str], *args):
        self.app = FastAPI()
        self.setup_routes()
        self.base_url = "https://www.alphavantage.co/query"
        api_key = api_key
        self.function = function
        self.symbols = symbols
        self.more_params = args

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
            symbols: List[str] = Query(["AAPL"], description="List of stock symbols (e.g., AAPL, MSFT)"),
            interval: str = Query("5min", description="Time interval (e.g., 1min, 5min, 15min, 30min, 60min)"),
        ):

            params = {
                "function": self.function,
                "symbol": self.symbols,
                "apikey": self.api_key,
                "interval": self.more_params["interval"]
            }

            used_function = FunctionStructure(self.function)
            function_param = used_function.function_rules(self.function, params)

            try:
                # Raise issue if limitations symbols are exceeded
                if self.handle_errors(function_param, params) == False: return

                # Check cache and fetch data
                if self.cache_allow():
                    pass

                # Execute request
                response = requests.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()

                if "Error Message" in data:
                    raise HTTPException(status_code=400, detail=data["Error Message"])

                if not data.get(f"Time Series ({interval})"):
                    raise HTTPException(status_code=404, detail=f"No intraday data found for {symbols} at {interval}")

                # Structure the response according to the Pydantic model
                metadata = data.get("Meta Data", {})
                time_series = data.get(f"Time Series ({interval})", {})
                formatted_time_series = {
                    timestamp: StockPriceData(**values) for timestamp, values in time_series.items()
                }
                formatted_response = TimeSeriesIntraday(
                    meta=metadata,
                    time_series_5min=formatted_time_series  # Assuming interval maps to this key
                )

                return formatted_response

            except requests.exceptions.RequestException as e:
                raise HTTPException(status_code=500, detail=f"Error connecting to Alpha Vantage: {e}")
            except HTTPException as e:
                raise e
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

        def handle_errors(self, function_param, params):
            """
            Handle errors based on function parameters.
            """
            # Check if the number of symbols exceeds the limit
            if function_param["symbols"] < len(self.symbols):
                print(f"Exceeded the limit of {function_param['symbols']} symbol(s).")
                return False

            # Handle parameter requirements
            if function_param["required"]:
                for param in params:
                    if param not in function_param["required"]:
                        print(f"Missing required parameter: {param}")
                        return False


            # Check if the time delay limit is exceeded
            if function_param["time delay limit"] < 5:
                print(f"Exceeded the time delay limit of {function_param['time delay limit']} seconds.")
                return False

            return True

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
    meta: dict
    time_series_5min: dict[str, StockPriceData]

class ErrorResponse(BaseModel):
    """Represents an error response from the API."""
    detail: str
