# SkanIA API — Skandia Colombia Hackathon

Backend centralizado en FastAPI que expone los tres módulos de IA del equipo.

## Estructura

```
app/
├── main.py                  → FastAPI + CORS
├── config.py                → Variables de entorno
├── routes/
│   ├── chat.py              → POST /api/chat
│   ├── recommendation.py    → POST /api/recommendation
│   └── ocr.py               → POST /api/ocr
├── services/
│   └── anthropic_service.py → Llama a la API de Claude
└── prompts/
    ├── chat_prompt.py
    ├── recommendation_prompt.py
    └── ocr_prompt.py
```

## Configuración inicial

### 1. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Copia `.env.example` a `.env` y reemplaza la API Key:

```bash
cp .env.example .env
```

Edita `.env`:
```
ANTHROPIC_API_KEY=sk-ant-TU_CLAVE_REAL_AQUI
ALLOWED_ORIGINS=http://localhost:5173
APP_ENV=development
```

### 3. Levantar el servidor

```bash
uvicorn app.main:app --reload --port 8000
```

El servidor queda disponible en `http://localhost:8000`.  
Documentación interactiva: `http://localhost:8000/docs`

---

## Endpoints

### Health check
```
GET /
→ { "status": "ok", "app": "SkanIA" }
```

### Módulo 1 — Chatbot
```
POST /api/chat
Body: { "messages": [{"role": "user", "content": "¿Qué es la pensión voluntaria?"}] }
```

### Módulo 2 — Recomendación
```
POST /api/recommendation
Body: {
  "client_profile": {
    "age": 35,
    "products": ["Cesantías"],
    "query": "¿Qué producto me conviene para ahorrar?"
  }
}
```

### Módulo 3 — OCR / Documentos
```
POST /api/ocr
Body: { "document_text": "Texto extraído del documento..." }
```

---

## Notas de seguridad

- El archivo `.env` está en `.gitignore`. **Nunca subas tu API Key al repositorio.**
- El frontend solo hace peticiones a `http://localhost:8000`; la API Key vive exclusivamente en el backend.
