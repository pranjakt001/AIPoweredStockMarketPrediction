#!/bin/bash

# Development Startup Script

echo "🔧 Starting Development Server..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
mkdir -p logs data/raw data/processed data/models

# Copy environment file
if [ ! -f ".env" ]; then
    cp .env.example .env
fi

# Run development server
export FLASK_APP=backend/app.py
export FLASK_ENV=development

echo "🌐 Starting Flask development server on http://localhost:5000"
echo "📱 Open frontend/index.html in your browser"
echo ""
echo "Press Ctrl+C to stop the server"

python -m flask run --host=0.0.0.0 --port=5000
