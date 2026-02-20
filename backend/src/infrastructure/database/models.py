"""
SQLAlchemy ORM models for the application.
All tables are prefixed with 'zev_simple_rag_1_'.
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


class SessionModel(Base):
    """
    Chat session model.
    Table name: zev_simple_rag_1_sessions
    """

    __tablename__ = "zev_simple_rag_1_sessions"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    messages: Mapped[List["MessageModel"]] = relationship(
        "MessageModel", back_populates="session", cascade="all, delete-orphan", order_by="MessageModel.created_at"
    )


class MessageModel(Base):
    """
    Chat message model.
    Table name: zev_simple_rag_1_messages
    """

    __tablename__ = "zev_simple_rag_1_messages"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    session_id: Mapped[UUID] = mapped_column(ForeignKey("zev_simple_rag_1_sessions.id"), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)  # 'user' or 'assistant'
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Token usage information
    input_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    output_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    rag_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    total_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # RAG references (stored as JSONB)
    rag_references: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Relationships
    session: Mapped["SessionModel"] = relationship("SessionModel", back_populates="messages")
