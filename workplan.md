# Smart Data Package — Hackathon Workplan (4 hours total, 4 people)

## Goal
By the end of the hackathon, demo a simple app that:
1. Uploads a PDF (the provided 50-page demo file),
2. Indexes it in Weaviate via LlamaIndex,
3. Lets users ask natural language questions, answered through RAG powered by FriendliAI.

---

## Roles & Tasks

### **Hour 0–1: Setup and Environment**
**Owner:** Person A (Infra)
- Spin up local Weaviate instance or use Weaviate Cloud (free tier).  
- Set up environment variables for FriendliAI and LlamaIndex.  
- Initialize repo structure: `backend/`, `frontend/`, `data/`.

### **Hour 1–2: Backend Core**
**Owner:** Person B (Backend)
- Implement `/ingest` endpoint: upload → parse PDF → chunk → embed → store in Weaviate.  
- Implement `/query` endpoint: take user query → retrieve top-k → send context to FriendliAI → return answer.

**Libraries:** `llama_index`, `weaviate-client`, `fastapi`, `friendliai-sdk`

---

### **Hour 2–3: Frontend**
**Owner:** Person C (Frontend)
- Simple Streamlit (or Gradio) UI:
  - File upload
  - Text box for questions
  - Display response and citations (page numbers if possible)

---

### **Hour 3–4: Integration & Demo Polish**
**Owner:** Person D (Integration)
- Connect backend and frontend endpoints.  
- Test with the demo PDF: ask 5 example questions (“What’s the target yield?”, “List FTE requirements”).  
- Add 1–2 example screenshots or short Loom video for demo.  
- Prepare final pitch: *“Today, we built an AI that reads tech transfer packages so CDMOs can ask questions instead of digging through PDFs.”*

---

## Stretch Goals (if time remains)
- Add metadata filters (by section or page).
- Cache embeddings locally.
- Add “multi-perspective” extraction stub (Finance / FTE / Sustainability cards).

---

**Deliverable:**  
A minimal RAG prototype showing full stack integration:  
**Weaviate (storage)** + **LlamaIndex (retrieval)** + **FriendliAI (LLM inference)**.
