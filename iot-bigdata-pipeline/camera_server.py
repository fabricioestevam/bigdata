"""
Servidor Flask para Receber IMAGENS da Webcam
Detecção de Ônibus com YOLOv8 + MongoDB
"""

from flask import Flask, request, jsonify
from datetime import datetime, timezone
from pymongo import MongoClient
from pathlib import Path
from dotenv import load_dotenv
import os
import sys
import cv2
import numpy as np
from ultralytics import YOLO

# ================================================
# Carregar .env
# ================================================
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

if not os.getenv("MONGO_URI"):
    print("❌ ERRO: MONGO_URI não carregou. Verifique o .env")
    sys.exit(1)

# ================================================
# Configurações
# ================================================
app = Flask(__name__)

# MongoDB
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
CAMERA_COLLECTION = "upload_imagens"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[CAMERA_COLLECTION]

# Modelo YOLOv8
model = YOLO("yolov8n.pt")  # versão leve, rápida
COCO_CLASSES = model.names  # lista de classes COCO

print("============================================")
print("🚀 Servidor rodando no Render + YOLOv8")
print(f"📦 Banco: {DB_NAME}")
print(f"📁 Coleção: {CAMERA_COLLECTION}")
print("============================================")

# ================================================
# Health Check
# ================================================
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "online",
        "service": "Webcam Upload Server",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

# ================================================
# Endpoint de Upload com detecção
# ================================================
@app.route("/upload", methods=["POST"])
def upload_image():
    try:
        if "imagem" not in request.files:
            return jsonify({"linha_detectada": "nenhum"}), 400

        file = request.files["imagem"]
        parada_origem = request.form.get("parada_origem", "A")
        parada_destino = request.form.get("parada_destino", "B")

        img_bytes = file.read()
        npimg = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        # =========================
        # Detectar ônibus com YOLO
        # =========================
        results = model(img)[0]
        linha_detectada = "nenhum"

        for det in results.boxes:
            cls_id = int(det.cls[0])
            if COCO_CLASSES[cls_id] == "bus":
                # Aqui você pode integrar OCR ou QR code para pegar a linha real
                linha_detectada = "407"  # exemplo fixo por enquanto
                break

        # =========================
        # Salvar no MongoDB
        # =========================
        doc = {
            "imagem_base64": img_bytes.hex(),
            "parada_origem": parada_origem,
            "parada_destino": parada_destino,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tamanho_bytes": len(img_bytes),
            "content_type": file.content_type,
            "nome_arquivo": file.filename,
            "fonte": "webcam",
            "linha_detectada": linha_detectada
        }

        result = collection.insert_one(doc)

        print("\n📸 Upload recebido!")
        print(f"🆔 ID: {result.inserted_id}")
        print(f"⬆ Tamanho: {len(img_bytes)} bytes")
        print(f"🚏 Origem: {parada_origem} | Destino: {parada_destino}")
        print(f"🚌 Linha detectada: {linha_detectada}")

        return jsonify({
            "status": "success",
            "message": "Imagem salva com sucesso",
            "id": str(result.inserted_id),
            "linha_detectada": linha_detectada
        }), 201

    except Exception as e:
        print(f"❌ ERRO no upload: {e}")
        return jsonify({"linha_detectada": "nenhum", "error": str(e)}), 500

# ================================================
# Listar todas as imagens
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
            "destino": d["parada_destino"],
            "linha_detectada": d.get("linha_detectada", "nenhum")
        })
    return jsonify(lista)

# ================================================
# Últimos uploads (para monitor)
# ================================================
@app.route("/ultimos", methods=["GET"])
def ultimos():
    docs = collection.find().sort("timestamp", -1).limit(10)
    resposta = []
    for d in docs:
        resposta.append({
            "id": str(d["_id"]),
            "origem": d.get("parada_origem", "?"),
            "destino": d.get("parada_destino", "?"),
            "timestamp": d.get("timestamp", ""),
            "linha_detectada": d.get("linha_detectada", "nenhum")
        })
    return jsonify(resposta)

# ================================================
# Main
# ================================================
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    print("\n🌐 Servidor Flask disponível!")
    app.run(host="0.0.0.0", port=PORT)
