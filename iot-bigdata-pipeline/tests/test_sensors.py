import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.sensors import DHT22Sensor, SensorFactory

class TestSensors:
    def test_dht22_sensor_creation(self):
        sensor = SensorFactory.create_sensor("DHT22")
        assert sensor is not None
        assert isinstance(sensor, DHT22Sensor)