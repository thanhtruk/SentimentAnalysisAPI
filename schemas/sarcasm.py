from pydantic import BaseModel


class SarcasmRequest(BaseModel):
    text: str


class SarcasmResponse(BaseModel):
    is_sarcasm: bool
    probability: float