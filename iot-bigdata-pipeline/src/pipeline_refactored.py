from src.core.sensors import DHT22Sensor
from src.core.storage import MongoDBStore
from src.data_cleaning.cleaners import DataCleaner
import time

def main():
    sensor = DHT22Sensor()
    cleaner = DataCleaner()
    storage = MongoDBStore()

    while True:
        data = sensor.read_data()
        cleaned_data = cleaner.clean(data)
        storage.save(cleaned_data)
        print(f"Saved: {cleaned_data}")
        time.sleep(5)

if __name__ == "__main__":
    main()
