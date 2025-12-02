"""
Servidor Flask para ESP32-CAM
Conecta no SEU cluster MongoDB Atlas existente
"""

from flask import Flask, request, jsonify
from datetime import datetime, timezone
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Carregar configurações do seu .env existente
# Especificar caminho explícito do .env
import sys
from pathlib import Path

# Garantir que está na pasta correta
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Debug: verificar se carregou
if not os.getenv('MONGO_URI'):
    print("⚠️  AVISO: .env não foi carregado corretamente!")
    print(f"   Procurando em: {env_path}")
    print(f"   Arquivo existe: {env_path.exists()}")
    sys.exit(1)

app = Flask(__name__)

# Usar SUAS credenciais MongoDB que já estão no .env
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME')
CAMERA_COLLECTION = os.getenv('CAMERA_COLLECTION', 'camera_data')

print("🚀 Iniciando Servidor ESP32-CAM...")
print("=" * 60)
print("🔗 Conectando ao SEU MongoDB Atlas...")

# Conectar no SEU cluster MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[CAMERA_COLLECTION]
    
    # Testar conexão
    client.admin.command('ping')
    print("✅ CONECTADO ao seu cluster existente!")
    print(f"📊 Database: {DB_NAME}")
    print(f"📹 Collection: {CAMERA_COLLECTION}")
    print("=" * 60)
except Exception as e:
    print(f"❌ Erro ao conectar: {e}")
    print("💡 Verifique suas credenciais no arquivo .env")
    print("=" * 60)


@app.route('/health', methods=['GET'])
def health():
    """Verificar se servidor está online"""
    try:
        # Testar conexão MongoDB
        client.admin.command('ping')
        mongodb_status = 'connected'
    except:
        mongodb_status = 'disconnected'
    
    return jsonify({
        'status': 'online',
        'service': 'ESP32-CAM Pipeline Server',
        'database': DB_NAME,
        'collection': CAMERA_COLLECTION,
        'mongodb': mongodb_status,
        'timestamp': datetime.now(timezone.utc).isoformat()
    })


@app.route('/camera/data', methods=['POST'])
def receive_camera_data():
    """
    Receber dados do ESP32-CAM e salvar no MongoDB
    
    Payload esperado:
    {
        "device_id": "AA:BB:CC:DD:EE:FF",
        "device_type": "ESP32-CAM",
        "ip_address": "192.168.1.50",
        "metrics": {
            "uptime_seconds": 120,
            "free_heap": 180000,
            "wifi_rssi": -52
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Nenhum dado recebido'}), 400
        
        device_id = data.get('device_id', 'unknown')
        metrics = data.get('metrics', {})
        
        # Log de recebimento
        print(f"\n📥 Dados recebidos da câmera: {device_id}")
        print(f"   📍 IP: {data.get('ip_address')}")
        print(f"   ⏱️  Uptime: {metrics.get('uptime_seconds')}s")
        print(f"   💾 Heap Livre: {metrics.get('free_heap')} bytes")
        print(f"   📶 WiFi RSSI: {metrics.get('wifi_rssi')} dBm")
        
        # Adicionar timestamp se não existir
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now(timezone.utc).isoformat()
        
        # Validação e análise dos dados
        free_heap = metrics.get('free_heap', 0)
        if free_heap < 50000:
            data['memory_status'] = 'critical'
            data['memory_alert'] = True
        elif free_heap < 100000:
            data['memory_status'] = 'warning'
            data['memory_alert'] = False
        else:
            data['memory_status'] = 'healthy'
            data['memory_alert'] = False
        
        # Validação de WiFi (RSSI em dBm)
        rssi = metrics.get('wifi_rssi', -100)
        if rssi > -50:
            data['wifi_status'] = 'excellent'
        elif rssi > -60:
            data['wifi_status'] = 'good'
        elif rssi > -70:
            data['wifi_status'] = 'fair'
        else:
            data['wifi_status'] = 'poor'
        
        # Marcar como processado
        data['cleaned'] = True
        data['processed_at'] = datetime.now(timezone.utc).isoformat()
        
        # Salvar no MongoDB
        result = collection.insert_one(data)
        
        # Log de sucesso
        print(f"✅ Dados salvos no MongoDB!")
        print(f"   📦 ID: {result.inserted_id}")
        print(f"   💾 Status Memória: {data['memory_status']}")
        print(f"   📶 Status WiFi: {data['wifi_status']}")
        
        return jsonify({
            'status': 'success',
            'message': 'Dados salvos com sucesso',
            'document_id': str(result.inserted_id),
            'memory_status': data['memory_status'],
            'wifi_status': data['wifi_status']
        }), 201
        
    except Exception as e:
        print(f"❌ Erro ao processar dados: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/camera/stats', methods=['GET'])
def get_stats():
    """
    Ver estatísticas dos dados salvos
    
    Exemplo: http://localhost:5000/camera/stats
    Ou com filtro: http://localhost:5000/camera/stats?device_id=AA:BB:CC:DD:EE:FF
    """
    try:
        device_id = request.args.get('device_id')
        
        # Filtrar por device_id se fornecido
        query = {'device_id': device_id} if device_id else {}
        
        # Contar documentos
        total = collection.count_documents(query)
        
        # Buscar último documento
        latest = collection.find_one(query, sort=[('timestamp', -1)])
        
        # Contar alertas de memória
        memory_alerts = collection.count_documents({
            **query,
            'memory_alert': True
        })
        
        # Estatísticas de WiFi
        wifi_poor = collection.count_documents({
            **query,
            'wifi_status': 'poor'
        })
        
        return jsonify({
            'total_documentos': total,
            'memory_alerts': memory_alerts,
            'wifi_poor_count': wifi_poor,
            'ultimo_envio': latest.get('timestamp') if latest else None,
            'ultimo_device': latest.get('device_id') if latest else None,
            'collection': CAMERA_COLLECTION
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/camera/latest', methods=['GET'])
def get_latest():
    """
    Buscar dados mais recentes
    
    Exemplo: http://localhost:5000/camera/latest
    """
    try:
        device_id = request.args.get('device_id')
        query = {'device_id': device_id} if device_id else {}
        
        latest = collection.find_one(query, sort=[('timestamp', -1)])
        
        if not latest:
            return jsonify({
                'message': 'Nenhum dado encontrado',
                'query': query
            }), 404
        
        # Converter ObjectId para string
        latest['_id'] = str(latest['_id'])
        
        return jsonify({
            'status': 'success',
            'data': latest
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/camera/list', methods=['GET'])
def list_devices():
    """
    Listar todos os dispositivos únicos
    
    Exemplo: http://localhost:5000/camera/list
    """
    try:
        # Buscar todos os device_ids únicos
        devices = collection.distinct('device_id')
        
        # Para cada dispositivo, buscar último registro
        devices_info = []
        for device in devices:
            latest = collection.find_one(
                {'device_id': device},
                sort=[('timestamp', -1)]
            )
            
            if latest:
                devices_info.append({
                    'device_id': device,
                    'ip_address': latest.get('ip_address'),
                    'last_seen': latest.get('timestamp'),
                    'memory_status': latest.get('memory_status'),
                    'wifi_status': latest.get('wifi_status')
                })
        
        return jsonify({
            'total_devices': len(devices),
            'devices': devices_info
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🎥 ESP32-CAM Pipeline Server - RODANDO NO RENDER!")
    print("=" * 60)

    PORT = int(os.environ.get("PORT", 5000))

    app.run(host='0.0.0.0', port=PORT)
