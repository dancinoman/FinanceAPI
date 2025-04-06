
class FunctionStructure:
    """
    Class to define function rules for the api.
    """

    def __init__(self, function: str):

        self.function = function

    def function_rules(self):

        limitations = {
            "TIME_SERIES_INTRADAY": {
                "max_symbols": 1,
                "intervals": ["1min", "5min", "15min", "30min", "60min"],
                "required": ["function","symbol", "interval"],
                "limit": 1000
            },
            "ANALYTICS_FIXED_WINDOW": {
                "max_symbols": 10,
                "range": ["full","day", "week", "month", "year"],
                "required": ["function","symbol", "range"],
                "limit": 500
            },

            # Add more functions and their limitations as needed
        }

        return limitations.get(self.function, {})
