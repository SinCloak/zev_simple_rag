"""
Zev Simple RAG AI Agent - FastAPI Backend
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from structlog import get_logger

from src.api.dependencies import get_rag_service
from src.api.v1 import chat, sessions
from src.core.config import settings
from src.core.logging import configure_logging
from src.infrastructure.database.models import Base
from src.infrastructure.database.session import engine

logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    FastAPI lifespan manager for startup and shutdown events.
    """
    # Startup
    configure_logging(settings.debug)
    logger.info("Starting application", app_name=settings.app_name, version=settings.app_version)

    # Initialize database tables
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables initialized")
    except Exception as e:
        logger.error("Database initialization failed", error=str(e))

    # Initialize RAG service
    try:
        rag_service = get_rag_service()
        rag_service.initialize()
        logger.info("RAG service initialized")

        # Try to ingest documents
        try:
            count = await rag_service.ingest_documents()
            if count > 0:
                logger.info("Initial document ingestion completed", count=count)
        except Exception as e:
            logger.warning("Initial document ingestion failed", error=str(e))

    except Exception as e:
        logger.error("RAG service initialization failed", error=str(e))

    yield

    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Simple RAG AI Agent with FastAPI backend",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sessions.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")


@app.get("/")
async def root() -> dict:
    """Root endpoint."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }


@app.get("/health")
async def health() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
