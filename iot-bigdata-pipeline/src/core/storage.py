from pymongo import MongoClient
from typing import Dict, Any
from src.core.interfaces import IDataStore
from src.config import Config

class MongoDBStore(IDataStore):
    """MongoDB storage implementation following Dependency Inversion Principle"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self._connect()
    
    def _connect(self):
        """Establish connection to MongoDB"""
        try:
            self.client = MongoClient(Config.MONGO_CONNECTION)
            self.db = self.client[Config.DATABASE_NAME]
            self.collection = self.db[Config.COLLECTION_NAME]
            
            # Test connection
            self.client.admin.command('ping')
            print("✅ Conectado ao MongoDB Atlas com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao conectar com MongoDB: {e}")
            raise
    
    def save(self, data: Dict[str, Any]):
        """Save data to MongoDB with error handling"""
        if data is None:  # Skip invalid data
            return False
            
        try:
            result = self.collection.insert_one(data)
            print(f"✅ Dados armazenados com ID: {result.inserted_id}")
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar dados: {e}")
            return False
    
    def __del__(self):
        """Ensure proper connection cleanup"""
        if self.client:
            self.client.close()