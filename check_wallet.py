#!/usr/bin/env python3
"""
Atlas Wallet Quick Check
Simple wallet status without network blocking
"""
import os
import json

WALLET_PATH = os.path.expanduser("~/.atlas/real_wallet.json")

def show_wallet():
    print("=" * 60)
    print("Atlas Testnet Wallet Status")
    print("=" * 60)
    
    if os.path.exists(WALLET_PATH):
        with open(WALLET_PATH, 'r') as f:
            wallet = json.load(f)
        
        print(f"\n✅ Wallet Found!")
        print(f"   Address: {wallet.get('address', 'N/A')}")
        print(f"   Network: {wallet.get('network', 'N/A')}")
        print(f"   Created: {wallet.get('created_at', 'N/A')}")
        print(f"\n   Balances:")
        for token, balance in wallet.get('balances', {}).items():
            print(f"     {token}: {balance}")
        
        print(f"\n   Transactions: {len(wallet.get('transactions', []))}")
        
        # Show faucet info
        address = wallet.get('address')
        if address:
            print(f"\n🔗 Get testnet funds:")
            print(f"   1. https://sepoliafaucet.com/")
            print(f"   2. Enter address: {address}")
            print(f"   3. Verify: https://sepolia.etherscan.io/address/{address}")
    else:
        print("\n❌ No wallet found.")
        print("   Run: python3 src/wdk_wallet/wallet_real.py")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    show_wallet()
