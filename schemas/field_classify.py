from pydantic import BaseModel


class FieldRequest(BaseModel):
    text: str


class FieldResponse(BaseModel):
    field: str
    field_detail: list
