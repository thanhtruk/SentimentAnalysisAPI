from fastapi import APIRouter
from schemas.sarcasm import SarcasmResponse, SarcasmRequest
from services.sarcasm_service import predict_sarcasm

router = APIRouter()


@router.post("/predict", response_model=SarcasmResponse)
def analyze_sentiment(req: SarcasmRequest):
    is_sarcasm, probability = predict_sarcasm(req.text)
    return SarcasmResponse(is_sarcasm=is_sarcasm, probability=probability)