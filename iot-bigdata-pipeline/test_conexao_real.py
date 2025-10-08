import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def test_conexao_direta():
    try:
        print("🧪 TESTE DE CONEXÃO DIRETA...")
        
        # String de conexão DIRETA
        uri = "mongodb+srv://iot-user:IoT2024Secure@cluster0.wnfcroh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        
        client = MongoClient(
            uri,
            tls=True,
            serverSelectionTimeoutMS=10000
        )
        
        # Teste
        client.admin.command('ping')
        print("🎉 CONEXÃO BEM-SUCEDIDA!")
        
        # Testar escrita
        db = client["iot_database"]
        col = db["sensor_data"]
        
        test_data = {"test": True, "message": "Conexão funcionando!"}
        result = col.insert_one(test_data)
        print(f"✅ Escrita realizada! ID: {result.inserted_id}")
        
        count = col.count_documents({})
        print(f"📊 Total de documentos: {count}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ FALHA: {e}")
        return False

test_conexao_direta()
