
class FunctionStructure:
    """
    Class to define function rules for the api.
    """

    def __init__(self, function: str, params: dict):

        self.function = function
        self.params = params

        def function_rules(self, function: str, params: dict):

            limitations = {
                "TIME_SERIES_INTRADAY": {
                    "max_symbols": 5,
                    "intervals": ["1min", "5min", "15min", "30min", "60min"],
                    "required": ["function","symbols", "interval"],
                    "limit": 1000
                },
                "ANALYTICS_FIXED_WINDOW": {
                    "max_symbols": 10,
                    "range": ["full","day", "week", "month", "year"],
                    "required": ["function","symbols", "range"],
                    "limit": 500
                },

                # Add more functions and their limitations as needed
            }

            return limitations.get(function, {})
