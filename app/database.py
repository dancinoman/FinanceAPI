from typing import List

class Redis:
    def __init__(self):
        self.cache = {"GOOGL_5min": "From Cache"}
        self.fake_db = {
            "123": {"id": "123", "value": "From DB"}
        }
    def get_key(self, symbol: List[str], interval: str):
        return f"{','.join(symbol)}_{interval}"

    def set(self, key, value):
        self.cache[key] = value

    def clear(self):
        self.cache.clear()
