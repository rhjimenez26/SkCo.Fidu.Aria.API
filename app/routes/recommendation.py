import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.anthropic_service import call_claude
from app.prompts.recommendation_prompt import RECOMMENDATION_SYSTEM_PROMPT

router = APIRouter()


class ClientProfile(BaseModel):
    age: int
    products: list[str] = []
    query: str


class RecommendationRequest(BaseModel):
    client_profile: ClientProfile


class RecommendationResponse(BaseModel):
    recommendation: str
    products: list[str]
    status: str


@router.post("/recommendation", response_model=RecommendationResponse)
def recommendation(body: RecommendationRequest):
    profile = body.client_profile
    user_message = (
        f"Perfil del cliente:\n"
        f"- Edad: {profile.age} años\n"
        f"- Productos actuales: {', '.join(profile.products) if profile.products else 'Ninguno'}\n"
        f"- Consulta: {profile.query}"
    )

    try:
        reply = call_claude(
            messages=[{"role": "user", "content": user_message}],
            system_prompt=RECOMMENDATION_SYSTEM_PROMPT,
            max_tokens=800,
        )

        # Intentar extraer lista de productos mencionados en la respuesta
        recommended_products = [
            p for p in ["Cesantías", "Pensión Voluntaria", "Seguros de Vida", "Fondos de Inversión"]
            if p.lower() in reply.lower()
        ]

        return RecommendationResponse(
            recommendation=reply,
            products=recommended_products,
            status="ok",
        )

    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))
