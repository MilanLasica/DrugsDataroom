# PharmaFlow Backend

FastAPI backend for PharmaFlow - AI-Driven Drug Manufacturing Assistant

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. (Optional) Run Weaviate locally:
```bash
docker run -d \
  -p 8080:8080 \
  -p 50051:50051 \
  --name weaviate \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  semitechnologies/weaviate:latest
```

5. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Key Endpoints

- `POST /api/upload` - Upload pharmaceutical PDF
- `GET /api/documents` - List all documents
- `GET /api/documents/{id}` - Get multi-perspective analysis
- `POST /api/chat` - Chat with document
- `GET /api/search` - Search related literature

## Architecture

- **Document Processing**: LlamaIndex for PDF parsing and entity extraction
- **Vector Store**: Weaviate for semantic search and embeddings
- **LLM Inference**: FriendliAI for fast, low-latency responses
- **Multi-Perspective Extraction**: Finance, Sustainability, Chemistry analysis
- **Chat Agent**: Conversational interface with citations

