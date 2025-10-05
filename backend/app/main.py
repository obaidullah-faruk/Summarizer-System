from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.logging import logger
from app.api.v1.router import api_router
from app.database.db import create_db_and_tables
from app.database.deps import SessionDep

settings = get_settings()


@asynccontextmanager
async def lifespan(the_app):
    logger.info("Startup things")
    create_db_and_tables()
    yield
    logger.info("Shutdown things")


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_prefix)

# For prometheus
Instrumentator().instrument(app).expose(app)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.version
    }
