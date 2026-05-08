from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal

from app.services.anthropic_service import call_claude
from app.prompts.chat_prompt import get_chat_prompt
from app.config import PORTAL_BASE_URL

router = APIRouter()


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]
    session_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    status: str


@router.post("/chat", response_model=ChatResponse)
def chat(body: ChatRequest):
    if not body.messages:
        raise HTTPException(status_code=400, detail="El campo 'messages' no puede estar vacío.")

    try:
        reply = call_claude(
            messages=[m.model_dump() for m in body.messages],
            system_prompt=get_chat_prompt(PORTAL_BASE_URL),
            max_tokens=600,
        )
        return ChatResponse(response=reply, status="ok")

    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))
