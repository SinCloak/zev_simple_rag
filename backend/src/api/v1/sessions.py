"""
Session management API endpoints.
"""
from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from structlog import get_logger

from src.api.dependencies import SessionServiceDep
from src.application.dtos import (
    SessionCreate,
    SessionDetailResponse,
    SessionResponse,
    SessionUpdate,
)

logger = get_logger()
router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    data: SessionCreate,
    service: SessionServiceDep,
) -> SessionResponse:
    """
    Create a new chat session.
    """
    logger.info("Creating new session", title=data.title)
    return await service.create_session(data)


@router.get("", response_model=List[SessionResponse])
async def list_sessions(
    service: SessionServiceDep,
) -> List[SessionResponse]:
    """
    List all active chat sessions.
    """
    return await service.list_sessions()


@router.get("/{session_id}", response_model=SessionDetailResponse)
async def get_session(
    session_id: UUID,
    service: SessionServiceDep,
) -> SessionDetailResponse:
    """
    Get a session by ID with all messages.
    """
    session = await service.get_session(session_id, include_messages=True)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )
    return session


@router.put("/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: UUID,
    data: SessionUpdate,
    service: SessionServiceDep,
) -> SessionResponse:
    """
    Update a session.
    """
    session = await service.update_session(session_id, data)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )
    return session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: UUID,
    service: SessionServiceDep,
) -> None:
    """
    Delete (deactivate) a session.
    """
    success = await service.delete_session(session_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )
