from typing import Dict, Any

class DataCleaner:
    def remove_outliers_iqr(self, data: Dict[str, Any]) -> Dict[str, Any]:
        temp = data.get("temperature")
        if temp is not None and (temp < -50 or temp > 100):
            data["_outlier_corrected"] = [{"field": "temperature", "original": temp, "corrected": 25.0}]
            data["temperature"] = 25.0
        return data

    def fill_missing_values(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if "humidity" not in data:
            data["humidity"] = 50.0
        return data

    def clean(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data = self.remove_outliers_iqr(data)
        data = self.fill_missing_values(data)
        return data
