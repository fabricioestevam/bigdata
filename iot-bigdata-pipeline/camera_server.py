"""
Servidor Flask para Receber IMAGENS da Webcam
Compatível com Render + MongoDB Atlas
"""

from flask import Flask, request, jsonify
from datetime import datetime, timezone
from pymongo import MongoClient
from pathlib import Path
from dotenv import load_dotenv
import os
import sys

# Carregar .env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

if not os.getenv("MONGO_URI"):
    print("❌ ERRO: MONGO_URI não carregou. Verifique o .env")
    sys.exit(1)

app = Flask(__name__)

# MongoDB
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
CAMERA_COLLECTION = "upload_imagens"   # Nova coleção para uploads

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[CAMERA_COLLECTION]

print("============================================")
print("🚀 Servidor rodando no Render")
print(f"📦 Banco: {DB_NAME}")
print(f"📁 Coleção: {CAMERA_COLLECTION}")
print("============================================")


# ================================================
#   HEALTH CHECK
# ================================================

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "online",
        "service": "Webcam Upload Server",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })


# ================================================
#   NOVO ENDPOINT: /upload
# ================================================

@app.route("/upload", methods=["POST"])
def upload_image():
    """
    Recebe imagem da webcam:
    
    POST /upload
    multipart/form-data:
        imagem = arquivo
        parada_origem = "A"
        parada_destino = "B"
    """
    
    try:
        if "imagem" not in request.files:
            return jsonify({"error": "Nenhuma imagem recebida"}), 400

        file = request.files["imagem"]
        parada_origem = request.form.get("parada_origem", "A")
        parada_destino = request.form.get("parada_destino", "B")

        # Ler arquivo como bytes
        img_bytes = file.read()

        doc = {
            "imagem_base64": img_bytes.hex(),   # armazenar seguro
            "parada_origem": parada_origem,
            "parada_destino": parada_destino,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tamanho_bytes": len(img_bytes),
            "content_type": file.content_type,
            "nome_arquivo": file.filename,
            "fonte": "webcam"
        }

        result = collection.insert_one(doc)

        print("\n📸 Upload recebido!")
        print(f"🆔 ID: {result.inserted_id}")
        print(f"⬆ Tamanho: {len(img_bytes)} bytes")
        print(f"🚏 Origem: {parada_origem} | Destino: {parada_destino}")

        return jsonify({
            "status": "success",
            "message": "Imagem salva com sucesso",
            "id": str(result.inserted_id)
        }), 201

    except Exception as e:
        print(f"❌ ERRO no upload: {e}")
        return jsonify({"error": str(e)}), 500


# ================================================
#   LISTAR IMAGENS
# ================================================
@app.route("/upload/list", methods=["GET"])
def list_images():
    docs = collection.find().sort("timestamp", -1)

    lista = []
    for d in docs:
        lista.append({
            "id": str(d["_id"]),
            "timestamp": d["timestamp"],
            "size_bytes": d["tamanho_bytes"],
            "origem": d["parada_origem"],
            "destino": d["parada_destino"]
        })

    return jsonify(lista)


# ================================================
#   MAIN
# ================================================
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    print("\n🌐 Servidor Flask disponível!")
    app.run(host="0.0.0.0", port=PORT)
