import dotenv
import os
import requests

#import class
from app.functions import Functions

dotenv.load_dotenv()

class StockMarket:
    def __init__(self):
        self.api_key = os.environ.get("API_KEY")
        self.function = "TIME_SERIES_INTRADAY"
        self.base_url = "https://www.alphavantage.co/query"
        self.symbols = ["AAPL"]
        self.interval = "5min"

    def cache_allow(self):
        """
        Check if the cache is allowed.
        """
        # Placeholder for cache logic
        return True

    def execute(self):

        # Build function rules
        params = {
            "function": self.function,
            "symbol": self.symbols,
            "apikey": self.api_key,
            "interval": self.interval
        }

        used_function = Functions(self.function)
        function_param = used_function.function_rules(self.function, params)


        try:
            # Raise issue if limitations symbols are exceeded
            if self.handle_errors(function_param, params) == False: return

            # Check cache and fetch data
            if self.cache_allow():
                pass

            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            print(data)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {self.symbols}: {e}")


    def handle_errors(self, function_param, params):
        """
        Handle errors based on function parameters.
        """
        # Check if the number of symbols exceeds the limit
        if function_param["symbols"] < len(self.symbols):
            print(f"Exceeded the limit of {function_param['symbols']} symbol(s).")
            return False

        # Handle parameter requirements
        if function_param["requiered"]:
            for param in params:
                if param not in function_param["requiered"]:
                    print(f"Missing required parameter: {param}")
                    return False


        # Check if the time delay limit is exceeded
        if function_param["time delay limit"] < 5:
            print(f"Exceeded the time delay limit of {function_param['time delay limit']} seconds.")
            return False

        return True



if __name__ == "__main__":
    stock_market = StockMarket()
    stock_market.execute()
