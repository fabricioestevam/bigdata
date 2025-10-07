import os

MONGO_CONNECTION = os.getenv("MONGO_CONNECTION", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "iot_data")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "temperature_readings")
