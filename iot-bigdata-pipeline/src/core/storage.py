from pymongo import MongoClient
from typing import Dict, Any
from src.config import MONGO_CONNECTION, DATABASE_NAME, COLLECTION_NAME
from .interfaces import IDataStore

class MongoDBStore(IDataStore):
    def __init__(self):
        self.client = MongoClient(MONGO_CONNECTION)
        self.db = self.client[DATABASE_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def save(self, data: Dict[str, Any]):
        self.collection.insert_one(data)
