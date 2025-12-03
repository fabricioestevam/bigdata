# 🚍 Sistema BRT Recife - API de Detecção

API REST para detecção e previsão de chegada de ônibus do BRT Recife.

## 🎯 Linhas Monitoradas
- **437**: TI Caxangá (Conde da Boa Vista)
- **2441**: TI CDU (Conde da Boa Vista)
- **2450**: TI Camaragibe (Conde da Boa Vista)
- **2444**: TI Getúlio Vargas (Conde da Boa Vista)

## 🚀 Tecnologias
- **YOLOv8** - Detecção de ônibus
- **EasyOCR** - Leitura de letreiros
- **Flask** - API REST
- **MongoDB Atlas** - Armazenamento
- **Render** - Deploy

## 📡 Endpoints

### `GET /health`
Status do servidor

### `POST /upload`
Upload de imagem para detecção
- Form Data: `imagem` (arquivo)
- Returns: `{"linha_detectada": "437"}`

### `POST /deteccao/manual`
Registrar detecção manual
- JSON: `{"linha": "437", "parada_origem": "A", "parada_destino": "B"}`

### `GET /previsoes/:parada_id`
Consultar previsões de chegada
- Returns: lista de ônibus em rota

### `GET /linhas`
Listar linhas conhecidas

### `GET /stats`
Estatísticas do sistema

## 🔧 Configuração

### Variáveis de Ambiente
```bash
MONGO_URI=mongodb+srv://...
DB_NAME=iot_database
PORT=5000
```

## 🚀 Deploy (Render)

1. Conectar repositório GitHub
2. Configurar variáveis de ambiente
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `python server.py`
5. Deploy!

## 📖 Documentação
Ver [docs/API.md](docs/API.md) para detalhes completos.

## 🤝 Contribuindo
Pull requests são bem-vindos!

## 📝 Licença
Projeto educacional - Big Data SENAC