# Zev Simple RAG AI Agent

A simple yet powerful RAG (Retrieval-Augmented Generation) AI Agent with FastAPI backend and Vue3 frontend.

## Features

- 🤖 **AI Chat**: Conversational interface powered by Gemini 3.5 Pro
- 📚 **RAG System**: Built-in knowledge base using Chroma vector database
- 💬 **Session Management**: Chat history and context persistence
- 📝 **Markdown Rendering**: Beautifully formatted AI responses
- 📊 **Token Usage**: Detailed token consumption breakdown
- 🔄 **Streaming Responses**: Real-time AI responses
- 📖 **Reference Display**: Show sources used for RAG answers
- 🌐 **Web Search**: Optional web search (configurable)
- 🧠 **Deep Thinking**: Optional deep thinking mode (configurable)

## Tech Stack

### Backend
- **FastAPI**: Modern, fast Python web framework
- **SQLAlchemy 2.0**: Async ORM for PostgreSQL
- **LangChain**: RAG framework
- **Chroma**: Vector database
- **Gemini API**: LLM from Google
- **PostgreSQL**: Persistent storage for sessions

### Frontend
- **Vue 3**: Progressive JavaScript framework
- **TypeScript**: Type-safe development
- **Vite**: Fast build tool
- **Pinia**: State management
- **Marked**: Markdown parser
- **Highlight.js**: Code syntax highlighting

## Project Structure

```
zev_simple_rag_1/
├── backend/
│   ├── src/
│   │   ├── api/              # API routes
│   │   ├── application/      # Application services
│   │   ├── domain/           # Domain entities
│   │   ├── infrastructure/   # Database, RAG, repositories
│   │   ├── core/             # Config, logging
│   │   └── main.py           # FastAPI entry
│   ├── knowledge_base/       # Markdown documents
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── api/              # API clients
│   │   ├── components/       # Vue components
│   │   ├── router/           # Vue router
│   │   ├── stores/           # Pinia stores
│   │   ├── types/            # TypeScript types
│   │   ├── views/            # Page components
│   │   └── main.ts
│   └── package.json
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Poetry (for Python dependencies)

### Backend Setup

1. **Install dependencies**:
   ```bash
   cd backend
   D:\PythonVenv\Scripts\python.exe -m pip install poetry
   D:\PythonVenv\Scripts\python.exe -m poetry install
   ```

2. **Configure PostgreSQL**:
   - Ensure PostgreSQL is running on port 5432
   - Default credentials: user `postgres`, password `6666`

3. **Start the backend**:
   ```bash
   D:\PythonVenv\Scripts\python.exe -m poetry run uvicorn src.main:app --reload
   ```

   The backend will be available at: http://localhost:8000
   API docs: http://localhost:8000/docs

### Frontend Setup

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start the frontend**:
   ```bash
   npm run dev
   ```

   The frontend will be available at: http://localhost:3000

## Configuration

See [CONFIGURATION_GUIDE.md](./CONFIGURATION_GUIDE.md) for detailed configuration options.

## API Endpoints

### Sessions
- `POST /api/v1/sessions` - Create a new session
- `GET /api/v1/sessions` - List all sessions
- `GET /api/v1/sessions/{id}` - Get session with messages
- `PUT /api/v1/sessions/{id}` - Update a session
- `DELETE /api/v1/sessions/{id}` - Delete a session

### Chat
- `POST /api/v1/chat` - Send a chat message (non-streaming)
- `POST /api/v1/chat/stream` - Send a chat message (streaming)
- `POST /api/v1/chat/ingest` - Ingest documents from knowledge base

## Knowledge Base

Add your Markdown documents to `backend/knowledge_base/`. The system will automatically:
- Load `.md` files
- Split them into chunks
- Store in Chroma vector database
- Retrieve relevant documents during chat

## Database Tables

All tables are prefixed with `zev_simple_rag_1_`:
- `zev_simple_rag_1_sessions` - Chat sessions
- `zev_simple_rag_1_messages` - Chat messages with token usage and references

## License

MIT
