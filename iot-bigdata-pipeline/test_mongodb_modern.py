import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

def test_modern_connection():
    try:
        mongo_uri = os.getenv("MONGO_URI")
        print("🔗 Testando conexão MONGODB (versão moderna)...")
        print(f"📧 Usuário: iot-user")
        print(f"🌐 Cluster: cluster0.wnfcroh.mongodb.net")
        
        # Conexão moderna - sem opções SSL complexas
        client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000
        )
        
        # Testar conexão
        client.admin.command('ping')
        print("🎉 CONEXÃO BEM-SUCEDIDA!")
        
        # Testar database
        db = client["iot_database"]
        collection = db["sensor_data"]
        
        # Inserir teste
        test_data = {
            "temperature": 25.5,
            "humidity": 60.0,
            "test": True,
            "message": "Teste de conexão funcionando!",
            "timestamp": "2024-01-01T10:00:00"
        }
        
        result = collection.insert_one(test_data)
        print(f"✅ Dado inserido! ID: {result.inserted_id}")
        
        # Contar documentos
        count = collection.count_documents({})
        print(f"📊 Total de documentos: {count}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ FALHA: {e}")
        print("\n💡 Possíveis soluções:")
        print("1. Verifique se o usuário 'iot-user' existe no MongoDB Atlas")
        print("2. Verifique se a senha está correta")
        print("3. Verifique se o IP 0.0.0.0/0 está na whitelist")
        print("4. O cluster pode estar pausado")
        return False

if __name__ == "__main__":
    test_modern_connection()
