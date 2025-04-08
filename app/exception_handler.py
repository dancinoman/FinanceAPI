import time
class ExceptionHandler:
    """
    Class to define function rules for the api.
    """

    def __init__(self, function: str):
        self.request_history_ip = {}
        self.max_requests_per_minute_per_ip = 5
        self.function = function

    def function_rules(self):

        limitations = {
            "TIME_SERIES_INTRADAY": {
                "max_symbols": 1,
                "interval": ["1min", "5min", "15min", "30min", "60min"],
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

    def handle_errors(self, function_param, params, symbols, request=None):
        """
        Handle errors based on function parameters and rate limits.
        """
        errors = []

        # Rate Limiting (Example per IP)
        if request:
            client_ip = request.client.host
            now = time.time()

            if client_ip not in self.request_history_ip:
                self.request_history_ip[client_ip] = []

            self.request_history_ip[client_ip][:] = [
                t for t in self.request_history_ip[client_ip] if t > now - 60
            ]

            if len(self.request_history_ip[client_ip]) >= self.max_requests_per_minute_per_ip:
                errors.append(f"Too many requests from IP {client_ip}. Please try again later.")
                return errors  # Return immediately if rate limited

            self.request_history_ip[client_ip].append(now)

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
