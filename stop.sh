#!/bin/bash

echo "⏹️  Stopping Port Monitor..."

# Find and kill dashboard processes
PIDS=$(pgrep -f "python.*app.py" 2>/dev/null)

if [ -z "$PIDS" ]; then
    echo "ℹ️  No Port Monitor processes found."
else
    echo "🔍 Found Port Monitor processes: $PIDS"
    kill $PIDS
    sleep 2
    
    # Check if processes are still running
    REMAINING=$(pgrep -f "python.*app.py" 2>/dev/null)
    if [ -n "$REMAINING" ]; then
        echo "⚠️  Some processes still running, force killing: $REMAINING"
        kill -9 $REMAINING
    fi
    
    echo "✅ Port Monitor stopped successfully"
fi

# Also check port 8080 specifically
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Something else is using port 8080:"
    lsof -i :8080
    echo ""
    echo "To kill it: kill -9 \$(lsof -ti :8080)"
else
    echo "🔓 Port 8080 is now available"
fi