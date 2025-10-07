from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class ISensor(ABC):
    @abstractmethod
    def read_data(self) -> Optional[Dict[str, Any]]:
        pass

class IDataCollector(ABC):
    @abstractmethod
    def collect(self) -> None:
        pass

class IDataProcessor(ABC):
    @abstractmethod
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

class IDataStore(ABC):
    @abstractmethod
    def save(self, data: Dict[str, Any]) -> None:
        pass
