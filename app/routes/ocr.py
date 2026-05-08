import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.anthropic_service import call_claude
from app.prompts.ocr_prompt import OCR_SYSTEM_PROMPT

router = APIRouter()


class OCRRequest(BaseModel):
    document_text: str


class OCRResponse(BaseModel):
    extracted_data: dict
    summary: str
    status: str


@router.post("/ocr", response_model=OCRResponse)
def ocr(body: OCRRequest):
    if not body.document_text.strip():
        raise HTTPException(status_code=400, detail="El campo 'document_text' no puede estar vacío.")

    try:
        reply = call_claude(
            messages=[{"role": "user", "content": body.document_text}],
            system_prompt=OCR_SYSTEM_PROMPT,
            max_tokens=1200,
        )

        try:
            parsed = json.loads(reply)
            extracted_data = parsed.get("extracted_data", {})
            summary = parsed.get("summary", reply)
        except json.JSONDecodeError:
            # Si Claude no devuelve JSON puro, tratamos la respuesta como resumen
            extracted_data = {}
            summary = reply

        return OCRResponse(extracted_data=extracted_data, summary=summary, status="ok")

    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))
