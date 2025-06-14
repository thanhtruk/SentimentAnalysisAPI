from pydantic import BaseModel


class ClauseRequest(BaseModel):
    text: str


class ClauseResponse(BaseModel):
    all_clauses: list
