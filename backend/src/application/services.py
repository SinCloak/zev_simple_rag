"""
Application services for business logic orchestration.
"""
from datetime import datetime
from typing import AsyncGenerator, Dict, List, Optional, Tuple
from uuid import UUID, uuid4

from structlog import get_logger

from src.application.dtos import (
    ChatRequest,
    ChatResponse,
    MessageResponse,
    ReferenceDocument,
    SessionCreate,
    SessionDetailResponse,
    SessionResponse,
    SessionUpdate,
    TokenUsage,
)
from src.domain.entities import Message, Session
from src.infrastructure.ml.rag_service import RAGService, get_rag_service
from src.infrastructure.repositories.session_repository import (
    MessageRepository,
    SessionRepository,
)

logger = get_logger()


class SessionService:
    """Service for session management operations."""

    def __init__(
        self,
        session_repo: SessionRepository,
        message_repo: MessageRepository,
    ) -> None:
        self.session_repo = session_repo
        self.message_repo = message_repo

    async def create_session(self, data: SessionCreate) -> SessionResponse:
        """
        Create a new chat session.

        Args:
            data: Session creation data

        Returns:
            Created session response
        """
        session = Session(title=data.title)
        created = await self.session_repo.create(session)

        return SessionResponse(
            id=created.id,
            title=created.title,
            created_at=created.created_at,
            updated_at=created.updated_at,
            is_active=created.is_active,
            message_count=0,
        )

    async def get_session(self, session_id: UUID, include_messages: bool = False) -> Optional[SessionResponse]:
        """
        Get a session by ID.

        Args:
            session_id: Session UUID
            include_messages: Whether to include messages

        Returns:
            Session response or None
        """
        session = await self.session_repo.get_by_id(session_id, include_messages=include_messages)
        if not session:
            return None

        if include_messages:
            return SessionDetailResponse(
                id=session.id,
                title=session.title,
                created_at=session.created_at,
                updated_at=session.updated_at,
                is_active=session.is_active,
                message_count=len(session.messages),
                messages=[
                    self._message_to_response(m)
                    for m in session.messages
                ],
            )

        return SessionResponse(
            id=session.id,
            title=session.title,
            created_at=session.created_at,
            updated_at=session.updated_at,
            is_active=session.is_active,
            message_count=len(session.messages),
        )

    async def list_sessions(self) -> List[SessionResponse]:
        """
        List all active sessions.

        Returns:
            List of session responses
        """
        sessions = await self.session_repo.list_all(only_active=True)
        return [
            SessionResponse(
                id=s.id,
                title=s.title,
                created_at=s.created_at,
                updated_at=s.updated_at,
                is_active=s.is_active,
                message_count=len(s.messages),
            )
            for s in sessions
        ]

    async def update_session(self, session_id: UUID, data: SessionUpdate) -> Optional[SessionResponse]:
        """
        Update a session.

        Args:
            session_id: Session UUID
            data: Update data

        Returns:
            Updated session or None
        """
        session = await self.session_repo.get_by_id(session_id)
        if not session:
            return None

        if data.title is not None:
            session.title = data.title
        if data.is_active is not None:
            session.is_active = data.is_active

        updated = await self.session_repo.update(session)
        if not updated:
            return None

        return SessionResponse(
            id=updated.id,
            title=updated.title,
            created_at=updated.created_at,
            updated_at=updated.updated_at,
            is_active=updated.is_active,
        )

    async def delete_session(self, session_id: UUID) -> bool:
        """
        Delete (deactivate) a session.

        Args:
            session_id: Session UUID

        Returns:
            True if deleted
        """
        return await self.session_repo.delete(session_id)

    def _message_to_response(self, message: Message) -> MessageResponse:
        """Convert a Message entity to response DTO."""
        references = None
        if message.rag_references:
            references = [
                ReferenceDocument(
                    source=ref.get("source"),
                    content=ref.get("content", ""),
                    metadata=ref.get("metadata", {}),
                    similarity_score=ref.get("similarity_score"),
                )
                for ref in message.rag_references
            ]

        token_usage = None
        if any([
            message.input_tokens,
            message.output_tokens,
            message.rag_tokens,
            message.total_tokens,
        ]):
            token_usage = TokenUsage(
                input_tokens=message.input_tokens,
                output_tokens=message.output_tokens,
                rag_tokens=message.rag_tokens,
                total_tokens=message.total_tokens,
            )

        return MessageResponse(
            id=message.id,
            session_id=message.session_id,
            role=message.role,
            content=message.content,
            created_at=message.created_at,
            token_usage=token_usage,
            references=references,
        )


class ChatService:
    """Service for chat operations with RAG."""

    def __init__(
        self,
        session_repo: SessionRepository,
        message_repo: MessageRepository,
        rag_service: RAGService,
    ) -> None:
        self.session_repo = session_repo
        self.message_repo = message_repo
        self.rag_service = rag_service

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """
        Process a chat request (non-streaming).

        Args:
            request: Chat request data

        Returns:
            Chat response
        """
        # Get or create session
        session = None
        if request.session_id:
            session = await self.session_repo.get_by_id(request.session_id, include_messages=True)

        if not session:
            session = Session(title=self._generate_title(request.message))
            session = await self.session_repo.create(session)

        # Save user message
        user_message = Message(
            session_id=session.id,
            role="user",
            content=request.message,
        )
        await self.message_repo.create(user_message)

        # Get chat history
        chat_history = [
            {"role": m.role, "content": m.content}
            for m in session.messages
        ]

        # Query RAG
        answer, docs, token_usage = await self.rag_service.query(
            question=request.message,
            chat_history=chat_history,
        )

        # Prepare references
        references = [
            {
                "source": doc.metadata.get("source"),
                "content": doc.page_content[:200] + "...",
                "metadata": doc.metadata,
            }
            for doc in docs
        ]

        # Save assistant message
        assistant_message = Message(
            id=uuid4(),
            session_id=session.id,
            role="assistant",
            content=answer,
            created_at=datetime.utcnow(),
            input_tokens=token_usage.get("input_tokens"),
            output_tokens=token_usage.get("output_tokens"),
            rag_tokens=token_usage.get("rag_tokens"),
            total_tokens=token_usage.get("total_tokens"),
            rag_references=references,
        )
        await self.message_repo.create(assistant_message)

        # Update session
        session.title = self._generate_title(request.message)
        await self.session_repo.update(session)

        # Convert to response
        ref_docs = [
            ReferenceDocument(
                source=doc.metadata.get("source"),
                content=doc.page_content,
                metadata=doc.metadata,
            )
            for doc in docs
        ]

        msg_response = MessageResponse(
            id=assistant_message.id,
            session_id=assistant_message.session_id,
            role=assistant_message.role,
            content=assistant_message.content,
            created_at=assistant_message.created_at,
            token_usage=TokenUsage(**token_usage) if token_usage else None,
            references=ref_docs,
        )

        return ChatResponse(session_id=session.id, message=msg_response)

    async def stream_chat(
        self,
        request: ChatRequest,
    ) -> AsyncGenerator[Tuple[str, Optional[List[ReferenceDocument]], Optional[Dict]], None]:
        """
        Stream a chat response.

        Args:
            request: Chat request data

        Yields:
            Tuples of (content_chunk, references, token_usage)
        """
        # Get or create session
        session = None
        if request.session_id:
            session = await self.session_repo.get_by_id(request.session_id, include_messages=True)

        if not session:
            session = Session(title=self._generate_title(request.message))
            session = await self.session_repo.create(session)

        # Save user message
        user_message = Message(
            session_id=session.id,
            role="user",
            content=request.message,
        )
        await self.message_repo.create(user_message)

        # Get chat history
        chat_history = [
            {"role": m.role, "content": m.content}
            for m in session.messages
        ]

        # Stream RAG response
        full_content = ""
        ref_docs = None
        token_usage = None

        async for chunk, docs, tu in self.rag_service.stream_query(
            question=request.message,
            chat_history=chat_history,
        ):
            full_content += chunk or ""
            if docs is not None:
                ref_docs = docs
            if tu is not None:
                token_usage = tu

            yield chunk, docs, tu

        # Save assistant message after stream completes
        references = []
        if ref_docs:
            references = [
                {
                    "source": doc.metadata.get("source"),
                    "content": doc.page_content[:200] + "...",
                    "metadata": doc.metadata,
                }
                for doc in ref_docs
            ]

        assistant_message = Message(
            id=uuid4(),
            session_id=session.id,
            role="assistant",
            content=full_content,
            created_at=datetime.utcnow(),
            rag_tokens=token_usage.get("rag_tokens") if token_usage else None,
            rag_references=references,
        )
        await self.message_repo.create(assistant_message)

        # Update session title
        session.title = self._generate_title(request.message)
        await self.session_repo.update(session)

    def _generate_title(self, message: str, max_length: int = 50) -> str:
        """Generate a session title from the first message."""
        title = message.strip()[:max_length]
        if len(message) > max_length:
            title += "..."
        return title or "New Conversation"
