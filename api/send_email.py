from fastapi import HTTPException

from fastapi import APIRouter
from schemas.send_email import EmailRequest
from services.send_email_service import send_email

router = APIRouter()


@router.post("/send-email")
def send_email_api(request: EmailRequest):
    try:
        result = send_email(request.recipient_email, request.subject, request.message)

        if result["status"] == "error":
            raise Exception(result["detail"])

        return result

    except Exception as e:
        print(f"Lỗi nội bộ khi gửi email: {e}")
        raise HTTPException(status_code=500, detail=str(e))
