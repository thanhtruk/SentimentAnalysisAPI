from pydantic import BaseModel


class SarcasmRequest(BaseModel):
    text: str


class SarcasmResponse(BaseModel):
    is_sarcasm: str
    probability: float