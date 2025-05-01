from pymongo import MongoClient
from datetime import datetime

#TODO Fix hotcoded values

class MongoDatabase:

    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):

        client = MongoClient("mongodb://localhost:27017/")
        db = client[self.db_name]
        collection = db["temperature_data"]

        doc = {
            "sensor": "temp_sensor_1",
            "timestamp": datetime.utcnow(),
            "value": 25.4
        }

        collection.insert_one(doc)

        result = collection.find_one({"sensor": "temp_sensor_1"})
        print("Inserted Document:", result)
