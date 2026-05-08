import os
from dotenv import load_dotenv

load_dotenv()

AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_DEPLOYMENT: str = os.getenv("AZURE_OPENAI_DEPLOYMENT", "model-router")
AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
ALLOWED_ORIGINS: list[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
APP_ENV: str = os.getenv("APP_ENV", "development")
PORTAL_BASE_URL: str = os.getenv("PORTAL_BASE_URL", "https://skoportalempresarialcorporateangularig.azurewebsites.net")

if not AZURE_OPENAI_API_KEY:
    raise ValueError(
        "❌ AZURE_OPENAI_API_KEY no está configurada. "
        "Revisa tu archivo .env. Consulta .env.example para ver el formato correcto."
    )

if not AZURE_OPENAI_ENDPOINT:
    raise ValueError(
        "❌ AZURE_OPENAI_ENDPOINT no está configurada. "
        "Debe ser la URL de tu recurso Azure OpenAI, ej: https://mi-recurso.openai.azure.com/"
    )
