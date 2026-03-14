#!/usr/bin/env python3
"""
Export dashboard as static HTML for mobile viewing
"""
import os
import sys
import json
from datetime import datetime

sys.path.insert(0, 'src/wdk_wallet')
sys.path.insert(0, 'src/atlas_core')

from wallet import AtlasWallet
from integration import AtlasWDKIntegration

def generate_static_html():
    """Generate static HTML dashboard."""
    
    # Get data
    atlas = AtlasWDKIntegration()
    status = atlas.get_economic_status()
    txs = atlas.wallet.get_transaction_history(limit=10)
    
    wallet_data = status['wallet']
    
    # Build transaction HTML
    tx_html = ""
    for tx in txs:
        tx_type = tx['type']
        amount = tx['amount']
        token = tx['token']
        source = tx.get('source', tx.get('category', 'Unknown'))
        color = "#22c55e" if tx_type == 'income' else "#ef4444"
        sign = "+" if tx_type == 'income' else "-"
        
        tx_html += f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 15px; background: #0a0a0a; border-radius: 8px; margin-bottom: 10px;">
            <div>
                <div style="font-weight: bold; color: {color}; text-transform: uppercase;">{tx_type}</div>
                <div style="color: #666; font-size: 0.85em; margin-top: 5px;">{source}</div>
            </div>
            <div style="font-family: monospace; font-size: 1.1em; color: {color};">
                {sign}${amount:.2f} {token}
            </div>
        </div>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Atlas - Self-Custodial Bounty Hunter</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0a0a0a; color: #fff; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        header {{ text-align: center; padding: 40px 0; border-bottom: 1px solid #333; }}
        header h1 {{ font-size: 2.5em; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; }}
        header p {{ color: #888; font-size: 1.1em; }}
        .status-badge {{ display: inline-block; padding: 8px 16px; background: #22c55e; color: #000; border-radius: 20px; font-weight: bold; margin-top: 15px; }}
        .grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top: 30px; }}
        @media (min-width: 768px) {{ .grid {{ grid-template-columns: repeat(4, 1fr); }} }}
        .card {{ background: #1a1a1a; border-radius: 12px; padding: 20px; border: 1px solid #333; }}
        .card h2 {{ font-size: 0.8em; text-transform: uppercase; color: #888; margin-bottom: 10px; letter-spacing: 1px; }}
        .card .value {{ font-size: 1.8em; font-weight: bold; color: #fff; }}
        .card .sub-value {{ font-size: 0.85em; color: #666; margin-top: 5px; }}
        .positive {{ color: #22c55e; }}
        .negative {{ color: #ef4444; }}
        .neutral {{ color: #3b82f6; }}
        .wallet-info, .transactions {{ background: #1a1a1a; border-radius: 12px; padding: 20px; margin-top: 20px; border: 1px solid #333; }}
        .wallet-info h2, .transactions h2 {{ color: #888; font-size: 0.8em; text-transform: uppercase; margin-bottom: 15px; }}
        .address {{ font-family: monospace; background: #0a0a0a; padding: 12px; border-radius: 8px; word-break: break-all; font-size: 0.85em; color: #3b82f6; }}
        .explorer-link {{ display: inline-block; margin-top: 10px; color: #667eea; text-decoration: none; }}
        footer {{ text-align: center; padding: 30px 0; color: #666; border-top: 1px solid #333; margin-top: 30px; font-size: 0.85em; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🤖 Atlas</h1>
            <p>Self-Custodial Bounty Hunter</p>
            <span class="status-badge">● Operational</span>
        </header>
        
        <div class="grid">
            <div class="card">
                <h2>Net Profit</h2>
                <div class="value positive">${wallet_data['net_profit']:.2f}</div>
                <div class="sub-value">Lifetime earnings</div>
            </div>
            <div class="card">
                <h2>Total Income</h2>
                <div class="value">${wallet_data['total_income']:.2f}</div>
                <div class="sub-value">From bounties</div>
            </div>
            <div class="card">
                <h2>Total Expenses</h2>
                <div class="value negative">${wallet_data['total_expense']:.2f}</div>
                <div class="sub-value">Operational costs</div>
            </div>
            <div class="card">
                <h2>ROI</h2>
                <div class="value neutral">{wallet_data['roi']:.1f}x</div>
                <div class="sub-value">Return on investment</div>
            </div>
        </div>
        
        <div class="wallet-info">
            <h2>🔗 Agent Wallet (Sepolia Testnet)</h2>
            <div class="address">{wallet_data['address']}</div>
            <a href="https://sepolia.etherscan.io/address/{wallet_data['address']}" target="_blank" class="explorer-link">View on Etherscan →</a>
            <div style="margin-top: 15px;">
                <strong>Balances:</strong>
                <span style="margin-left: 10px;">ETH: {wallet_data['balances'].get('ETH', 0):.4f}</span>
                <span style="margin-left: 20px;">USDT: {wallet_data['balances'].get('USDT', 0):.2f}</span>
            </div>
        </div>
        
        <div class="transactions">
            <h2>📊 Recent Transactions</h2>
            {tx_html}
        </div>
        
        <footer>
            <p>Atlas - Autonomous Economic Agent for Tether Hackathon Galáctica 2026</p>
            <p style="margin-top: 10px;">
                <a href="https://github.com/Gitthack/atlas-wdk-hackathon" style="color: #667eea;">GitHub</a> • 
                Sepolia Testnet • WDK Compatible
            </p>
            <p style="margin-top: 10px; font-size: 0.8em;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
    </div>
</body>
</html>"""
    
    return html

if __name__ == '__main__':
    html = generate_static_html()
    output_path = 'dashboard_static.html'
    with open(output_path, 'w') as f:
        f.write(html)
    print(f"✅ Static dashboard exported to: {output_path}")
    print(f"📱 Open this file in your phone's browser to view the dashboard")
