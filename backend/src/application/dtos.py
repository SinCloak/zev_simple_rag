"""
Data Transfer Objects (DTOs) for API requests and responses.
"""
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ============== Session DTOs ==============

class SessionBase(BaseModel):
    """Base session schema."""

    title: str = Field(..., min_length=1, max_length=255)


class SessionCreate(SessionBase):
    """Schema for creating a session."""

    pass


class SessionUpdate(SessionBase):
    """Schema for updating a session."""

    is_active: Optional[bool] = None


class SessionResponse(SessionBase):
    """Schema for session responses."""

    id: UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool
    message_count: Optional[int] = None

    class Config:
        from_attributes = True


class SessionDetailResponse(SessionResponse):
    """Schema for session detail with messages."""

    messages: List["MessageResponse"] = []


# ============== Message DTOs ==============

class MessageBase(BaseModel):
    """Base message schema."""

    content: str = Field(..., min_length=1)


class UserMessageRequest(MessageBase):
    """Schema for user message requests."""

    enable_web_search: bool = False
    enable_deep_thinking: bool = False


class TokenUsage(BaseModel):
    """Schema for token usage information."""

    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    rag_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class ReferenceDocument(BaseModel):
    """Schema for RAG reference document."""

    source: Optional[str] = None
    content: str
    metadata: Dict = Field(default_factory=dict)
    similarity_score: Optional[float] = None


class MessageResponse(MessageBase):
    """Schema for message responses."""

    id: UUID
    session_id: UUID
    role: str
    created_at: datetime
    token_usage: Optional[TokenUsage] = None
    references: Optional[List[ReferenceDocument]] = None

    class Config:
        from_attributes = True


class AssistantStreamEvent(BaseModel):
    """Schema for streaming events."""

    event_type: str  # 'content', 'token_usage', 'references', 'done', 'error'
    content: Optional[str] = None
    token_usage: Optional[TokenUsage] = None
    references: Optional[List[ReferenceDocument]] = None
    error: Optional[str] = None


# ============== Chat DTOs ==============

class ChatRequest(BaseModel):
    """Schema for chat requests."""

    message: str = Field(..., min_length=1)
    session_id: Optional[UUID] = None
    enable_web_search: bool = False
    enable_deep_thinking: bool = False


class ChatResponse(BaseModel):
    """Schema for chat responses."""

    session_id: UUID
    message: MessageResponse


# Update forward references
SessionDetailResponse.model_rebuild()
