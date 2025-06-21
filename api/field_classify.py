from fastapi import APIRouter
from schemas.field_classify import FieldRequest, FieldResponse
from services.field_classify_service import detect_fields_in_text

router = APIRouter()


@router.post("/detect", response_model=FieldResponse)
def analyze_sentiment(req: FieldRequest):
    field, field_detail = detect_fields_in_text(req.text)
    return FieldResponse(field=field, field_detail=field_detail)
