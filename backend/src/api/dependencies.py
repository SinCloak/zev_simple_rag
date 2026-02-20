"""
FastAPI dependency injection configuration.
"""
from typing import Annotated, AsyncGenerator, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger

from src.application.services import ChatService, SessionService
from src.core.config import settings
from src.infrastructure.database.session import get_db_session
from src.infrastructure.ml.rag_service import RAGService, get_rag_service
from src.infrastructure.repositories.session_repository import (
    MessageRepository,
    SessionRepository,
)

logger = get_logger()

# Type aliases for dependencies
DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]


# RAG Service dependency
async def get_rag_service_dep() -> AsyncGenerator[RAGService, None]:
    """Get the RAG service, initializing if needed."""
    rag_service = get_rag_service()
    if not rag_service.is_initialized():
        rag_service.initialize()

        # Try to ingest documents if knowledge base exists
        try:
            await rag_service.ingest_documents()
        except Exception as e:
            logger.warning("Failed to ingest initial documents", error=str(e))

    yield rag_service


RAGServiceDep = Annotated[RAGService, Depends(get_rag_service_dep)]


# Repository dependencies
def get_session_repository(db_session: DbSessionDep) -> SessionRepository:
    """Get session repository."""
    return SessionRepository(db_session)


def get_message_repository(db_session: DbSessionDep) -> MessageRepository:
    """Get message repository."""
    return MessageRepository(db_session)


SessionRepositoryDep = Annotated[SessionRepository, Depends(get_session_repository)]
MessageRepositoryDep = Annotated[MessageRepository, Depends(get_message_repository)]


# Service dependencies
def get_session_service(
    session_repo: SessionRepositoryDep,
    message_repo: MessageRepositoryDep,
) -> SessionService:
    """Get session service."""
    return SessionService(session_repo, message_repo)


def get_chat_service(
    session_repo: SessionRepositoryDep,
    message_repo: MessageRepositoryDep,
    rag_service: RAGServiceDep,
) -> ChatService:
    """Get chat service."""
    return ChatService(session_repo, message_repo, rag_service)


SessionServiceDep = Annotated[SessionService, Depends(get_session_service)]
ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]
