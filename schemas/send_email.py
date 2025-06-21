from pydantic import BaseModel


class EmailRequest(BaseModel):
    recipient_email: str
    message: str