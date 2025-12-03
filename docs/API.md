# 📋 API Documentation

## Base URL
```
Production: https://seu-app.onrender.com
```

## Authentication
Não requerida (API pública)

## Endpoints

### POST /upload
Upload de imagem para detecção de ônibus

**Request:**
```http
POST /upload
Content-Type: multipart/form-data

imagem: <arquivo>
parada_origem: A
parada_destino: B
```

**Response 201:**
```json
{
  "status": "success",
  "linha_detectada": "437",
  "nome_linha": "TI Caxangá (Conde da Boa Vista) - BRT",
  "timestamp": "2025-12-03T15:30:00Z"
}
```

**Response 200 (nenhum ônibus):**
```json
{
  "status": "not_found",
  "linha_detectada": "nenhum",
  "mensagem": "Nenhum ônibus válido detectado"
}
```

---

### POST /deteccao/manual
Registrar detecção manual

**Request:**
```json
{
  "linha": "437",
  "parada_origem": "A",
  "parada_destino": "B"
}
```

**Response 201:**
```json
{
  "status": "success",
  "deteccao_id": "a1b2c3d4",
  "linha": "437",
  "tempo_estimado_min": 5,
  "previsao_chegada": "2025-12-03T15:35:00Z",
  "posicao_fila": 1
}
```

---

### GET /previsoes/:parada_id
Consultar previsões para uma parada

**Request:**
```http
GET /previsoes/B
```

**Response 200:**
```json
{
  "parada": "B",
  "total": 3,
  "previsoes": [
    {
      "linha": "437",
      "nome": "TI Caxangá",
      "minutos": 2,
      "previsao_hora": "15:32"
    },
    {
      "linha": "2441",
      "nome": "TI CDU",
      "minutos": 5,
      "previsao_hora": "15:35"
    }
  ],
  "atualizado_em": "15:30:45"
}
```

---

### GET /linhas
Listar linhas conhecidas

**Response 200:**
```json
{
  "total": 4,
  "linhas": [
    {
      "linha": "437",
      "nome": "TI Caxangá (Conde da Boa Vista) - BRT",
      "tempo_medio_min": 5,
      "distancia_km": 2.5
    }
  ]
}
```

---

### GET /stats
Estatísticas do sistema

**Response 200:**
```json
{
  "total_deteccoes": 150,
  "em_rota": 5,
  "chegaram": 120,
  "expirados": 25,
  "top_linhas": [
    {"_id": "437", "count": 50}
  ]
}
```

## Rate Limiting
Não implementado (free tier Render)

## CORS
Habilitado para todos os origins