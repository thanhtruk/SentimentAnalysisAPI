from typing import Dict

from pydantic import BaseModel


class ExtractWordRequest(BaseModel):
    text: str


class ExtractWordResponse(BaseModel):
    words_count: Dict[str, int]