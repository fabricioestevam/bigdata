import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class following Single Responsibility Principle"""
    
    # MongoDB Configuration
    MONGO_CONNECTION = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DATABASE_NAME = os.getenv("DB_NAME", "iot_database")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "sensor_data")
    
    # Sensor Configuration
    SENSOR_SIMULATION = os.getenv("SENSOR_SIMULATION", "True").lower() == "true"
    DATA_GENERATION_INTERVAL = int(os.getenv("DATA_GENERATION_INTERVAL", "5"))
    
    # Data Validation Rules
    TEMPERATURE_RANGE = (-50, 60)  # Celsius
    HUMIDITY_RANGE = (0, 100)      # Percentage