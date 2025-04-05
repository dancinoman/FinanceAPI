import dotenv
import os
import requests
import json

import time

dotenv.load_dotenv()

class StockMarket:
    def __init__(self):
        self.api_key = os.environ.get("API_KEY")
        self.function = "REALTIME_OPTIONS"
        self.base_url = "https://www.alphavantage.co/query"
        self.symbols = ["AAPL", "GOOG", "IBM", "MSFT", "AMZN"]
        self.limitation = {
            "REALTIME_OPTIONS": {"symbols": 5, "time delay limit": 12}
            }

    def execute(self):

        params = {"function": self.function, "symbol": self.symbols, "apikey": self.api_key}
        try:

            # Raise issue if limitations symbols are exceeded
            if len(self.symbols) > self.limitation[self.function]["symbols"]:
                print(f"Exceeded the limit of {self.limitation[self.function]['symbols']} symbols.")
                return

            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            print(data)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {self.symbols}: {e}")

            print(f"Waiting for {self.limitaion['time delay limit']} seconds...")
            time.sleep(self.limitaion['time delay limit'])  # Delay to stay within Alpha Vantage's free tier limit




if __name__ == "__main__":
    stock_market = StockMarket()
    stock_market.execute()
