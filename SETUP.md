# PharmaFlow Setup Guide

## Quick Start (Recommended)

### Option 1: Docker Compose (Easiest)

1. **Prerequisites**: Docker and Docker Compose installed

2. **Set environment variables**:
```bash
# Create .env file in project root
echo "FRIENDLI_TOKEN=your_friendli_token_here" > .env
```

3. **Start all services**:
```bash
docker-compose up -d
```

4. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Weaviate: http://localhost:8080

5. **View logs**:
```bash
docker-compose logs -f
```

6. **Stop services**:
```bash
docker-compose down
```

### Option 2: Manual Setup (Development)

#### Step 1: Start Weaviate

**Using Docker**:
```bash
docker run -d \
  -p 8080:8080 \
  -p 50051:50051 \
  --name weaviate \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  semitechnologies/weaviate:latest
```

**Or use Weaviate Cloud**: Sign up at https://console.weaviate.cloud/

#### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
WEAVIATE_URL=http://localhost:8080
WEAVIATE_API_KEY=
FRIENDLI_TOKEN=your_friendli_token_here
OPENAI_API_KEY=
EOF

# Start backend server
python main.py
```

Backend will be available at http://localhost:8000

#### Step 3: Frontend Setup

```bash
# Return to project root
cd ..

# Install Node dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at http://localhost:3000

## API Keys Setup

### 1. FriendliAI Token

PharmaFlow uses FriendliAI for fast LLM inference.

1. Sign up at https://friendli.ai/
2. Get your API token from the dashboard
3. Add to `.env`: `FRIENDLI_TOKEN=your_token`

**Note**: The app will work without FriendliAI by using fallback mock responses, but the AI features will be limited.

### 2. Weaviate Setup

**Local (Docker)**:
- No API key needed
- Just set `WEAVIATE_URL=http://localhost:8080`

**Cloud (Recommended for production)**:
1. Sign up at https://console.weaviate.cloud/
2. Create a cluster
3. Get your cluster URL and API key
4. Update `.env`:
   ```
   WEAVIATE_URL=https://your-cluster.weaviate.network
   WEAVIATE_API_KEY=your_api_key
   ```

### 3. Optional: OpenAI API Key

If you want to use OpenAI embeddings instead of local HuggingFace embeddings:
```
OPENAI_API_KEY=your_openai_key
```

## Verify Installation

### 1. Check Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "services": {
    "weaviate": true,
    "document_processor": true,
    "extraction": true,
    "chat": true
  }
}
```

### 2. Test Frontend

1. Open http://localhost:3000
2. Click "PharmaFlow" in the sidebar
3. You should see the upload interface

## Troubleshooting

### Backend Issues

**"Could not connect to Weaviate"**
- Check if Weaviate is running: `docker ps | grep weaviate`
- Verify Weaviate URL in `.env`
- Try accessing http://localhost:8080/v1/.well-known/ready

**"friendli package not available"**
- The app will work with mock responses
- To enable AI features, install: `pip install friendli-client`
- Add your FRIENDLI_TOKEN to `.env`

**"Module not found" errors**
- Ensure virtual environment is activated
- Run: `pip install -r requirements.txt`

### Frontend Issues

**"Cannot connect to backend"**
- Verify backend is running at http://localhost:8000
- Check CORS settings in `backend/main.py`
- Ensure port 8000 is not blocked

**"Module not found" errors**
- Run: `npm install`
- Clear cache: `rm -rf .next node_modules && npm install`

**D3.js visualization not showing**
- Install D3: `npm install d3 @types/d3`
- Check browser console for errors

### Docker Issues

**Services won't start**
```bash
# Check logs
docker-compose logs

# Rebuild images
docker-compose build --no-cache

# Reset everything
docker-compose down -v
docker-compose up --build
```

**Port conflicts**
- Change ports in `docker-compose.yml` if 3000, 8000, or 8080 are in use

## Development Tips

### Hot Reload

Both frontend and backend support hot reload:
- **Frontend**: Save any file and Next.js will auto-refresh
- **Backend**: FastAPI with `reload=True` will restart on file changes

### Testing the API

Use the interactive API docs:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Sample Test Flow

1. **Upload a test PDF**:
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_document.pdf"
```

2. **List documents**:
```bash
curl http://localhost:8000/api/documents
```

3. **Get analysis** (replace with your document_id):
```bash
curl http://localhost:8000/api/documents/{document_id}
```

4. **Chat with document**:
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "your_document_id",
    "message": "What are the specifications?",
    "conversation_history": []
  }'
```

## Production Deployment

### Environment Variables for Production

```bash
# Backend .env
WEAVIATE_URL=https://your-cluster.weaviate.network
WEAVIATE_API_KEY=your_production_key
FRIENDLI_TOKEN=your_production_token

# Frontend .env.production
NEXT_PUBLIC_API_URL=https://your-api-domain.com
```

### Build for Production

**Backend**:
```bash
cd backend
pip install -r requirements.txt
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

**Frontend**:
```bash
npm run build
npm start
```

### Deployment Options

- **Frontend**: Vercel, Netlify, AWS Amplify
- **Backend**: AWS ECS, Google Cloud Run, Heroku, Railway
- **Database**: Weaviate Cloud (managed)

## Need Help?

- Check API docs: http://localhost:8000/docs
- Review logs: `docker-compose logs -f`
- File an issue on GitHub

---

Happy hacking! 🚀

