#!/bin/bash
# QueryFlux - Startup Script for Linux/Mac
# This script starts the Flask application

echo ""
echo "===================================================================="
echo "  🚀 QueryFlux - PDF Question Answering & Summarization System"
echo "===================================================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
    echo ""
    echo "Installing dependencies..."
    ./.venv/bin/pip install -r req.txt
    echo "✓ Dependencies installed"
    echo ""
fi

# Activate virtual environment and start Flask
echo "Starting QueryFlux..."
echo ""
source ./.venv/bin/activate
python app.py

# If Flask stops, show message
echo ""
echo "===================================================================="
echo "  Flask application stopped"
echo "===================================================================="
