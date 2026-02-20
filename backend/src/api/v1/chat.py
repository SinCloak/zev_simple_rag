"""
Chat API endpoints with streaming support.
"""
import json
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from structlog import get_logger

from src.api.dependencies import ChatServiceDep, RAGServiceDep, SessionServiceDep
from src.application.dtos import (
    AssistantStreamEvent,
    ChatRequest,
    ChatResponse,
    ReferenceDocument,
    TokenUsage,
)

logger = get_logger()
router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    service: ChatServiceDep,
) -> ChatResponse:
    """
    Send a chat message and get a response (non-streaming).
    """
    logger.info("Processing chat request")
    return await service.chat(request)


@router.post("/stream")
async def chat_stream(
    request: ChatRequest,
    service: ChatServiceDep,
) -> StreamingResponse:
    """
    Send a chat message and get a streaming response.
    """
    logger.info("Processing streaming chat request")

    async def generate():
        """Stream generator function."""
        references_sent = False
        full_content = ""
        final_references: Optional[list] = None
        final_token_usage: Optional[dict] = None

        try:
            async for chunk, docs, token_usage in service.stream_chat(request):
                if chunk:
                    full_content += chunk
                    event = AssistantStreamEvent(
                        event_type="content",
                        content=chunk,
                    )
                    yield f"data: {json.dumps(event.model_dump())}\n\n"

                if docs and not references_sent:
                    final_references = docs
                    ref_docs = [
                        ReferenceDocument(
                            source=doc.metadata.get("source"),
                            content=doc.page_content,
                            metadata=doc.metadata,
                        )
                        for doc in docs
                    ]
                    event = AssistantStreamEvent(
                        event_type="references",
                        references=ref_docs,
                    )
                    yield f"data: {json.dumps(event.model_dump())}\n\n"
                    references_sent = True

                if token_usage:
                    final_token_usage = token_usage
                    event = AssistantStreamEvent(
                        event_type="token_usage",
                        token_usage=TokenUsage(**token_usage),
                    )
                    yield f"data: {json.dumps(event.model_dump())}\n\n"

            # Send done event
            event = AssistantStreamEvent(event_type="done")
            yield f"data: {json.dumps(event.model_dump())}\n\n"

        except Exception as e:
            logger.error("Stream error", error=str(e))
            event = AssistantStreamEvent(
                event_type="error",
                error=str(e),
            )
            yield f"data: {json.dumps(event.model_dump())}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/ingest", status_code=status.HTTP_202_ACCEPTED)
async def ingest_documents(
    rag_service: RAGServiceDep,
) -> dict:
    """
    Manually trigger document ingestion from the knowledge base.
    """
    try:
        count = await rag_service.ingest_documents()
        return {
            "message": "Ingestion completed",
            "documents_ingested": count,
        }
    except Exception as e:
        logger.error("Ingestion failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ingestion failed: {e}",
        )
