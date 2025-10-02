from functools import lru_cache
from time import time

from transformers import pipeline
import torch

from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()


class TextSummarizerService:
    def __init__(self):
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        logger.info(f"Initializing ML model on device: {self.device}")

        try:
            self.summarizer = pipeline("summarization", model=settings.summary_ml_model, device=self.device)
        except Exception as exp:
            logger.error(f"Failed to load ML model: {exp}")

    def summarize(self, text: str, max_length: int = None, min_length: int = None) -> str:
        start_time = time()
        status = "success"

        try:
            max_len = max_length or settings.summary_ml_max_length
            min_len = min_length or settings.summary_ml_min_length

            result = self.summarizer(
                text,
                max_length=max_len,
                min_length=min_len,
                do_sample=False
            )

            duration = time() - start_time
            logger.info(f"Summary model executed in: {duration}")
            return result[0]['summary_text']
        except Exception as exp:
            status = "error"
            logger.error(f"Summarization failed: {exp}")


@lru_cache
def get_summary_ml_service() -> TextSummarizerService:
    return TextSummarizerService()
