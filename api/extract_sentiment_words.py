from fastapi import APIRouter
from schemas.extract_sentiment_words import ExtractWordResponse, ExtractWordRequest
from services.extract_sentiment_words import extract_adj

router = APIRouter()


@router.post("/keyword", response_model = ExtractWordResponse)
def analyze_sentiment(req: ExtractWordRequest):
    words_count = extract_adj(req.text)
    return ExtractWordResponse(words_count = words_count)