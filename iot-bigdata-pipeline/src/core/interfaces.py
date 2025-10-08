from abc import ABC, abstractmethod
from typing import Dict, Any

class ISensor(ABC):
    """Interface for sensors following Interface Segregation Principle"""
    
    @abstractmethod
    def read_data(self) -> Dict[str, Any]:
        pass

class IDataCleaner(ABC):
    """Interface for data cleaning strategies"""
    
    @abstractmethod
    def clean(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

class IDataStore(ABC):
    """Interface for data storage following Open/Closed Principle"""
    
    @abstractmethod
    def save(self, data: Dict[str, Any]):
        pass