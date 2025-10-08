import random
from datetime import datetime
from typing import Dict, Any
from .interfaces import ISensor
# REMOVA esta linha: from src.config import Config

class DHT22Sensor(ISensor):
    """Simulated DHT22 Temperature and Humidity Sensor"""
    
    def read_data(self) -> Dict[str, Any]:
        # Agora vamos importar Config dentro do método para evitar circular import
        from config import Config
        
        if Config.SENSOR_SIMULATION:
            return self._generate_simulated_data()
        else:
            return self._read_physical_sensor()
    
    def _generate_simulated_data(self) -> Dict[str, Any]:
        """Generate realistic sensor data with occasional anomalies"""
        base_temp = random.uniform(20, 30)
        base_humidity = random.uniform(40, 70)
        
        # Simulate occasional sensor errors (5% chance)
        if random.random() < 0.05:
            base_temp = random.uniform(-100, 100)  # Invalid range
            base_humidity = random.uniform(-10, 110)  # Invalid range
        
        return {
            "temperature": round(base_temp, 2),
            "humidity": round(base_humidity, 2),
            "timestamp": datetime.utcnow(),
            "sensor_id": "DHT22_SIM_001",
            "sensor_type": "temperature_humidity"
        }
    
    def _read_physical_sensor(self) -> Dict[str, Any]:
        """Placeholder for real sensor reading"""
        raise NotImplementedError("Physical sensor not implemented in simulation mode")

class SensorFactory:
    """Factory class for creating different sensor types"""
    
    @staticmethod
    def create_sensor(sensor_type: str = "DHT22") -> ISensor:
        if sensor_type == "DHT22":
            return DHT22Sensor()
        else:
            raise ValueError(f"Unsupported sensor type: {sensor_type}")