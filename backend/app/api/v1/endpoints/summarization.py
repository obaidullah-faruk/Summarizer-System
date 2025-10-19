from fastapi import APIRouter, Depends, Body
from app.services.ml_service import get_summary_ml_service, TextSummarizerService
from app.schemas.summarization import SummarizationResponse
from app.core.logging import logger
from app.utils.auth import get_current_user
from app.utils.hash import create_text_hash
from app.core.redis import get_redis_client
from redis.asyncio import Redis

router = APIRouter()


@router.post("/summarize", response_model=SummarizationResponse)
async def summarize_plain_text(text: str = Body(..., media_type="text/plain"),
                               redis_client: Redis = Depends(get_redis_client),
                               current_user_id: str = Depends(get_current_user),
                               text_ml_service: TextSummarizerService = Depends(get_summary_ml_service)):
    logger.info(f"Plain text summarization request received: {text}")
    hash = create_text_hash(text)
    summary_in_redis = await redis_client.get(hash)
    if summary_in_redis:
        logger.info(f"summary available in redis: {summary_in_redis}")
        return SummarizationResponse(summary=summary_in_redis, original_length=len(text), summary_length=len(summary_in_redis))
    summary = text_ml_service.summarize(text)
    logger.info(f"summary from model: {summary}")
    await redis_client.set(hash, summary, ex=3600)
    logger.info(f"summary stored in redis")
    return SummarizationResponse(summary=summary, original_length=len(text), summary_length=len(summary))
