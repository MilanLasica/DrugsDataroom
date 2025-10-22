from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
import os
from dotenv import load_dotenv

from services.document_processor import DocumentProcessor
from services.weaviate_service import WeaviateService
from services.extraction_service import ExtractionService
from services.chat_service import ChatService

load_dotenv()

app = FastAPI(title="PharmaFlow API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
document_processor = DocumentProcessor()
weaviate_service = WeaviateService()
extraction_service = ExtractionService()
chat_service = ChatService(weaviate_service)


# Pydantic models
class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    pages: int
    status: str


class ExtractionResponse(BaseModel):
    document_id: str
    finance: Dict[str, Any]
    sustainability: Dict[str, Any]
    chemistry: Dict[str, Any]
    graph_data: Dict[str, Any]


class ChatRequest(BaseModel):
    document_id: str
    message: str
    conversation_history: Optional[List[Dict[str, str]]] = []


class ChatResponse(BaseModel):
    response: str
    citations: List[Dict[str, Any]]
    sources: List[str]


@app.get("/")
async def root():
    return {"message": "PharmaFlow API", "status": "running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "services": {
        "weaviate": weaviate_service.is_connected(),
        "document_processor": True,
        "extraction": True,
        "chat": True
    }}


@app.post("/api/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a pharmaceutical document (PDF)"""
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Save uploaded file
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process document
        result = await document_processor.process_document(file_path, file.filename)
        
        # Store in Weaviate
        await weaviate_service.store_document(result)
        
        return DocumentUploadResponse(
            document_id=result["document_id"],
            filename=file.filename,
            pages=result["pages"],
            status="processed"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/documents")
async def list_documents():
    """List all uploaded documents"""
    try:
        documents = await weaviate_service.list_documents()
        return {"documents": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/documents/{document_id}", response_model=ExtractionResponse)
async def get_document_analysis(document_id: str):
    """Get multi-perspective analysis of a document"""
    try:
        # Retrieve document from Weaviate
        document = await weaviate_service.get_document(document_id)
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Extract multi-perspective insights
        analysis = await extraction_service.extract_perspectives(document)
        
        return ExtractionResponse(
            document_id=document_id,
            finance=analysis["finance"],
            sustainability=analysis["sustainability"],
            chemistry=analysis["chemistry"],
            graph_data=analysis["graph_data"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_document(request: ChatRequest):
    """Chat with a document using AI agent"""
    try:
        response = await chat_service.process_query(
            document_id=request.document_id,
            message=request.message,
            conversation_history=request.conversation_history
        )
        
        return ChatResponse(
            response=response["answer"],
            citations=response["citations"],
            sources=response["sources"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/search")
async def search_literature(query: str, limit: int = 5):
    """Search for related literature using Weaviate"""
    try:
        results = await weaviate_service.search_literature(query, limit)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import os
    venv_path = os.path.join(os.path.dirname(__file__), "venv")
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True, 
        reload_dirs=[os.path.dirname(__file__)],
        reload_excludes=[venv_path, "venv"]
    )

