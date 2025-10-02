from contextlib import asynccontextmanager

from fastapi import FastAPI, Body
from transformers import pipeline
import torch

from app.core.config import get_settings
from app.core.logging import logger
from app.api.v1.router import api_router

settings = get_settings()


@asynccontextmanager
async def lifespan(the_app):
    logger.info("Startup things")
    yield
    logger.info("Shutdown things")


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.include_router(api_router, prefix=settings.API_V1_prefix)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.version
    }
