#!/bin/bash

echo "🚀 Starting Port Monitor..."
echo "================================================"

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the port-monitor directory."
    exit 1
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    
    # Install requirements in new venv
    echo "📥 Installing requirements..."
    venv/bin/pip install -r requirements.txt
else
    # Check if requirements are installed
    if ! venv/bin/python3 -c "import flask" 2>/dev/null; then
        echo "📥 Installing requirements..."
        venv/bin/pip install -r requirements.txt
    fi
fi

# Check if port 8080 is available
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 8080 is already in use!"
    echo "   To find what's using it: lsof -i :8080"
    echo "   To kill it: kill -9 \$(lsof -ti :8080)"
    echo ""
    echo "   The dashboard will try to start anyway..."
fi

echo "🚀 Starting Port Monitor server..."
echo "   Dashboard: http://localhost:8080"
echo "   API: http://localhost:8080/api/ports"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================================"

# Start the Flask app using venv python directly
venv/bin/python3 app.py