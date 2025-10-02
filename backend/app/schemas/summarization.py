from pydantic import BaseModel


class SummarizationResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int
