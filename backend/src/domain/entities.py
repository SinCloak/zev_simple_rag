"""
Domain entities for the application.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID, uuid4


@dataclass
class Message:
    """Chat message domain entity."""

    id: UUID = field(default_factory=uuid4)
    session_id: Optional[UUID] = None
    role: str = "user"  # 'user' or 'assistant'
    content: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)

    # Token usage
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    rag_tokens: Optional[int] = None
    total_tokens: Optional[int] = None

    # RAG references
    rag_references: Optional[List[Dict]] = None


@dataclass
class Session:
    """Chat session domain entity."""

    id: UUID = field(default_factory=uuid4)
    title: str = "New Conversation"
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True
    messages: List[Message] = field(default_factory=list)

    def add_message(self, message: Message) -> None:
        """Add a message to the session."""
        message.session_id = self.id
        self.messages.append(message)
        self.updated_at = datetime.utcnow()
