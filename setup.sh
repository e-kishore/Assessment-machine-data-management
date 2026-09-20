#!/bin/bash

# Machine Data Management - Setup Script
# This script sets up everything you need to run the application

echo "🚀 Setting up Machine Data Management Application..."
echo ""

# Check Python version
echo "✓ Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

python_version=$(python3 --version)
echo "  Found: $python_version"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "  ✓ Dependencies installed"
echo ""

# Create ML model
echo "🤖 Training ML model..."
python3 ml_model.py

if [ $? -ne 0 ]; then
    echo "❌ Failed to create ML model"
    exit 1
fi

echo "  ✓ ML model created (risk_model.pkl)"
echo ""

echo ""
echo "✅ Setup complete!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎯 Next steps:"
echo ""
echo "1️⃣  Start the FastAPI backend server (Terminal 1):"
echo "   python main.py"
echo ""
echo "2️⃣  In another terminal, start a web server (Terminal 2):"
echo "   python -m http.server 3000"
echo ""
echo "3️⃣  Open your browser and go to:"
echo "   http://localhost:3000/frontend.html"
echo ""
echo "💡 FastAPI runs on: http://localhost:8000"
echo "📚 API docs at: http://localhost:8000/docs"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📚 Learn more: Read LEARNING_GUIDE.md"
echo "📖 Full documentation: Read README.md"
echo ""