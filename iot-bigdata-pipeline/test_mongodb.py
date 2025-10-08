import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

def test_connection():
    try:
        # Obter string de conexão do .env
        mongo_uri = os.getenv("MONGO_URI")
        print(f"🔗 Tentando conectar: {mongo_uri.split('@')[1]}")
        
        # Conectar ao MongoDB
        client = MongoClient(mongo_uri)
        
        # Testar conexão
        client.admin.command('ping')
        print("✅ Conexão com MongoDB Atlas bem-sucedida!")
        
        # Listar bancos de dados
        dbs = client.list_database_names()
        print(f"📊 Bancos disponíveis: {dbs}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

if __name__ == "__main__":
    test_connection()
