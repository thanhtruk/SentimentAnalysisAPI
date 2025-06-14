from fastapi import APIRouter
from schemas.clause_split import ClauseResponse, ClauseRequest
from services.clause_split_service import process_text

router = APIRouter()


@router.post("/split", response_model=ClauseResponse)
def analyze_sentiment(req: ClauseRequest):
    all_clauses = process_text(req.text)
    return ClauseResponse(all_clauses=all_clauses)