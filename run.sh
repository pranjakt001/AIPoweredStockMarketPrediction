#!/bin/bash

# Production Startup Script for Stock Market Prediction System

echo "🚀 Starting AI Stock Market Prediction System..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs data/raw data/processed data/models

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
fi

# Start the backend server
echo "🌐 Starting backend server..."
export FLASK_APP=backend/app.py
export FLASK_ENV=production

# Run with gunicorn for production
gunicorn --bind 0.0.0.0:5000 \
         --workers 4 \
         --timeout 120 \
         --access-logfile logs/access.log \
         --error-logfile logs/error.log \
         --log-level info \
         'backend.app:create_app()'
