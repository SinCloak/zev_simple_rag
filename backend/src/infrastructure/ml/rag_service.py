"""
RAG (Retrieval-Augmented Generation) service using LangChain and Chroma.
"""
import os
from pathlib import Path
from typing import AsyncGenerator, Dict, List, Optional, Tuple

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from structlog import get_logger

from src.core.config import settings

logger = get_logger()


class RAGService:
    """Service for RAG operations using LangChain and Chroma."""

    def __init__(self) -> None:
        """Initialize the RAG service."""
        self.llm: Optional[ChatGoogleGenerativeAI] = None
        self.embeddings: Optional[GoogleGenerativeAIEmbeddings] = None
        self.vector_store: Optional[Chroma] = None
        self.retriever = None
        self.rag_chain = None
        self._initialized = False

    def initialize(self) -> None:
        """
        Initialize the RAG service components.

        Raises:
            RuntimeError: If initialization fails
        """
        try:
            logger.info("Initializing RAG service...")

            # Initialize LLM
            self.llm = ChatGoogleGenerativeAI(
                model=settings.gemini_model,
                google_api_key=settings.gemini_api_key,
                temperature=0.7,
                streaming=True,
            )

            # Initialize embeddings
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=settings.gemini_api_key,
            )

            # Initialize vector store
            persist_dir = Path(settings.chroma_persist_directory)
            persist_dir.mkdir(parents=True, exist_ok=True)

            self.vector_store = Chroma(
                collection_name=settings.chroma_collection_name,
                embedding_function=self.embeddings,
                persist_directory=str(persist_dir),
            )

            # Create retriever
            self.retriever = self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4},
            )

            # Create RAG chain
            self._create_rag_chain()

            self._initialized = True
            logger.info("RAG service initialized successfully")

        except Exception as e:
            logger.error("Failed to initialize RAG service", error=str(e))
            raise RuntimeError(f"RAG initialization failed: {e}") from e

    def _create_rag_chain(self) -> None:
        """Create the RAG chain with proper prompt template."""
        if not self.llm or not self.retriever:
            raise RuntimeError("RAG components not initialized")

        # System prompt for RAG
        system_prompt = """You are a helpful AI assistant. Use the following pieces of retrieved context to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Keep the answer concise and well-structured using markdown formatting where appropriate.

Context:
{context}
"""

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="chat_history", optional=True),
                ("human", "{input}"),
            ]
        )

        # Create the chain
        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        self.rag_chain = create_retrieval_chain(self.retriever, question_answer_chain)

    def is_initialized(self) -> bool:
        """Check if the service is initialized."""
        return self._initialized

    async def ingest_documents(self, knowledge_base_path: Optional[str] = None) -> int:
        """
        Ingest documents from the knowledge base directory.

        Args:
            knowledge_base_path: Path to the knowledge base directory.
                               Uses settings.knowledge_base_path if not provided.

        Returns:
            Number of documents ingested
        """
        if not self.vector_store or not self.embeddings:
            raise RuntimeError("RAG service not initialized")

        kb_path = Path(knowledge_base_path or settings.knowledge_base_path)

        if not kb_path.exists():
            logger.warning("Knowledge base path does not exist", path=str(kb_path))
            return 0

        documents = []
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True,
        )

        # Load all markdown files
        md_files = list(kb_path.rglob("*.md"))
        logger.info(f"Found {len(md_files)} markdown files")

        for md_file in md_files:
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Create document with metadata
                doc = Document(
                    page_content=content,
                    metadata={
                        "source": str(md_file.relative_to(kb_path)),
                        "file_path": str(md_file),
                    },
                )

                # Split document
                split_docs = text_splitter.split_documents([doc])
                documents.extend(split_docs)
                logger.debug(f"Processed {md_file.name}: {len(split_docs)} chunks")

            except Exception as e:
                logger.error(f"Failed to process {md_file}", error=str(e))

        if documents:
            # Add to vector store
            self.vector_store.add_documents(documents)
            logger.info(f"Ingested {len(documents)} document chunks")
            return len(documents)

        return 0

    async def query(
        self,
        question: str,
        chat_history: Optional[List[Dict]] = None,
    ) -> Tuple[str, List[Document], Dict]:
        """
        Query the RAG system.

        Args:
            question: The user's question
            chat_history: Optional chat history as list of message dicts

        Returns:
            Tuple of (answer, referenced_documents, token_usage)
        """
        if not self.rag_chain:
            raise RuntimeError("RAG chain not initialized")

        try:
            # Format chat history for LangChain
            formatted_history = []
            if chat_history:
                for msg in chat_history:
                    if msg.get("role") == "user":
                        formatted_history.append(("human", msg.get("content", "")))
                    elif msg.get("role") == "assistant":
                        formatted_history.append(("ai", msg.get("content", "")))

            # Invoke RAG chain
            result = await self.rag_chain.ainvoke({
                "input": question,
                "chat_history": formatted_history,
            })

            answer = result.get("answer", "")
            docs = result.get("context", [])

            # Token usage - Gemini provides this differently
            token_usage = {
                "input_tokens": None,
                "output_tokens": None,
                "rag_tokens": self._estimate_rag_tokens(docs),
                "total_tokens": None,
            }

            return answer, docs, token_usage

        except Exception as e:
            logger.error("RAG query failed", error=str(e))
            raise

    async def stream_query(
        self,
        question: str,
        chat_history: Optional[List[Dict]] = None,
    ) -> AsyncGenerator[Tuple[str, Optional[List[Document]], Optional[Dict]], None]:
        """
        Stream the RAG query response.

        Args:
            question: The user's question
            chat_history: Optional chat history

        Yields:
            Tuples of (content_chunk, documents, token_usage)
        """
        if not self.llm or not self.retriever:
            raise RuntimeError("RAG service not initialized")

        try:
            # First retrieve relevant documents
            docs = await self.retriever.ainvoke(question)

            # Format context
            context = "\n\n".join([
                f"Source: {doc.metadata.get('source', 'unknown')}\n{doc.page_content}"
                for doc in docs
            ])

            # Build prompt
            system_prompt = f"""You are a helpful AI assistant. Use the following pieces of retrieved context to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Keep the answer concise and well-structured using markdown formatting where appropriate.

Context:
{context}
"""

            messages = [
                ("system", system_prompt),
            ]

            # Add chat history
            if chat_history:
                for msg in chat_history:
                    if msg.get("role") == "user":
                        messages.append(("human", msg.get("content", "")))
                    elif msg.get("role") == "assistant":
                        messages.append(("ai", msg.get("content", "")))

            messages.append(("human", question))

            # Stream the response
            docs_sent = False
            token_usage = {
                "rag_tokens": self._estimate_rag_tokens(docs),
            }

            async for chunk in self.llm.astream(messages):
                if not docs_sent:
                    yield chunk.content, docs, token_usage
                    docs_sent = True
                else:
                    yield chunk.content, None, None

        except Exception as e:
            logger.error("Stream query failed", error=str(e))
            raise

    def _estimate_rag_tokens(self, docs: List[Document]) -> int:
        """Estimate the number of tokens in retrieved documents."""
        total_chars = sum(len(doc.page_content) for doc in docs)
        # Rough estimate: 1 token ≈ 4 characters
        return total_chars // 4


# Singleton instance
_rag_service: Optional[RAGService] = None


def get_rag_service() -> RAGService:
    """Get or create the RAG service singleton."""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service
