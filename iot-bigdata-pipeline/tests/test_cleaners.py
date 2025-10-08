import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_cleaning.cleaners import DataCleaner, AnomalyDetector

class TestCleaners:
    def test_data_cleaner_valid_data(self):
        cleaner = DataCleaner()
        test_data = {
            'temperature': 25.5,
            'humidity': 60.0,
            'timestamp': '2024-01-01T10:00:00'
        }
        
        cleaned = cleaner.clean(test_data)
        assert cleaned['temperature_status'] == 'valid'
        assert cleaned['humidity_status'] == 'valid'
        assert 'cleaned_at' in cleaned