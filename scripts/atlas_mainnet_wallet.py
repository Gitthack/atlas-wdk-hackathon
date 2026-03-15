#!/usr/bin/env python3
"""
Atlas Mainnet Integration
Real USDT/USDC interactions on Ethereum mainnet
"""
import os
import sys
import json
from datetime import datetime
from typing import Dict, Optional
from decimal import Decimal

try:
    from web3 import Web3
    from eth_account import Account
    WEB3_AVAILABLE = True
except ImportError:
    WEB3_AVAILABLE = False
    print("⚠️  Run: pip install web3 eth-account")

# USDT Contract on Ethereum Mainnet
USDT_CONTRACT = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
USDT_ABI = '''[
    {"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},
    {"constant":false,"inputs":[{"name":"_upgradedAddress","type":"address"}],"name":"deprecate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},
    {"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},
    {"constant":true,"inputs":[],"name":"deprecated","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},
    {"constant":false,"inputs":[{"name":"_evilUser","type":"address"}],"name":"addBlackList","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},
    {"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},
    {"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},
    {"constant":true,"inputs":[],"name":"upgradedAddress","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},
    {"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balances","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},
    {"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},
    {"constant":true,"inputs":[],"name":"maximumFee","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},
    {"constant":true,"inputs":[],"name":"_totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},
    {"constant":false,"inputs":[],"name":"unpause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},
    {"constant":true,"inputs":[{"name":"_maker","type":"address"}],"name":"getBlackListStatus","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},
    {"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowed","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},
    {"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},
    {"constant":true,"inputs":[{"name":"who","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},
    {"constant":true,"inputs":[],"name":"getOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},
    {"constant":false,"inputs":[],"name":"pause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},
    {"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},
    {"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},
    {"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},
    {"constant":false,"inputs":[{"name":"newBasisPoints","type":"uint256"}],"name":"setParams","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},
    {"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"issue","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},
    {"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"redeem","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},
    {"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},
    {"constant":true,"inputs":[],"name":"basisPointsRate","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},
    {"constant":true,"inputs":[{"name":"","type":"address"}],"name":"isBlackListed","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},
    {"constant":false,"inputs":[{"name":"_clearedUser","type":"address"}],"name":"removeBlackList","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},
    {"constant":true,"inputs":[],"name":"MAX_UINT","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},
    {"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},
    {"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_subtractedValue","type":"uint256"}],"name":"decreaseApproval","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},
    {"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},
    {"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_addedValue","type":"uint256"}],"name":"increaseApproval","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},
    {"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},
    {"constant":true,"inputs":[],"name":"getOwner","outputs":[{"name":"owner","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},
    {"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},
    {"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"},
    {"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},
    {"anonymous":false,"inputs":[{"indexed":false,"name":"newAddress","type":"address"}],"name":"Deprecate","type":"event"},
    {"anonymous":false,"inputs":[{"indexed":false,"name":"feeBasisPoints","type":"uint256"},{"indexed":false,"name":"maxFee","type":"uint256"}],"name":"Params","type":"event"},
    {"anonymous":false,"inputs":[{"indexed":false,"name":"_blackListedUser","type":"address"},{"indexed":false,"name":"_balance","type":"uint256"}],"name":"DestroyedBlackFunds","type":"event"},
    {"anonymous":false,"inputs":[{"indexed":false,"name":"_user","type":"address"}],"name":"AddedBlackList","type":"event"},
    {"anonymous":false,"inputs":[{"indexed":false,"name":"_user","type":"address"}],"name":"RemovedBlackList","type":"event"},
    {"anonymous":false,"inputs":[{"indexed":true,"name":"previousOwner","type":"address"},{"indexed":true,"name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},
    {"anonymous":false,"inputs":[],"name":"Pause","type":"event"},
    {"anonymous":false,"inputs":[],"name":"Unpause","type":"event"}
]'''

# Mainnet RPC endpoints (fallback list)
MAINNET_RPCS = [
    "https://eth.llamarpc.com",
    "https://rpc.ankr.com/eth",
    "https://ethereum.publicnode.com",
]

class AtlasMainnetWallet:
    """
    Real Ethereum mainnet wallet with USDT support.
    WARNING: This uses real funds!
    """
    
    def __init__(self, private_key: Optional[str] = None):
        self.config_path = os.path.expanduser("~/.atlas/mainnet_wallet.json")
        
        # Initialize Web3
        self.w3 = None
        for rpc in MAINNET_RPCS:
            try:
                self.w3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={'timeout': 5}))
                if self.w3.is_connected():
                    print(f"[MAINNET] Connected via {rpc}")
                    break
            except:
                continue
        
        if not self.w3:
            print("[MAINNET] ⚠️  Could not connect to mainnet")
        
        # Load or create wallet
        self.wallet_data = self._load_wallet()
        
        if private_key:
            self.account = Account.from_key(private_key)
            self.wallet_data["address"] = self.account.address
            self.wallet_data["private_key"] = private_key
            self._save_wallet()
        elif self.wallet_data.get("private_key"):
            self.account = Account.from_key(self.wallet_data["private_key"])
        else:
            self.account = None
            print("[MAINNET] ⚠️  No wallet configured. Use generate_wallet() or import_private_key()")
        
        # USDT Contract
        if self.w3:
            self.usdt = self.w3.eth.contract(
                address=Web3.to_checksum_address(USDT_CONTRACT),
                abi=json.loads(USDT_ABI)
            )
    
    def _load_wallet(self) -> Dict:
        if os.path.exists(self.config_path):
            with open(self.config_path) as f:
                return json.load(f)
        return {
            "address": None,
            "private_key": None,
            "network": "mainnet",
            "balances": {"ETH": 0.0, "USDT": 0.0},
            "transactions": [],
            "created_at": datetime.now().isoformat(),
            "warning_acknowledged": False
        }
    
    def _save_wallet(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.wallet_data, f, indent=2)
    
    def acknowledge_warning(self):
        """User must acknowledge real funds warning"""
        print("=" * 70)
        print("⚠️  ⚠️  ⚠️  WARNING: REAL FUNDS ⚠️  ⚠️  ⚠️")
        print("=" * 70)
        print("This wallet interacts with ETHEREUM MAINNET.")
        print("All transactions use REAL ETH and REAL USDT.")
        print("Gas fees are paid in REAL ETH.")
        print("")
        print("Make sure you understand:")
        print("1. Transactions are irreversible")
        print("2. Gas fees can be high ($10-100+)")
        print("3. Private key security is critical")
        print("")
        
        confirm = input("Type 'I UNDERSTAND' to proceed: ")
        if confirm == "I UNDERSTAND":
            self.wallet_data["warning_acknowledged"] = True
            self._save_wallet()
            return True
        return False
    
    def get_address(self) -> Optional[str]:
        return self.wallet_data.get("address")
    
    def get_balance_eth(self) -> float:
        """Get ETH balance"""
        if not self.account or not self.w3:
            return 0.0
        try:
            balance_wei = self.w3.eth.get_balance(self.account.address)
            return float(self.w3.from_wei(balance_wei, 'ether'))
        except Exception as e:
            print(f"[ERROR] Could not fetch ETH balance: {e}")
            return self.wallet_data.get("balances", {}).get("ETH", 0.0)
    
    def get_balance_usdt(self) -> float:
        """Get USDT balance"""
        if not self.account or not self.w3 or not self.usdt:
            return self.wallet_data.get("balances", {}).get("USDT", 0.0)
        try:
            balance = self.usdt.functions.balanceOf(self.account.address).call()
            # USDT has 6 decimals
            return balance / 1e6
        except Exception as e:
            print(f"[ERROR] Could not fetch USDT balance: {e}")
            return self.wallet_data.get("balances", {}).get("USDT", 0.0)
    
    def record_income(self, amount: float, source: str, tx_hash: Optional[str] = None):
        """Record bounty income"""
        self.wallet_data["balances"]["USDT"] = self.get_balance_usdt()
        
        tx = {
            "type": "income",
            "amount": amount,
            "token": "USDT",
            "source": source,
            "tx_hash": tx_hash,
            "on_chain": tx_hash is not None,
            "timestamp": datetime.now().isoformat()
        }
        self.wallet_data["transactions"].append(tx)
        self._save_wallet()
        print(f"[INCOME] +${amount} USDT from {source}")
    
    def record_expense(self, amount: float, category: str, tx_hash: Optional[str] = None):
        """Record operational expense"""
        self.wallet_data["balances"]["USDT"] = self.get_balance_usdt()
        
        tx = {
            "type": "expense",
            "amount": amount,
            "token": "USDT",
            "category": category,
            "tx_hash": tx_hash,
            "on_chain": tx_hash is not None,
            "timestamp": datetime.now().isoformat()
        }
        self.wallet_data["transactions"].append(tx)
        self._save_wallet()
        print(f"[EXPENSE] -${amount} USDT for {category}")
    
    def demo(self):
        """Demo mainnet wallet (read-only)"""
        print("=" * 70)
        print("💎 ATLAS MAINNET WALLET (READ-ONLY DEMO)")
        print("=" * 70)
        print(f"\nWallet Address: {self.get_address() or 'Not configured'}")
        print(f"Network: Ethereum Mainnet")
        print(f"USDT Contract: {USDT_CONTRACT}")
        
        if self.w3 and self.get_address():
            print("\n📊 Balances:")
            eth_bal = self.get_balance_eth()
            usdt_bal = self.get_balance_usdt()
            print(f"   ETH: {eth_bal:.6f}")
            print(f"   USDT: {usdt_bal:.2f}")
            
            if eth_bal > 0 or usdt_bal > 0:
                print("\n✅ Wallet has real funds!")
            else:
                print("\nℹ️  Wallet is empty (or could not fetch balances)")
        
        print("\n⚠️  To enable transactions:")
        print("   1. Set GITHUB_TOKEN for GitHub integration")
        print("   2. Import wallet with real ETH/USDT")
        print("   3. Run acknowledge_warning()")
        print("   4. Use send_usdt() for payments")

def main():
    """Main entry"""
    wallet = AtlasMainnetWallet()
    wallet.demo()

if __name__ == "__main__":
    main()
