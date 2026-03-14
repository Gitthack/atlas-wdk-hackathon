#!/usr/bin/env python3
"""
Atlas Dashboard
Real-time economic dashboard for Atlas agent
"""
import os
import sys
import json
from datetime import datetime
from flask import Flask, render_template, jsonify

sys.path.insert(0, 'src/wdk_wallet')
sys.path.insert(0, 'src/atlas_core')

from wallet import AtlasWallet
from integration import AtlasWDKIntegration

app = Flask(__name__)

# Initialize Atlas
atlas = AtlasWDKIntegration()

@app.route('/')
def dashboard():
    """Main dashboard page."""
    return render_template('dashboard.html')

@app.route('/api/status')
def api_status():
    """API endpoint for agent status."""
    try:
        status = atlas.get_economic_status()
        return jsonify({
            'success': True,
            'data': status
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/transactions')
def api_transactions():
    """API endpoint for transaction history."""
    try:
        txs = atlas.wallet.get_transaction_history(limit=20)
        return jsonify({
            'success': True,
            'data': txs
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/ledger')
def api_ledger():
    """API endpoint for ledger export."""
    try:
        ledger = atlas.export_on_chain_proof()
        return jsonify({
            'success': True,
            'data': json.loads(ledger)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("=" * 60)
    print("Atlas Dashboard")
    print("=" * 60)
    print(f"\n🚀 Starting server...")
    print(f"📍 Open: http://localhost:5000")
    print(f"📊 API: http://localhost:5000/api/status")
    print(f"\n⚠️  Press Ctrl+C to stop")
    print("=" * 60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
