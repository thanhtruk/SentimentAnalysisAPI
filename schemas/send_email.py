from pydantic import BaseModel


class EmailRequest(BaseModel):
    recipient_email: str
    subject: str
    message: str