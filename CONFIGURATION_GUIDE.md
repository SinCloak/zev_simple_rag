# Configuration Guide

This project has been pre-configured with the credentials provided. Below is the detailed configuration information.

## Credentials Summary

| Service | Credential | Value |
|---------|-----------|-------|
| **Gemini API Key** | `gemini_api_key` | `AIzaSyCzRQ3CnG0yK8gE8zqVPYDr3eBYOgf0oCc` |
| **PostgreSQL** | Host | `localhost` |
| **PostgreSQL** | Port | `5432` |
| **PostgreSQL** | User | `postgres` |
| **PostgreSQL** | Password | `6666` |
| **PostgreSQL** | Database | `postgres` |

## Backend Configuration

### Environment Variables

Create a `backend/.env` file (optional - defaults are already set):

```env
# Application
DEBUG=true

# Database
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_PASSWORD=6666
DATABASE_NAME=postgres

# Gemini API
GEMINI_API_KEY=AIzaSyCzRQ3CnG0yK8gE8zqVPYDr3eBYOgf0oCc
GEMINI_MODEL=gemini-3.5-pro-preview

# Chroma DB
CHROMA_PERSIST_DIRECTORY=./chroma_db
CHROMA_COLLECTION_NAME=zev_simple_rag_1_docs

# Knowledge Base
KNOWLEDGE_BASE_PATH=./knowledge_base

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

### Configuration File

The main configuration is in `backend/src/core/config.py`. All default values are pre-configured.

## Frontend Configuration

Create a `frontend/.env.development` file (optional):

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Database Setup

### PostgreSQL

Ensure PostgreSQL is installed and running:

```bash
# Check if PostgreSQL is running (Windows)
# Use Services.msc or pgAdmin

# Or via command line (if in PATH)
psql --version
```

### Database Tables

The application will automatically create the following tables on startup:
- `zev_simple_rag_1_sessions` - Chat sessions
- `zev_simple_rag_1_messages` - Chat messages

No manual migrations needed.

## Knowledge Base

### Adding Documents

1. Add your Markdown documents to `backend/knowledge_base/`
2. The system will automatically ingest them on startup
3. Or manually trigger ingestion via API:
   ```bash
   curl -X POST http://localhost:8000/api/v1/chat/ingest
   ```

### Document Structure

The knowledge base is pre-populated with:
- Gemini API documentation
- LangChain documentation
- Chroma DB documentation

## Running the Application

### Start Backend

```bash
cd backend
D:\PythonVenv\Scripts\python.exe -m poetry install
D:\PythonVenv\Scripts\python.exe -m poetry run uvicorn src.main:app --reload
```

Backend URL: http://localhost:8000
API Docs: http://localhost:8000/docs

### Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: http://localhost:3000

## API Usage Examples

### Create a Session

```bash
curl -X POST http://localhost:8000/api/v1/sessions \
  -H "Content-Type: application/json" \
  -d '{"title": "My Chat"}'
```

### Send a Chat Message (Streaming)

```javascript
// Using the EventSource API in browser
const response = await fetch('/api/v1/chat/stream', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'What is RAG?',
    session_id: 'your-session-uuid',
    enable_web_search: false,
    enable_deep_thinking: false
  })
});
```

## Troubleshooting

### Backend won't start

- Check PostgreSQL is running on port 5432
- Verify PostgreSQL credentials (user: postgres, password: 6666)
- Check that the Python virtual environment is correct: `D:\PythonVenv\Scripts\python.exe`

### Frontend can't connect to backend

- Ensure backend is running on http://localhost:8000
- Check CORS settings in `backend/src/core/config.py`
- Verify the API proxy in `frontend/vite.config.ts`

### RAG not returning relevant results

- Check that documents were ingested (call `/api/v1/chat/ingest`)
- Verify Chroma DB is created in `backend/chroma_db/`
- Check that documents are in Markdown format

## Gemini API

The Gemini API key is pre-configured:
- API Key: `AIzaSyCzRQ3CnG0yK8gE8zqVPYDr3eBYOgf0oCc`
- Model: `gemini-3.5-pro-preview`

To change the model, update `GEMINI_MODEL` in your `.env` file.

## Git Configuration

### GitHub Repository

- Repository: https://github.com/SinCloak/zev_simple_rag
- Email: zeagglefkus@gmail.com
- Password: zHZ48484

To push changes:

```bash
git remote add origin https://github.com/SinCloak/zev_simple_rag.git
git branch -M main
git push -u origin main
```

When prompted for credentials:
- Username: zeagglefkus@gmail.com
- Password: zHZ48484
