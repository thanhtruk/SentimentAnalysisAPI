from fastapi import APIRouter
from schemas.sentiment import SentimentRequest, SentimentResponse
from models.sentiment_model import predict_sentiment

router = APIRouter()


@router.post("/predict", response_model=SentimentResponse)
def analyze_sentiment(req: SentimentRequest):
    sentiment, probability = predict_sentiment(req.text)
    return SentimentResponse(sentiment=sentiment, probability=probability)
