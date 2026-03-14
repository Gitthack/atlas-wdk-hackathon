#!/usr/bin/env python3
"""
Atlas Wallet - Check Balance from Chain
Quick balance check with real-time update
"""
import os
import json
import sys

sys.path.insert(0, 'src/wdk_wallet')
from wallet_real import AtlasRealWallet

def main():
    print("=" * 60)
    print("Atlas Wallet - Live Balance Check")
    print("=" * 60)
    
    wallet = AtlasRealWallet()
    address = wallet.get_address()
    
    if not address:
        print("\n❌ No wallet found!")
        print("   Run: python3 src/wdk_wallet/wallet_real.py")
        return
    
    print(f"\n📍 Address: {address}")
    print(f"🔗 Explorer: https://sepolia.etherscan.io/address/{address}")
    
    print("\n⏳ Fetching live balance from Sepolia...")
    try:
        wallet.update_balances()
        eth_balance = wallet.get_balance_eth()
        print(f"\n✅ Balance Updated!")
        print(f"   ETH: {eth_balance} (for gas)")
        print(f"   USDT: {wallet.wallet_data.get('balances', {}).get('USDT', 0)}")
        
        if eth_balance > 0:
            print(f"\n🎉 You have testnet ETH! Ready for transactions.")
        else:
            print(f"\n⚠️  No ETH yet. Check explorer link above.")
            
    except Exception as e:
        print(f"\n⚠️  Could not fetch live balance: {e}")
        print(f"   Check manually: https://sepolia.etherscan.io/address/{address}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
