import os
from dotenv import load_dotenv
from pymongo import MongoClient
import ssl

load_dotenv()

def test_real_connection():
    try:
        mongo_uri = os.getenv("MONGO_URI")
        print("🔗 Testando conexão REAL com MongoDB...")
        
        client = MongoClient(
            mongo_uri,
            ssl=True,
            ssl_cert_reqs=ssl.CERT_NONE,
            serverSelectionTimeoutMS=10000
        )
        
        # Testar conexão
        client.admin.command('ping')
        print("🎉 CONEXÃO BEM-SUCEDIDA!")
        
        # Testar criar database e coleção
        db = client["iot_database"]
        collection = db["sensor_data"]
        
        # Testar inserção
        test_data = {
            "temperature": 25.5,
            "humidity": 60.0,
            "test": True,
            "message": "Teste de conexão"
        }
        
        result = collection.insert_one(test_data)
        print(f"✅ Dado inserido! ID: {result.inserted_id}")
        
        # Contar documentos
        count = collection.count_documents({})
        print(f"📊 Total de documentos na coleção: {count}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ FALHA: {e}")
        return False

if __name__ == "__main__":
    test_real_connection()
