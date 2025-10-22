#!/bin/bash

echo "🚀 Starting PharmaFlow..."
echo ""

# Check if .env exists in backend
if [ ! -f "backend/.env" ]; then
    echo "⚠️  No backend/.env file found. Creating from example..."
    cp backend/.env.example backend/.env
    echo "✅ Created backend/.env - Please add your API keys!"
    echo ""
fi

# Check if docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Start Weaviate if not running
if ! docker ps | grep -q weaviate; then
    echo "📦 Starting Weaviate..."
    docker run -d \
      -p 8080:8080 \
      -p 50051:50051 \
      --name weaviate \
      -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
      -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
      semitechnologies/weaviate:latest
    echo "✅ Weaviate started on port 8080"
    sleep 3
else
    echo "✅ Weaviate already running"
fi

# Start backend
echo ""
echo "🐍 Starting Python backend..."
cd backend

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv and install dependencies
source venv/bin/activate
pip install -q -r requirements.txt

# Start backend in background
python main.py &
BACKEND_PID=$!
echo "✅ Backend started on port 8000 (PID: $BACKEND_PID)"

cd ..

# Start frontend
echo ""
echo "⚛️  Starting Next.js frontend..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

# Start frontend
npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend started on port 3000 (PID: $FRONTEND_PID)"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 PharmaFlow is ready!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📱 Frontend:  http://localhost:3000"
echo "🔧 Backend:   http://localhost:8000"
echo "📚 API Docs:  http://localhost:8000/docs"
echo "🗄️  Weaviate: http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop all services"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Wait for interrupt
trap "echo ''; echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; docker stop weaviate 2>/dev/null; echo '✅ All services stopped'; exit 0" INT

wait

