from fastapi import APIRouter
from pydantic import BaseModel
from app.services.translate_service import translate_text

router = APIRouter()

class TranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str

@router.post("/translate-text")
def translate_text_endpoint(req: TranslationRequest):
    output = translate_text(req.text, req.source_lang, req.target_lang)
    return {"translatedText": output}
