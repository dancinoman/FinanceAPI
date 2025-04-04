import dotenv
import os
import requests
import json

import time

dotenv.load_dotenv()

class StockMarket:
    def __init__(self):
        self.api_key = os.environ.get("API_KEY")
        self.base_url = "https://www.alphavantage.co/query"
        self.limitation = {"advanced analytics": 5, "technical indicators": 5}

    def get_stock_data(self, symbol):
        params = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": symbol,
            "apikey": self.api_key,
            "outputsize": "compact",
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        return data
    def get_technical_indicators(self, symbol, indicator):

        symbols = ["AAPL", "GOOG", "MSFT"]

        for symbol in symbols:
            params = {"function": "TIME_SERIES_DAILY_ADJUSTED", "symbol": symbol, "apikey": self.api_key}
            try:
                response = requests.get(self.base_url, params=params)
                response.raise_for_status()  # Raise an exception for bad status codes
                data = response.json()
                print(f"Data for {symbol}: {data.get('Meta Data', {}).get('Symbol')}")
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data for {symbol}: {e}")

            print("Waiting for 12 seconds...")
            time.sleep(12)  # Delay to stay within Alpha Vantage's free tier limit
