from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import ALLOWED_ORIGINS
from app.routes import chat, recommendation, ocr

app = FastAPI(
    title="SkanIA API - Skandia Colombia",
    description="Backend centralizado para los módulos de IA del equipo Skandia Hackathon",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api")
app.include_router(recommendation.router, prefix="/api")
app.include_router(ocr.router, prefix="/api")


@app.get("/")
def health_check():
    return {"status": "ok", "app": "SkanIA"}
