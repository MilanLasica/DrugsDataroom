# PharmaFlow Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         PharmaFlow System                        │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────┐         ┌──────────────────────┐
│   Frontend (React)   │ ◄─────► │  Backend (FastAPI)   │
│   Next.js + D3.js    │  HTTP   │   Python 3.11+       │
│   Port: 3000         │         │   Port: 8000         │
└──────────────────────┘         └──────────────────────┘
         │                                 │
         │                                 │
         │                        ┌────────┴────────┐
         │                        │                 │
         │                   ┌────▼─────┐    ┌─────▼─────┐
         │                   │ Weaviate │    │ FriendliAI│
         │                   │  Vector  │    │    API    │
         │                   │   Store  │    │ (External)│
         │                   │ Port:8080│    └───────────┘
         │                   └──────────┘
         │
    ┌────▼─────────────────────────────────┐
    │    Browser (User Interface)          │
    │  - Upload documents                  │
    │  - View analysis                     │
    │  - Explore graph                     │
    │  - Chat with agent                   │
    └──────────────────────────────────────┘
```

## Data Flow

### Stage 1: Document Ingestion

```
User uploads PDF
      │
      ▼
┌──────────────────┐
│  DocumentUpload  │  (React Component)
│   Component      │
└────────┬─────────┘
         │ POST /api/upload
         ▼
┌──────────────────┐
│   FastAPI        │
│   Upload         │
│   Endpoint       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ DocumentProcessor│
│  (LlamaIndex)    │
│                  │
│ - Parse PDF      │
│ - Extract text   │
│ - Chunk content  │
│ - Extract        │
│   entities       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ WeaviateService  │
│                  │
│ - Embed chunks   │
│ - Store vectors  │
│ - Index metadata │
└──────────────────┘
```

### Stage 2: Multi-Perspective Extraction

```
User selects document
      │
      ▼
GET /api/documents/{id}
      │
      ▼
┌──────────────────┐
│ WeaviateService  │ ──► Retrieve document
│                  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ExtractionService │
│  (AI-powered)    │
│                  │
│ ┌──────────────┐ │
│ │   Finance    │ │ ─► Cost analysis
│ └──────────────┘ │    Milestones
│ ┌──────────────┐ │    ROI
│ │Sustainability│ │ ─► Emissions
│ └──────────────┘ │    Recovery
│ ┌──────────────┐ │    Compliance
│ │  Chemistry   │ │ ─► Formulation
│ └──────────────┘ │    Parameters
│                  │    Quality specs
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   FriendliAI     │ (Optional)
│   Llama 3.1 70B  │ ─► AI summaries
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│PerspectiveDash   │
│   board (React)  │
│                  │
│ ┌──────────────┐ │
│ │ Finance Tab  │ │
│ ├──────────────┤ │
│ │Sustain. Tab  │ │
│ ├──────────────┤ │
│ │Chemistry Tab │ │
│ └──────────────┘ │
└──────────────────┘
```

### Stage 3: Chat Interface

```
User asks question
      │
      ▼
POST /api/chat
      │
      ▼
┌──────────────────┐
│   ChatService    │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────┐ ┌──────────┐
│Weaviate │ │FriendliAI│
│ Search  │ │   LLM    │
│         │ │          │
│Relevant │ │Generate  │
│chunks   │ │response  │
└────┬────┘ └────┬─────┘
     │           │
     └─────┬─────┘
           │
           ▼
    ┌─────────────┐
    │  Response   │
    │    with     │
    │  Citations  │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │ChatInterface│
    │   (React)   │
    │             │
    │ - Message   │
    │   history   │
    │ - Sources   │
    │ - Citations │
    └─────────────┘
```

## Component Architecture

### Backend Services

```
backend/
│
├── main.py                    # FastAPI app & endpoints
│   ├── POST /api/upload       # Upload PDF
│   ├── GET /api/documents     # List documents
│   ├── GET /api/documents/:id # Get analysis
│   ├── POST /api/chat         # Chat with doc
│   └── GET /api/search        # Search literature
│
└── services/
    │
    ├── document_processor.py
    │   ├── PDFReader           # Extract text
    │   ├── EntityExtractor     # Find entities
    │   ├── NodeParser          # Chunk text
    │   └── LlamaIndex          # Orchestration
    │
    ├── weaviate_service.py
    │   ├── Connection          # Weaviate client
    │   ├── SchemaManager       # Collection setup
    │   ├── Storage             # Store vectors
    │   └── Search              # Query vectors
    │
    ├── extraction_service.py
    │   ├── FinanceExtractor    # $, milestones
    │   ├── SustainExtractor    # Emissions, recovery
    │   ├── ChemistryExtractor  # Specs, parameters
    │   ├── GraphGenerator      # Knowledge graph
    │   └── FriendliClient      # AI summaries
    │
    └── chat_service.py
        ├── ContextBuilder      # Build prompt context
        ├── FriendliClient      # LLM inference
        ├── CitationExtractor   # Find sources
        └── MockResponder       # Fallback responses
```

### Frontend Components

```
app/
│
├── pages/
│   └── PharmaFlowPage.tsx     # Main container
│       ├── Tabs                # Upload/Analysis/Graph/Chat
│       └── State Management    # Selected doc, refresh
│
└── components/pharma/
    │
    ├── DocumentUpload.tsx
    │   ├── FileInput           # PDF selection
    │   ├── UploadProgress      # Status display
    │   └── APIClient           # POST /api/upload
    │
    ├── DocumentList.tsx
    │   ├── DocumentCard[]      # Document items
    │   ├── Selection           # Active doc highlight
    │   └── APIClient           # GET /api/documents
    │
    ├── PerspectiveDashboard.tsx
    │   ├── TabContainer        # Perspective tabs
    │   ├── FinancePerspective  # $ cards & metrics
    │   ├── SustainPerspective  # Environmental cards
    │   ├── ChemistryPerspective# Process cards
    │   └── APIClient           # GET /api/documents/:id
    │
    ├── KnowledgeGraph.tsx
    │   ├── D3ForceGraph        # Interactive viz
    │   ├── NodeRenderer        # SVG circles
    │   ├── LinkRenderer        # SVG lines
    │   └── APIClient           # graph_data from API
    │
    └── ChatInterface.tsx
        ├── MessageList         # Conversation history
        ├── MessageInput        # User input
        ├── SuggestedPrompts    # Quick questions
        ├── CitationDisplay     # Source links
        └── APIClient           # POST /api/chat
```

## Technology Stack Details

### Backend Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **API Framework** | FastAPI 0.115 | REST endpoints, async support |
| **Document Processing** | LlamaIndex 0.11 | PDF parsing, chunking |
| **Vector Store** | Weaviate 4.9 | Semantic search, embeddings |
| **Embeddings** | HuggingFace BGE | Local embedding model |
| **LLM Inference** | FriendliAI | Fast Llama 3.1 70B |
| **PDF Parsing** | PyPDF 5.1 | Text extraction |
| **Validation** | Pydantic 2.9 | Type checking, validation |

### Frontend Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Framework** | Next.js 14 | React with SSR/SSG |
| **UI Library** | React 18 | Component rendering |
| **Type Safety** | TypeScript 5 | Static typing |
| **Styling** | Tailwind CSS | Utility-first CSS |
| **Components** | Radix UI | Accessible primitives |
| **Visualization** | D3.js 7 | Knowledge graph |
| **State** | React Context | Global state |

## Deployment Architecture

### Development (Local)

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Weaviate   │    │   Backend    │    │   Frontend   │
│    Docker    │    │   Python     │    │   Next.js    │
│  localhost   │◄───┤  localhost   │◄───┤  localhost   │
│    :8080     │    │    :8000     │    │    :3000     │
└──────────────┘    └──────────────┘    └──────────────┘
```

### Production (Recommended)

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Weaviate    │    │   Backend    │    │   Frontend   │
│   Cloud      │    │   Cloud Run  │    │   Vercel     │
│  (Managed)   │◄───┤   or ECS     │◄───┤   (Edge)     │
└──────────────┘    └──────────────┘    └──────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  FriendliAI  │
                    │   API        │
                    │  (External)  │
                    └──────────────┘
```

## Data Models

### Document Model
```python
{
  "document_id": "uuid",
  "filename": "RMX-207.pdf",
  "pages": 50,
  "nodes": [
    {
      "id": "node_uuid",
      "text": "chunk content",
      "metadata": {...}
    }
  ],
  "entities": {
    "products": ["RMX-207"],
    "compounds": ["90%", "mRNA"],
    "parameters": [...],
    "timelines": ["3 months"],
    "costs": ["$190,000"]
  }
}
```

### Analysis Model
```python
{
  "document_id": "uuid",
  "finance": {
    "total_cost": "$190,000",
    "cost_breakdown": {...},
    "milestones": [...],
    "summary": "text"
  },
  "sustainability": {
    "waste_recovery": {...},
    "emissions": {...},
    "summary": "text"
  },
  "chemistry": {
    "formulation": {...},
    "process_parameters": {...},
    "quality_specs": {...},
    "summary": "text"
  },
  "graph_data": {
    "nodes": [...],
    "links": [...]
  }
}
```

### Chat Model
```python
{
  "document_id": "uuid",
  "message": "What are specs?",
  "conversation_history": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}

# Response:
{
  "response": "The specifications are...",
  "citations": [
    {
      "source": "RMX-207.pdf",
      "content": "excerpt...",
      "relevance": "primary"
    }
  ],
  "sources": ["RMX-207.pdf"]
}
```

## Scalability Considerations

### Current Implementation
- **Concurrent Users**: 10-50
- **Documents**: 100s
- **Response Time**: <2s (with API keys)
- **Storage**: In-memory + Weaviate

### Scale-Up Path
1. **Add Redis cache** for frequently accessed documents
2. **Celery task queue** for async processing
3. **PostgreSQL** for document metadata
4. **CDN** for static assets
5. **Load balancer** for backend replicas
6. **Weaviate cluster** for high availability

## Security Considerations

### Implemented
- ✅ CORS configuration
- ✅ Input validation (Pydantic)
- ✅ File type checking (.pdf only)
- ✅ Environment variable secrets

### Production TODO
- [ ] Authentication (JWT)
- [ ] Rate limiting
- [ ] API key management
- [ ] File size limits
- [ ] Malware scanning
- [ ] Encrypted data at rest
- [ ] Audit logging

---

For implementation details, see:
- Backend: `backend/main.py` and `backend/services/`
- Frontend: `app/pages/PharmaFlowPage.tsx` and `app/components/pharma/`

