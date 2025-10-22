# PharmaFlow - Quick Reference Card

## 🚀 One-Command Start
```bash
./start.sh
```
Then open: http://localhost:3000 → Click "PharmaFlow" in sidebar

## 🎯 Demo URLs
- **App**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Weaviate**: http://localhost:8080

## 📁 Project Structure
```
DrugsDataroom/
├── backend/              ← Python/FastAPI backend
│   ├── main.py          ← API endpoints
│   └── services/        ← LlamaIndex, Weaviate, FriendliAI
├── app/
│   ├── pages/
│   │   └── PharmaFlowPage.tsx  ← Main app
│   └── components/pharma/      ← All UI components
└── Documentation files
```

## 🎨 Features Checklist
- [x] PDF Upload (Stage 1)
- [x] Entity Extraction (Stage 1)
- [x] Vector Search (Stage 1)
- [x] Finance Dashboard (Stage 2)
- [x] Sustainability Dashboard (Stage 2)
- [x] Chemistry Dashboard (Stage 2)
- [x] Chat Agent (Stage 3)
- [x] Knowledge Graph (Bonus)

## 🔑 Environment Setup
```bash
# Copy template to backend
cp .env.template backend/.env

# Edit with your keys
FRIENDLI_TOKEN=your_token_here
WEAVIATE_URL=http://localhost:8080
```

## 💬 Demo Queries
Try these in the chat interface:
1. "What are the LNP formulation specifications?"
2. "What is the CO₂ emission limit?"
3. "What are the payment milestones?"
4. "What is the ethanol recovery target?"
5. "What is the batch size?"

## 🐛 Troubleshooting

**Backend won't start?**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```

**Frontend won't start?**
```bash
npm install
npm run dev
```

**Weaviate not running?**
```bash
docker run -d -p 8080:8080 --name weaviate \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  semitechnologies/weaviate:latest
```

**Port already in use?**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

## 📊 Tech Stack
- **Document**: LlamaIndex
- **Search**: Weaviate
- **AI**: FriendliAI (Llama 3.1)
- **Backend**: FastAPI/Python
- **Frontend**: Next.js/React
- **Viz**: D3.js

## 🎤 Elevator Pitch
*"PharmaFlow transforms 50-page pharmaceutical documents into structured intelligence in minutes. Upload an RFP, get instant multi-perspective analysis across finance, sustainability, and chemistry, then chat with your document using AI. What took weeks now takes minutes."*

## ⏱️ 30-Second Demo
1. Upload PDF (10s)
2. Show Analysis tab - toggle between Finance/Sustainability/Chemistry (10s)
3. Show Graph visualization (5s)
4. Ask a question in Chat (5s)

## 📞 Quick Help
- Full docs: `README_PHARMAFLOW.md`
- Setup guide: `SETUP.md`
- Demo script: `DEMO.md`
- Summary: `PHARMAFLOW_SUMMARY.md`

## 🏆 Key Differentiators
1. ✅ Complete 3-stage pipeline implemented
2. ✅ Works offline (mock data included)
3. ✅ Production-ready code
4. ✅ Beautiful, polished UI
5. ✅ Full documentation

## 🎁 Bonus Features
- Interactive D3.js knowledge graph
- Real-time chat with citations
- Suggested prompts
- Responsive design
- Error handling
- Loading states

---

**Need more details?** See `PHARMAFLOW_SUMMARY.md`
**Ready to present?** See `DEMO.md`

