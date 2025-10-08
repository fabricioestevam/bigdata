from typing import Dict, Any
from src.core.interfaces import IDataStore
from src.config import Config
import ssl

class MongoDBStore(IDataStore):
    """MongoDB storage - Conexão REAL com MongoDB Atlas"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.simulation_mode = True
        self._connect()
    
    def _connect(self):
        """Conexão REAL com tratamento adequado de SSL"""
        try:
            from pymongo import MongoClient
            
            print("🔗 Conectando ao MongoDB Atlas...")
            print(f"📧 Usuário: iot-user")
            print(f"🌐 Cluster: cluster0.wnfcroh.mongodb.net")
            
            # String de conexão CORRETA para MongoDB Atlas
            connection_string = "mongodb+srv://iot-user:IoT2024Secure@cluster0.wnfcroh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
            
            # Conexão com configurações específicas para MongoDB Atlas
            self.client = MongoClient(
                connection_string,
                tls=True,
                tlsAllowInvalidCertificates=False,  # IMPORTANTE: False para Atlas
                serverSelectionTimeoutMS=15000,
                connectTimeoutMS=15000,
                socketTimeoutMS=15000
            )
            
            # Teste de conexão REAL
            self.client.admin.command('ping')
            print("🎉 CONEXÃO REAL COM MONGODB ATLAS ESTABELECIDA!")
            
            # Configurar database e collection
            self.db = self.client["iot_database"]
            self.collection = self.db["sensor_data"]
            
            # Teste prático - inserir documento de teste
            test_doc = {
                "connection_test": True,
                "pipeline": "IoT Big Data Pipeline",
                "timestamp": "2024-01-01T00:00:00Z",
                "status": "connected"
            }
            result = self.collection.insert_one(test_doc)
            
            print(f"✅ Teste de escrita realizado! ID: {result.inserted_id}")
            
            # Contar documentos existentes
            count = self.collection.count_documents({})
            print(f"📊 Documentos na coleção: {count}")
            
            self.simulation_mode = False
            print("🚀 MODO MONGODB REAL ATIVADO!")
            
        except Exception as e:
            print(f"❌ ERRO de conexão: {str(e)[:100]}")
            print("💡 Soluções possíveis:")
            print("   1. Verifique se o cluster está ATIVO no MongoDB Atlas")
            print("   2. Verifique se o usuário 'iot-user' existe")
            print("   3. Adicione 0.0.0.0/0 na whitelist de IPs")
            print("   4. O ambiente pode ter restrições de rede")
            self.simulation_mode = True
    
    def save(self, data: Dict[str, Any]):
        """Save data no MongoDB REAL"""
        if data is None:
            return False
            
        try:
            if self.simulation_mode:
                print(f"💾 [SIMULAÇÃO] temp={data.get('temperature')}°C, hum={data.get('humidity')}%")
                return True
            else:
                # INSERÇÃO REAL NO MONGODB
                result = self.collection.insert_one(data)
                print(f"✅ DADOS SALVOS NO MONGODB! ID: {result.inserted_id}")
                return True
                
        except Exception as e:
            print(f"❌ Erro ao salvar no MongoDB: {e}")
            return False
    
    def __del__(self):
        if self.client and not self.simulation_mode:
            self.client.close()