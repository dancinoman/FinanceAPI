
class Functions:
    def __init__(self, function):
        self.function = function

    def function_rules(self, function, params):
        """
        Function rules for the API.
        """
        function_param = {
            "TIME_SERIES_INTRADAY": {"symbols": 1, "time delay limit": 10, "requiered": ["function","symbol", "interval", "apikey"]},
            "REALTIME_OPTIONS":     {"symbols": 5, "time delay limit": 5, "requiered": ["function","symbol", "apikey"]}
        }

        return function_param[function]
