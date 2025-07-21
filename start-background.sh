#!/bin/bash

echo "🖥️  Starting Port Monitor in Background..."

# Check if dashboard is already running
if curl -s http://localhost:8080/api/health > /dev/null 2>&1; then
    echo "✅ Port Monitor is already running!"
    echo "🌐 Access at: http://localhost:8080"
    exit 0
fi

# Kill any existing dashboard processes
pkill -f "python.*app.py" 2>/dev/null || true

# Start dashboard in background
nohup ./start.sh > port-monitor.log 2>&1 &
DASHBOARD_PID=$!

echo "🚀 Port Monitor started in background (PID: $DASHBOARD_PID)"
echo "📝 Logs: tail -f port-monitor.log"

# Wait for dashboard to be ready
echo "⏳ Waiting for Port Monitor to start..."
for i in {1..20}; do
    if curl -s http://localhost:8080/api/health > /dev/null 2>&1; then
        echo "✅ Port Monitor is ready!"
        echo ""
        echo "🌐 Dashboard: http://localhost:8080"
        echo "🔌 API: http://localhost:8080/api/ports"
        echo "📊 Health: http://localhost:8080/api/health"
        echo ""
        echo "📝 View logs: tail -f port-monitor.log"
        echo "⏹️  Stop: ./stop.sh"
        echo ""
        
        # Test the dashboard
        echo "🧪 Quick test:"
        curl -s http://localhost:8080/api/health | python3 -m json.tool 2>/dev/null || echo "API responding"
        
        exit 0
    fi
    
    echo "   Waiting... ($i/20)"
    sleep 1
done

echo "❌ Port Monitor failed to start. Check port-monitor.log for errors."
exit 1