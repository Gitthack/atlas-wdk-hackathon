#!/bin/bash
# Atlas Daily Full Scan - Manual trigger
cd /root/.openclaw/workspace/scripts

# Export tokens if available
export GITHUB_TOKEN="${GITHUB_TOKEN:-}"
export OPENAI_API_KEY="${OPENAI_API_KEY:-}"

echo "======================================"
echo "🚀 ATLAS DAILY FULL SCAN"
echo "======================================"
echo "Time: $(date)"
echo ""

# Run full platform scanner
python3 atlas_full_scanner.py

echo ""
echo "======================================"
echo "Scan complete. Check ~/.atlas/ for results."
echo "======================================"
