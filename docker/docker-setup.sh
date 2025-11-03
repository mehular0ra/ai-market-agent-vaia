#!/bin/bash

echo "🐳 Setting up AI Market Analyst with Docker"
echo "==========================================="
echo ""

if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "Please create .env file with your OPENAI_API_KEY"
    echo "Example: cp .env.example .env"
    exit 1
fi

source .env

if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Error: OPENAI_API_KEY not set in .env"
    exit 1
fi

echo "✅ Environment variables loaded"
echo ""

echo "🔨 Building Docker images..."
docker-compose build

echo ""
echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 10

echo ""
echo "🗄️  Initializing database..."
docker-compose exec api uv run python app/init_db.py

echo ""
echo "📄 Processing document..."
docker-compose exec api uv run python app/process_document.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 API is running at: http://localhost:8000"
echo "📚 API docs at: http://localhost:8000/docs"
echo ""
echo "🧪 Test the API:"
echo "  curl http://localhost:8000/health"
echo ""
echo "📊 View logs:"
echo "  docker-compose logs -f api"
echo ""
echo "🛑 Stop services:"
echo "  docker-compose down"

