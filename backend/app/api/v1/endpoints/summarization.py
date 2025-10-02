from fastapi import APIRouter, Depends, Body
from app.services.ml_service import get_summary_ml_service, TextSummarizerService
from app.schemas.summarization import SummarizationResponse
from app.core.logging import logger

router = APIRouter()


@router.post("/summarize", response_model=SummarizationResponse)
async def summarize_plain_text(text: str = Body(..., media_type="text/plain"),
                               text_ml_service: TextSummarizerService = Depends(get_summary_ml_service)):
    logger.info(f"Plain text summarization request received, length: {len(text)}")

    summary = text_ml_service.summarize(text)
    logger.info(f"summary: {summary}")
    return SummarizationResponse(summary=summary, original_length=len(text), summary_length=len(summary))
