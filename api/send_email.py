from http.client import HTTPException

from fastapi import APIRouter
from schemas.send_email import EmailRequest
from services.send_email_service import send_email

router = APIRouter()


@router.post("/send-email")
def send_email_api(request: EmailRequest):
    result = send_email(request.recipient_email, request.message)
    if result["status"] == "error":
        raise HTTPException()
    return result
