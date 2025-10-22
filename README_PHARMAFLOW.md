# PharmaFlow - AI-Driven Drug Manufacturing Assistant

![PharmaFlow](https://img.shields.io/badge/Hackathon-PharmaFlow-blue)
![Stack](https://img.shields.io/badge/Stack-LlamaIndex%20%7C%20Weaviate%20%7C%20FriendliAI-green)

## 🚀 Overview

PharmaFlow transforms dense pharmaceutical manufacturing documents (PDFs, RFPs, technical specs) into structured, searchable intelligence. It enables drug sponsors and CDMOs to communicate more effectively by extracting multi-perspective insights and providing an intelligent conversational interface.

## ✨ Features

### 📄 Stage 1: Data Ingestion & Literature Scraping
- **PDF Upload**: Upload pharmaceutical documents (RFPs, technical specifications, manufacturing briefs)
- **Entity Extraction**: Automatically extract products, formulations, parameters, timelines, and costs using LlamaIndex
- **Knowledge Linking**: Connect document requirements to existing literature and best practices via Weaviate vector search

### 🔍 Stage 2: Multi-Perspective Analysis
Extract and categorize insights across three key domains:

- **💰 Finance**: Cost breakdowns, payment milestones, budget allocations, ROI considerations
- **🌱 Sustainability**: Waste recovery, emissions targets, energy efficiency, environmental compliance
- **⚗️ Chemistry/Process**: Formulation details, process parameters, quality specs, critical manufacturing steps

Each perspective provides:
- Structured data extraction
- AI-powered summaries (via FriendliAI)
- Domain-specific metrics and requirements

### 💬 Stage 3: Manufacturing Agent Interface
- **Conversational AI**: Chat with your documents in natural language
- **Real-time Responses**: Powered by FriendliAI's ultra-low-latency inference
- **Cited Answers**: Every response includes source citations and relevant literature
- **Context-Aware**: Maintains conversation history for follow-up questions

### 📊 Knowledge Graph Visualization
- **Interactive D3.js Graph**: Visualize relationships between requirements, processes, and specifications
- **Category Nodes**: Finance, Sustainability, Chemistry connected to specific metrics
- **Drag & Zoom**: Explore the knowledge graph interactively

## 🏗️ Architecture

### Backend (Python/FastAPI)
```
backend/
├── main.py                    # FastAPI application
├── services/
│   ├── document_processor.py  # LlamaIndex PDF processing
│   ├── weaviate_service.py    # Vector store integration
│   ├── extraction_service.py  # Multi-perspective extraction
│   └── chat_service.py         # Conversational agent
└── requirements.txt
```

### Frontend (Next.js/React)
```
app/
├── pages/
│   └── PharmaFlowPage.tsx     # Main application page
└── components/pharma/
    ├── DocumentUpload.tsx      # PDF upload interface
    ├── DocumentList.tsx        # Document management
    ├── PerspectiveDashboard.tsx # Multi-perspective UI
    ├── ChatInterface.tsx       # Conversational agent UI
    └── KnowledgeGraph.tsx      # D3.js visualization
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Document Processing** | LlamaIndex |
| **Vector Search** | Weaviate |
| **LLM Inference** | FriendliAI (Llama 3.1 70B) |
| **Backend** | FastAPI + Python |
| **Frontend** | Next.js + React + TypeScript |
| **Visualization** | D3.js |
| **UI Components** | Radix UI + Tailwind CSS |

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker (optional, for Weaviate)

### Backend Setup

1. **Navigate to backend directory**:
```bash
cd backend
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env with your API keys:
# - FRIENDLI_TOKEN=your_friendli_token
# - WEAVIATE_URL=http://localhost:8080 (or cloud URL)
# - WEAVIATE_API_KEY=your_key (if using cloud)
```

5. **(Optional) Run Weaviate locally**:
```bash
docker run -d \
  -p 8080:8080 \
  -p 50051:50051 \
  --name weaviate \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  semitechnologies/weaviate:latest
```

6. **Start the backend**:
```bash
python main.py
```
Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Install dependencies**:
```bash
npm install
```

2. **Run development server**:
```bash
npm run dev
```
Frontend will be available at `http://localhost:3000`

3. **Navigate to PharmaFlow**:
   - Open `http://localhost:3000`
   - Click "PharmaFlow" in the sidebar

## 📖 Usage

### 1. Upload a Document
- Click the "PharmaFlow" tab in the sidebar
- Upload a pharmaceutical PDF (manufacturing spec, RFP, technical brief)
- Wait for processing (entity extraction and embedding)

### 2. View Multi-Perspective Analysis
- Select your document from the list
- Navigate to the "Analysis" tab
- Explore Finance, Sustainability, and Chemistry perspectives
- View extracted metrics, summaries, and requirements

### 3. Explore Knowledge Graph
- Navigate to the "Graph" tab
- Interact with the D3.js visualization
- See relationships between document elements
- Drag nodes to explore connections

### 4. Chat with Your Document
- Navigate to the "Chat" tab
- Ask questions about specifications, costs, timelines, etc.
- Use suggested prompts or type your own
- Get AI-powered answers with citations

### Example Questions
- "What are the LNP formulation specifications?"
- "What is the CO₂ emission limit per vial?"
- "What are the payment milestones?"
- "What is the ethanol recovery target?"
- "What is the batch size and manufacturing time?"

## 🎯 Impact

### Before PharmaFlow
- ⏱️ Days spent deciphering 50-100 page technical PDFs
- 📧 Miscommunication between sponsors and manufacturers
- 🔍 Difficulty finding specific requirements
- ⚠️ Missed sustainability or compliance details

### After PharmaFlow
- ⚡ **Minutes** to extract and understand all requirements
- 📊 **Structured** multi-perspective insights
- 💬 **Conversational** access to all information
- ✅ **Complete** coverage of all requirement categories

### Key Benefits
1. **Faster Tech Transfer**: Reduce interpretation time from weeks to hours
2. **Better Communication**: Clear, categorized requirements for all stakeholders
3. **Sustainability Alignment**: Explicit tracking of environmental targets
4. **Cost Transparency**: Clear visibility into financial requirements
5. **Process Clarity**: Detailed chemistry and manufacturing parameters

## 🏆 Hackathon Demo Flow

1. **Upload RMX-207 Technical Specification** (50-page PDF)
2. **Show Multi-Perspective Dashboard**:
   - Finance: $190K per batch, milestone payments
   - Sustainability: 85% ethanol recovery, <0.5kg CO₂/vial
   - Chemistry: 90% encapsulation efficiency, 80-120nm particle size
3. **Explore Knowledge Graph**: Visualize connections between requirements
4. **Chat Demo**:
   - "What are the specifications for RMX-207's LNP formulation?"
   - "What's the CO₂ limit per vial?"
   - "What payment milestone triggers batch release?"
5. **Show Real-time Responses** with citations from document

## 🔮 Future Enhancements

- [ ] Multi-document comparison and analysis
- [ ] Regulatory compliance checking (FDA, EMA guidelines)
- [ ] Automated RFP response generation
- [ ] Timeline and milestone tracking
- [ ] Cost estimation and optimization suggestions
- [ ] Integration with manufacturing execution systems (MES)
- [ ] Real-time collaboration features
- [ ] Advanced analytics and insights dashboard

## 📝 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/upload` | POST | Upload pharmaceutical PDF |
| `/api/documents` | GET | List all documents |
| `/api/documents/{id}` | GET | Get multi-perspective analysis |
| `/api/chat` | POST | Chat with document |
| `/api/search` | GET | Search related literature |

## 🤝 Contributing

This is a hackathon project! Contributions, issues, and feature requests are welcome.

## 📄 License

See LICENSE file for details.

## 🙏 Acknowledgments

- **LlamaIndex** - Document processing and indexing
- **Weaviate** - Vector search and embeddings
- **FriendliAI** - Fast LLM inference
- **Elysia** - Base template and architecture

---

Built with ❤️ for the hackathon by [Your Team Name]

