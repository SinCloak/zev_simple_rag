# Zev Simple RAG Backend

FastAPI backend for the RAG AI Agent.

## Installation

```bash
# Using the fixed virtual environment
D:\PythonVenv\Scripts\python.exe -m pip install poetry
D:\PythonVenv\Scripts\python.exe -m poetry install
```

## Running

```bash
# Development mode with hot reload
D:\PythonVenv\Scripts\python.exe -m poetry run uvicorn src.main:app --reload

# Or using the main module directly
D:\PythonVenv\Scripts\python.exe -m poetry run python -m src.main
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
src/
├── api/
│   ├── dependencies.py    # FastAPI dependency injection
│   └── v1/
│       ├── sessions.py    # Session management endpoints
│       └── chat.py        # Chat endpoints
├── application/
│   ├── dtos.py            # Pydantic schemas
│   └── services.py        # Business logic
├── domain/
│   └── entities.py        # Domain models
├── infrastructure/
│   ├── database/
│   │   ├── models.py      # SQLAlchemy models
│   │   └── session.py     # DB session management
│   ├── ml/
│   │   └── rag_service.py # RAG with LangChain + Chroma
│   └── repositories/
│       └── session_repository.py
├── core/
│   ├── config.py          # Settings
│   └── logging.py         # Logging configuration
└── main.py                # FastAPI entry point
```
