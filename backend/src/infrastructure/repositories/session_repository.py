"""
Repository for session and message database operations.
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from structlog import get_logger

from src.domain.entities import Message, Session
from src.infrastructure.database.models import MessageModel, SessionModel

logger = get_logger()


class SessionRepository:
    """Repository for session database operations."""

    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create(self, session: Session) -> Session:
        """
        Create a new session in the database.

        Args:
            session: Session domain entity

        Returns:
            Created session with ID
        """
        db_session = SessionModel(
            id=session.id,
            title=session.title,
            created_at=session.created_at,
            updated_at=session.updated_at,
            is_active=session.is_active,
        )
        self.db_session.add(db_session)
        await self.db_session.commit()
        await self.db_session.refresh(db_session)

        return self._to_entity(db_session)

    async def get_by_id(self, session_id: UUID, include_messages: bool = False) -> Optional[Session]:
        """
        Get a session by ID.

        Args:
            session_id: Session UUID
            include_messages: Whether to include messages

        Returns:
            Session entity or None
        """
        stmt = select(SessionModel).where(SessionModel.id == session_id)

        if include_messages:
            stmt = stmt.options(selectinload(SessionModel.messages))

        result = await self.db_session.execute(stmt)
        db_session = result.scalar_one_or_none()

        if not db_session:
            return None

        return self._to_entity(db_session, include_messages=include_messages)

    async def list_all(self, only_active: bool = True) -> List[Session]:
        """
        List all sessions.

        Args:
            only_active: Whether to only return active sessions

        Returns:
            List of session entities
        """
        stmt = select(SessionModel).order_by(SessionModel.updated_at.desc())

        if only_active:
            stmt = stmt.where(SessionModel.is_active.is_(True))

        result = await self.db_session.execute(stmt)
        db_sessions = result.scalars().all()

        return [self._to_entity(s) for s in db_sessions]

    async def update(self, session: Session) -> Optional[Session]:
        """
        Update a session.

        Args:
            session: Session entity with updated fields

        Returns:
            Updated session or None
        """
        db_session = await self.db_session.get(SessionModel, session.id)
        if not db_session:
            return None

        db_session.title = session.title
        db_session.is_active = session.is_active
        db_session.updated_at = datetime.utcnow()

        await self.db_session.commit()
        await self.db_session.refresh(db_session)

        return self._to_entity(db_session)

    async def delete(self, session_id: UUID) -> bool:
        """
        Delete a session (soft delete by deactivating).

        Args:
            session_id: Session UUID

        Returns:
            True if deleted
        """
        db_session = await self.db_session.get(SessionModel, session_id)
        if not db_session:
            return False

        db_session.is_active = False
        db_session.updated_at = datetime.utcnow()

        await self.db_session.commit()
        return True

    def _to_entity(self, db_session: SessionModel, include_messages: bool = False) -> Session:
        """Convert DB model to domain entity."""
        messages = []
        if include_messages and db_session.messages:
            messages = [
                Message(
                    id=m.id,
                    session_id=m.session_id,
                    role=m.role,
                    content=m.content,
                    created_at=m.created_at,
                    input_tokens=m.input_tokens,
                    output_tokens=m.output_tokens,
                    rag_tokens=m.rag_tokens,
                    total_tokens=m.total_tokens,
                    rag_references=m.rag_references,
                )
                for m in db_session.messages
            ]

        return Session(
            id=db_session.id,
            title=db_session.title,
            created_at=db_session.created_at,
            updated_at=db_session.updated_at,
            is_active=db_session.is_active,
            messages=messages,
        )


class MessageRepository:
    """Repository for message database operations."""

    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create(self, message: Message) -> Message:
        """
        Create a new message.

        Args:
            message: Message domain entity

        Returns:
            Created message
        """
        db_message = MessageModel(
            id=message.id,
            session_id=message.session_id,
            role=message.role,
            content=message.content,
            created_at=message.created_at,
            input_tokens=message.input_tokens,
            output_tokens=message.output_tokens,
            rag_tokens=message.rag_tokens,
            total_tokens=message.total_tokens,
            rag_references=message.rag_references,
        )
        self.db_session.add(db_message)
        await self.db_session.commit()
        await self.db_session.refresh(db_message)

        return self._to_entity(db_message)

    async def get_by_session(self, session_id: UUID) -> List[Message]:
        """
        Get all messages for a session.

        Args:
            session_id: Session UUID

        Returns:
            List of messages
        """
        stmt = (
            select(MessageModel)
            .where(MessageModel.session_id == session_id)
            .order_by(MessageModel.created_at)
        )
        result = await self.db_session.execute(stmt)
        db_messages = result.scalars().all()

        return [self._to_entity(m) for m in db_messages]

    def _to_entity(self, db_message: MessageModel) -> Message:
        """Convert DB model to domain entity."""
        return Message(
            id=db_message.id,
            session_id=db_message.session_id,
            role=db_message.role,
            content=db_message.content,
            created_at=db_message.created_at,
            input_tokens=db_message.input_tokens,
            output_tokens=db_message.output_tokens,
            rag_tokens=db_message.rag_tokens,
            total_tokens=db_message.total_tokens,
            rag_references=db_message.rag_references,
        )
