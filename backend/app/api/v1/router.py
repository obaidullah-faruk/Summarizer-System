from fastapi import APIRouter
from app.api.v1.endpoints import summarization
from app.api.v1.endpoints import authentication

api_router = APIRouter()

api_router.include_router(
    summarization.router,
    prefix="/ml",
    tags=["Summarization Machine Learning"]
)

api_router.include_router(
    authentication.router,
    prefix="/auth",
    tags=["Authentication"]
)
