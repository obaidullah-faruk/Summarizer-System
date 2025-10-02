from fastapi import APIRouter
from app.api.v1.endpoints import summarization

api_router = APIRouter()

api_router.include_router(
    summarization.router,
    prefix="/ml",
    tags=["Summarization Machine Learning"]
)