from fastapi import FastAPI
from api import sentiment, sarcasm, field_classify, clause_split, send_email, extract_sentiment_words

app = FastAPI(title="NLP API")

# Đăng ký router
app.include_router(sentiment.router, prefix="/sentiment", tags=["Sentiment"])
app.include_router(sarcasm.router, prefix="/sarcasm", tags=["Sarcasm"])
app.include_router(field_classify.router, prefix="/field", tags=["Field Classification"])
app.include_router(clause_split.router, prefix="/clause", tags=["Clause"])
app.include_router(extract_sentiment_words.router, prefix="/extract", tags=["Sentiment Words"])
app.include_router(send_email.router)
