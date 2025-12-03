"""
Servidor Flask para Render - Sistema BRT Recife
YOLOv8 + EasyOCR + MongoDB Atlas

Repositório: github.com/fabricioestevam/bigdata
Deploy: render.com
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta, timezone
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import sys
import cv2
import numpy as np
from ultralytics import YOLO
import uuid

# OCR
try:
    import easyocr
    OCR_AVAILABLE = True
    reader = easyocr.Reader(['pt', 'en'], gpu=False)
    print("✅ EasyOCR carregado")
except ImportError:
    OCR_AVAILABLE = False
    print("⚠️  EasyOCR não disponível")

# ================================================
# CONFIGURAÇÕES
# ================================================
load_dotenv()

app = Flask(__name__)
CORS(app)  # Permitir requisições do Netlify

# MongoDB
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "iot_database")

if not MONGO_URI:
    print("❌ ERRO: MONGO_URI não configurado!")
    sys.exit(1)

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
deteccoes_collection = db["deteccoes"]
logs_collection = db["logs_sistema"]
linhas_collection = db["linhas_conhecidas"]

# YOLOv8
print("📦 Carregando modelo YOLOv8...")
model = YOLO("yolov8n.pt")
print("✅ YOLOv8 carregado")

# Linhas conhecidas do BRT Recife
LINHAS_CONHECIDAS = {
    "437": {
        "nome": "TI Caxangá (Conde da Boa Vista) - BRT",
        "tempo_medio_min": 5,
        "distancia_km": 2.5
    },
    "2441": {
        "nome": "TI CDU (Conde da Boa Vista) - BRT",
        "tempo_medio_min": 5,
        "distancia_km": 2.5
    },
    "2450": {
        "nome": "TI Camaragibe (Conde da Boa Vista) - BRT",
        "tempo_medio_min": 5,
        "distancia_km": 2.5
    },
    "2444": {
        "nome": "TI Getúlio Vargas (Conde da Boa Vista) - BRT",
        "tempo_medio_min": 5,
        "distancia_km": 2.5
    }
}

print("\n" + "=" * 70)
print("🚍 SERVIDOR BRT RECIFE - RENDER.COM")
print("=" * 70)
print(f"📦 Database: {DB_NAME}")
print(f"🔍 OCR: {'✅ Ativo' if OCR_AVAILABLE else '❌ Inativo'}")
print(f"🚌 Linhas: {len(LINHAS_CONHECIDAS)}")
print("=" * 70 + "\n")


# ================================================
# FUNÇÕES AUXILIARES
# ================================================

def gerar_id_deteccao():
    """Gera ID único para cada detecção"""
    return str(uuid.uuid4())[:8]


def salvar_log(tipo, mensagem, detalhes=None):
    """Salva log no MongoDB"""
    try:
        log = {
            "tipo": tipo,
            "mensagem": mensagem,
            "detalhes": detalhes,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        logs_collection.insert_one(log)
    except:
        pass


def limpar_deteccoes_antigas():
    """Remove detecções com mais de 30 minutos"""
    limite = datetime.now(timezone.utc) - timedelta(minutes=30)
    deteccoes_collection.delete_many({
        "hora_deteccao": {"$lt": limite.isoformat()}
    })


# ================================================
# YOLO + OCR: DETECÇÃO DE LINHA
# ================================================

def detectar_linha_onibus(img):
    """
    1. YOLO detecta ônibus na imagem
    2. Recorta região do letreiro (parte superior)
    3. EasyOCR lê o número
    4. Valida se é linha conhecida
    
    Returns:
        str ou None: Número da linha detectada
    """
    if not OCR_AVAILABLE:
        print("⚠️  OCR não disponível")
        return None
    
    try:
        # Detectar objetos com YOLO
        results = model(img, conf=0.5)[0]  # Confiança mínima 50%
        
        for det in results.boxes:
            cls_id = int(det.cls[0])
            class_name = model.names[cls_id]
            
            # Se detectou ônibus (class 5 no COCO é "bus")
            if class_name == "bus":
                confidence = float(det.conf[0])
                print(f"🚌 Ônibus detectado (confiança: {confidence:.2f})")
                
                # Pegar coordenadas da bounding box
                x1, y1, x2, y2 = map(int, det.xyxy[0])
                
                # Recortar região do ônibus
                onibus_crop = img[y1:y2, x1:x2]
                
                if onibus_crop.size == 0:
                    continue
                
                # Focar na parte superior do ônibus (letreiro)
                altura = onibus_crop.shape[0]
                letreiro_crop = onibus_crop[0:int(altura*0.35), :]
                
                # Pré-processamento para melhorar OCR
                gray = cv2.cvtColor(letreiro_crop, cv2.COLOR_BGR2GRAY)
                
                # Aumentar contraste
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                enhanced = clahe.apply(gray)
                
                # Threshold adaptativo
                thresh = cv2.adaptiveThreshold(
                    enhanced, 255, 
                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                    cv2.THRESH_BINARY, 
                    11, 2
                )
                
                # OCR
                print("🔍 Executando OCR...")
                ocr_results = reader.readtext(thresh)
                
                # Procurar linhas válidas no texto detectado
                for (bbox, text, conf_ocr) in ocr_results:
                    # Extrair apenas números do texto
                    numeros = ''.join(filter(str.isdigit, text))
                    
                    print(f"   OCR leu: '{text}' → '{numeros}' (conf: {conf_ocr:.2f})")
                    
                    # Verificar se é uma linha conhecida
                    if numeros in LINHAS_CONHECIDAS and conf_ocr > 0.4:
                        print(f"✅ LINHA {numeros} IDENTIFICADA!")
                        return numeros
        
        print("ℹ️  Nenhuma linha válida detectada")
        return None
        
    except Exception as e:
        print(f"❌ Erro na detecção: {e}")
        salvar_log("erro", "Erro na detecção YOLO+OCR", {"erro": str(e)})
        return None


# ================================================
# ENDPOINTS
# ================================================

@app.route("/", methods=["GET"])
def home():
    """Página inicial"""
    return jsonify({
        "service": "BRT Recife Detection API",
        "version": "1.0",
        "endpoints": {
            "GET /health": "Status do servidor",
            "POST /upload": "Upload de imagem para detecção",
            "POST /deteccao/manual": "Registrar detecção manual",
            "GET /previsoes/<parada>": "Consultar previsões",
            "GET /linhas": "Listar linhas conhecidas",
            "GET /stats": "Estatísticas do sistema"
        }
    })


@app.route("/health", methods=["GET"])
def health():
    """Health check"""
    return jsonify({
        "status": "online",
        "service": "BRT Detection Server",
        "yolo": "active",
        "ocr": "active" if OCR_AVAILABLE else "inactive",
        "mongodb": "connected",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })


@app.route("/upload", methods=["POST"])
def upload_image():
    """
    Recebe imagem da webcam e detecta linha do ônibus
    
    Form Data:
        imagem: arquivo de imagem
        parada_origem: string (default "A")
        parada_destino: string (default "B")
    """
    try:
        if "imagem" not in request.files:
            return jsonify({"error": "Imagem não enviada"}), 400
        
        file = request.files["imagem"]
        parada_origem = request.form.get("parada_origem", "A")
        parada_destino = request.form.get("parada_destino", "B")
        
        # Ler imagem
        img_bytes = file.read()
        npimg = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({"error": "Imagem inválida"}), 400
        
        print(f"\n{'='*70}")
        print(f"📸 Nova imagem recebida ({len(img_bytes)} bytes)")
        print(f"{'='*70}")
        
        # Detectar linha com YOLO + OCR
        linha_detectada = detectar_linha_onibus(img)
        
        if linha_detectada:
            print(f"🎉 Linha {linha_detectada} detectada com sucesso!")
            
            return jsonify({
                "status": "success",
                "linha_detectada": linha_detectada,
                "nome_linha": LINHAS_CONHECIDAS[linha_detectada]["nome"],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }), 201
        else:
            print("ℹ️  Nenhum ônibus válido detectado")
            
            return jsonify({
                "status": "not_found",
                "linha_detectada": "nenhum",
                "mensagem": "Nenhum ônibus válido detectado"
            }), 200
        
    except Exception as e:
        print(f"❌ Erro no upload: {e}")
        salvar_log("erro", "Erro no endpoint /upload", {"erro": str(e)})
        return jsonify({"error": str(e)}), 500


@app.route("/deteccao/manual", methods=["POST"])
def deteccao_manual():
    """
    Registra detecção manual no sistema de fila
    
    JSON Body:
    {
        "linha": "437",
        "parada_origem": "A",
        "parada_destino": "B"
    }
    """
    try:
        data = request.get_json()
        
        linha = data.get("linha")
        parada_origem = data.get("parada_origem", "A")
        parada_destino = data.get("parada_destino", "B")
        
        if not linha:
            return jsonify({"error": "Linha não informada"}), 400
        
        if linha not in LINHAS_CONHECIDAS:
            return jsonify({
                "error": f"Linha {linha} não cadastrada",
                "linhas_validas": list(LINHAS_CONHECIDAS.keys())
            }), 404
        
        # Limpar detecções antigas
        limpar_deteccoes_antigas()
        
        # Gerar ID único
        deteccao_id = gerar_id_deteccao()
        
        # Calcular previsão
        linha_info = LINHAS_CONHECIDAS[linha]
        tempo_min = linha_info["tempo_medio_min"]
        
        agora = datetime.now(timezone.utc)
        previsao_chegada = agora + timedelta(minutes=tempo_min)
        
        # Salvar detecção
        deteccao = {
            "deteccao_id": deteccao_id,
            "linha": linha,
            "nome_linha": linha_info["nome"],
            "parada_origem": parada_origem,
            "parada_destino": parada_destino,
            "hora_deteccao": agora.isoformat(),
            "previsao_chegada": previsao_chegada.isoformat(),
            "tempo_estimado_min": tempo_min,
            "distancia_km": linha_info["distancia_km"],
            "status": "em_rota",
            "fonte": "deteccao_automatica"
        }
        
        result = deteccoes_collection.insert_one(deteccao)
        
        # Contar posição na fila
        posicao = deteccoes_collection.count_documents({
            "parada_destino": parada_destino,
            "status": "em_rota",
            "hora_deteccao": {"$lte": agora.isoformat()}
        })
        
        print(f"✅ Detecção registrada: Linha {linha} (posição {posicao})")
        
        salvar_log("deteccao", f"Ônibus {linha} detectado", {"deteccao_id": deteccao_id})
        
        return jsonify({
            "status": "success",
            "deteccao_id": deteccao_id,
            "linha": linha,
            "nome_linha": linha_info["nome"],
            "tempo_estimado_min": tempo_min,
            "previsao_chegada": previsao_chegada.isoformat(),
            "posicao_fila": posicao,
            "mongodb_id": str(result.inserted_id)
        }), 201
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/previsoes/<parada_id>", methods=["GET"])
def get_previsoes(parada_id):
    """
    Consulta previsões de chegada para uma parada
    Para o display mostrar a fila de ônibus
    
    Exemplo: GET /previsoes/B
    """
    try:
        agora = datetime.now(timezone.utc)
        
        # Buscar detecções ativas
        deteccoes = deteccoes_collection.find({
            "parada_destino": parada_id,
            "status": "em_rota"
        }).sort("previsao_chegada", 1)
        
        previsoes = []
        
        for det in deteccoes:
            previsao_dt = datetime.fromisoformat(det["previsao_chegada"])
            minutos_restantes = int((previsao_dt - agora).total_seconds() / 60)
            
            # Incluir até 1 minuto atrasado
            if minutos_restantes >= -1:
                previsoes.append({
                    "deteccao_id": det["deteccao_id"],
                    "linha": det["linha"],
                    "nome": det["nome_linha"],
                    "minutos": max(0, minutos_restantes),
                    "previsao_hora": previsao_dt.strftime("%H:%M"),
                    "status": "chegando" if minutos_restantes <= 0 else "em_rota"
                })
            else:
                # Marcar como expirado
                deteccoes_collection.update_one(
                    {"_id": det["_id"]},
                    {"$set": {"status": "expirado"}}
                )
        
        return jsonify({
            "parada": parada_id,
            "total": len(previsoes),
            "previsoes": previsoes[:10],  # Máximo 10
            "atualizado_em": agora.strftime("%H:%M:%S")
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/linhas", methods=["GET"])
def listar_linhas():
    """Lista todas as linhas conhecidas"""
    linhas = []
    for numero, info in LINHAS_CONHECIDAS.items():
        linhas.append({
            "linha": numero,
            "nome": info["nome"],
            "tempo_medio_min": info["tempo_medio_min"],
            "distancia_km": info["distancia_km"]
        })
    
    return jsonify({
        "total": len(linhas),
        "linhas": linhas
    })


@app.route("/stats", methods=["GET"])
def estatisticas():
    """Estatísticas do sistema"""
    try:
        total = deteccoes_collection.count_documents({})
        em_rota = deteccoes_collection.count_documents({"status": "em_rota"})
        chegaram = deteccoes_collection.count_documents({"status": "chegou"})
        
        # Top linhas
        pipeline = [
            {"$group": {"_id": "$linha", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]
        top_linhas = list(deteccoes_collection.aggregate(pipeline))
        
        return jsonify({
            "total_deteccoes": total,
            "em_rota": em_rota,
            "chegaram": chegaram,
            "expirados": total - em_rota - chegaram,
            "top_linhas": top_linhas,
            "linhas_cadastradas": len(LINHAS_CONHECIDAS)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================================================
# MAIN
# ================================================
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT, debug=False)