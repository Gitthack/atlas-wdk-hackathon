#!/bin/bash
# Serve dashboard on public IP for mobile access

cd /root/.openclaw/workspace/atlas-hackathon

echo "==============================================="
echo "Starting Atlas Dashboard - Mobile Access"
echo "==============================================="
echo ""

# Generate fresh static HTML
python3 export_dashboard.py

# Get IP address
IP=$(hostname -I | awk '{print $1}')
PORT=8080

echo "📱 To view on your phone:"
echo ""
echo "   1. Make sure your phone is on the same WiFi/network"
echo "   2. Open browser on your phone"
echo "   3. Go to: http://$IP:$PORT"
echo ""
echo "   Or scan this address: http://$IP:$PORT"
echo ""
echo "⚠️  Press Ctrl+C to stop"
echo "==============================================="

# Start simple HTTP server
python3 -m http.server $PORT
