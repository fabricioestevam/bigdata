import random
from .interfaces import ISensor
from typing import Dict, Any, Optional

class DHT22Sensor(ISensor):
    base_temperature = 25.0
    base_humidity = 50.0

    def read_data(self) -> Optional[Dict[str, Any]]:
        temperature = self.base_temperature + random.uniform(-2, 2)
        humidity = self.base_humidity + random.uniform(-10, 10)
        return {"temperature": temperature, "humidity": humidity, "sensor_id": "DHT22_LAB_001"}
