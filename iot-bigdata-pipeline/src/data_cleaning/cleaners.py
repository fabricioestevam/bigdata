from typing import Dict, Any, Optional
from datetime import datetime
from src.core.interfaces import IDataCleaner
from src.config import Config

class DataCleaner(IDataCleaner):
    """Data cleaning and validation following Single Responsibility Principle"""
    
    def clean(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply comprehensive data cleaning pipeline"""
        cleaned_data = data.copy()
        
        # Apply cleaning steps
        cleaned_data = self._validate_temperature(cleaned_data)
        cleaned_data = self._validate_humidity(cleaned_data)
        cleaned_data = self._add_metadata(cleaned_data)
        cleaned_data = self._remove_invalid_readings(cleaned_data)
        
        return cleaned_data
    
    def _validate_temperature(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean temperature data"""
        temp = data.get('temperature')
        min_temp, max_temp = Config.TEMPERATURE_RANGE
        
        if temp is None or not isinstance(temp, (int, float)):
            data['temperature'] = None
            data['temperature_status'] = 'invalid'
        elif temp < min_temp or temp > max_temp:
            data['temperature_status'] = 'out_of_range'
        else:
            data['temperature_status'] = 'valid'
            
        return data
    
    def _validate_humidity(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean humidity data"""
        humidity = data.get('humidity')
        min_hum, max_hum = Config.HUMIDITY_RANGE
        
        if humidity is None or not isinstance(humidity, (int, float)):
            data['humidity'] = None
            data['humidity_status'] = 'invalid'
        elif humidity < min_hum or humidity > max_hum:
            data['humidity_status'] = 'out_of_range'
        else:
            data['humidity_status'] = 'valid'
            
        return data
    
    def _add_metadata(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add cleaning metadata"""
        data['cleaned_at'] = datetime.utcnow()
        data['cleaning_version'] = '1.0'
        return data
    
    def _remove_invalid_readings(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Remove readings that are completely invalid"""
        if (data.get('temperature_status') == 'invalid' and 
            data.get('humidity_status') == 'invalid'):
            return None  # Signal to discard this reading
        return data

class AnomalyDetector(IDataCleaner):
    """Advanced anomaly detection for sensor data"""
    
    def clean(self, data: Dict[str, Any]) -> Dict[str, Any]:
        cleaned_data = data.copy()
        cleaned_data['anomaly_score'] = self._calculate_anomaly_score(data)
        return cleaned_data
    
    def _calculate_anomaly_score(self, data: Dict[str, Any]) -> float:
        """Calculate anomaly score based on data patterns"""
        score = 0.0
        
        # Temperature anomaly detection
        temp = data.get('temperature', 0)
        if not (15 <= temp <= 35):  # Expected range for indoor environments
            score += 0.5
        
        # Humidity anomaly detection
        humidity = data.get('humidity', 0)
        if not (30 <= humidity <= 80):  # Expected range for indoor environments
            score += 0.5
            
        return min(score, 1.0)