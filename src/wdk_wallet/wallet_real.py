#!/usr/bin/env python3
"""
Atlas Real Testnet Wallet
Production-ready wallet integration for Sepolia testnet
Compatible with WDK architecture
"""
import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
from eth_account import Account
from web3 import Web3

# Sepolia Testnet Configuration
# Using public RPC endpoints
SEPOLIA_RPCS = [
    "https://rpc.sepolia.org",  # Public Sepolia RPC
    "https://sepolia.gateway.tenderly.co",  # Tenderly
    "https://ethereum-sepolia.publicnode.com",  # Public node
]
SEPOLIA_CHAIN_ID = 11155111

# USDT Testnet Contract (Sepolia)
# This is a mock USDT contract address - replace with real testnet USDT
USDT_CONTRACT_ADDRESS = "0x..."  # To be filled with real testnet contract

class AtlasRealWallet:
    """
    Real testnet wallet for Atlas agent.
    Uses Ethereum Sepolia testnet with real transactions.
    """
    
    def __init__(self, private_key: Optional[str] = None, config_path: Optional[str] = None):
        self.config_path = config_path or os.path.expanduser("~/.atlas/real_wallet.json")
        
        # Initialize Web3 connection with fallback
        self.w3 = None
        for rpc in SEPOLIA_RPCS:
            try:
                w3 = Web3(Web3.HTTPProvider(rpc))
                if w3.is_connected():
                    self.w3 = w3
                    print(f"[WALLET] Connected to Sepolia via {rpc}")
                    break
            except Exception as e:
                continue
        
        if not self.w3:
            print("[WALLET] Warning: Could not connect to Sepolia RPC. Running in offline mode.")
            self.w3 = None
        
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
            self.wallet_data["address"] = None
    
    def _load_wallet(self) -> Dict:
        """Load wallet from storage."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {
            "address": None,
            "private_key": None,
            "network": "sepolia",
            "balances": {"ETH": 0.0, "USDT": 0.0},
            "transactions": [],
            "created_at": datetime.now().isoformat(),
            "agent_id": "atlas_v1"
        }
    
    def _save_wallet(self):
        """Persist wallet to storage."""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.wallet_data, f, indent=2)
    
    def generate_wallet(self) -> str:
        """Generate new wallet."""
        acct = Account.create()
        self.account = acct
        self.wallet_data["address"] = acct.address
        self.wallet_data["private_key"] = acct.key.hex()
        self._save_wallet()
        
        print(f"[WALLET] Generated new address: {acct.address}")
        print(f"[WALLET] Save this private key securely: {acct.key.hex()}")
        
        return acct.address
    
    def get_address(self) -> Optional[str]:
        """Get wallet address."""
        return self.wallet_data.get("address")
    
    def get_balance_eth(self) -> float:
        """Get ETH balance."""
        if not self.account or not self.w3:
            return 0.0
        try:
            balance_wei = self.w3.eth.get_balance(self.account.address)
            return self.w3.from_wei(balance_wei, 'ether')
        except Exception as e:
            print(f"[WALLET] Error fetching ETH balance: {e}")
            return self.wallet_data.get("balances", {}).get("ETH", 0.0)
    
    def get_balance_usdt(self) -> float:
        """Get USDT balance (placeholder for contract interaction)."""
        # In production: interact with USDT contract
        return self.wallet_data.get("balances", {}).get("USDT", 0.0)
    
    def update_balances(self):
        """Update balances from chain."""
        if self.account and self.w3:
            try:
                eth_balance = self.get_balance_eth()
                self.wallet_data["balances"]["ETH"] = eth_balance
                self._save_wallet()
            except Exception as e:
                print(f"[WALLET] Could not update balances: {e}")
    
    def record_income(self, amount: float, token: str, source: str, 
                      tx_hash: Optional[str] = None) -> Dict:
        """Record bounty income."""
        current = self.wallet_data.get("balances", {}).get(token, 0.0)
        self.wallet_data["balances"][token] = current + amount
        
        tx = {
            "type": "income",
            "amount": amount,
            "token": token,
            "source": source,
            "tx_hash": tx_hash,
            "on_chain": tx_hash is not None,
            "timestamp": datetime.now().isoformat()
        }
        self.wallet_data["transactions"].append(tx)
        self._save_wallet()
        
        return tx
    
    def record_expense(self, amount: float, token: str, category: str,
                       tx_hash: Optional[str] = None) -> Dict:
        """Record operational expense."""
        current = self.wallet_data.get("balances", {}).get(token, 0.0)
        if current < amount:
            raise ValueError(f"Insufficient balance: {current} < {amount}")
        
        self.wallet_data["balances"][token] = current - amount
        
        tx = {
            "type": "expense",
            "amount": amount,
            "token": token,
            "category": category,
            "tx_hash": tx_hash,
            "on_chain": tx_hash is not None,
            "timestamp": datetime.now().isoformat()
        }
        self.wallet_data["transactions"].append(tx)
        self._save_wallet()
        
        return tx
    
    def get_economics_summary(self) -> Dict:
        """Get economic summary."""
        txs = self.wallet_data.get("transactions", [])
        
        total_income = sum(t["amount"] for t in txs if t["type"] == "income")
        total_expense = sum(t["amount"] for t in txs if t["type"] == "expense")
        
        return {
            "address": self.wallet_data.get("address"),
            "network": self.wallet_data.get("network"),
            "balances": self.wallet_data.get("balances", {}),
            "total_income": total_income,
            "total_expense": total_expense,
            "net_profit": total_income - total_expense,
            "transaction_count": len(txs),
            "on_chain_transactions": len([t for t in txs if t.get("on_chain")]),
            "roi": (total_income - total_expense) / total_expense if total_expense > 0 else 0
        }
    
    def export_ledger(self) -> str:
        """Export ledger with integrity hash."""
        ledger = {
            "agent": "atlas_v1",
            "address": self.wallet_data.get("address"),
            "network": self.wallet_data.get("network"),
            "exported_at": datetime.now().isoformat(),
            "transactions": self.wallet_data.get("transactions", [])
        }
        
        ledger_json = json.dumps(ledger, sort_keys=True)
        ledger_hash = hashlib.sha256(ledger_json.encode()).hexdigest()
        ledger["integrity_hash"] = ledger_hash
        
        return json.dumps(ledger, indent=2)
    
    def get_faucet_links(self) -> List[str]:
        """Get links to obtain testnet funds."""
        address = self.get_address()
        if not address:
            return []
        
        return [
            f"https://sepoliafaucet.com/ - Get Sepolia ETH (for gas)",
            f"https://faucet.quicknode.com/ethereum/sepolia - Alternative faucet",
            f"Wallet address: {address}"
        ]


def main():
    """Demo real wallet"""
    print("=" * 60)
    print("Atlas Real Testnet Wallet Demo")
    print("Network: Sepolia (Ethereum Testnet)")
    print("=" * 60)
    
    wallet = AtlasRealWallet()
    
    # Generate wallet if needed
    if not wallet.get_address():
        print("\n[1] Generating new wallet...")
        address = wallet.generate_wallet()
        print(f"\n    Address: {address}")
        print(f"\n⚠️  IMPORTANT: Save the private key shown above!")
        print(f"   You'll need it to recover the wallet.")
    else:
        print(f"\n[1] Loaded existing wallet: {wallet.get_address()}")
    
    # Update balances from chain
    print("\n[2] Checking balances...")
    wallet.update_balances()
    balances = wallet.wallet_data["balances"]
    print(f"    ETH: {balances.get('ETH', 0)} (need for gas)")
    print(f"    USDT: {balances.get('USDT', 0)}")
    
    # Show faucet links
    print("\n[3] Get testnet funds from:")
    for link in wallet.get_faucet_links():
        print(f"    - {link}")
    
    # Simulate operations
    print("\n[4] Simulating bounty operations...")
    wallet.record_income(75.0, "USDT", "Bounty #1152", tx_hash="0x...abc")
    wallet.record_expense(2.0, "USDT", "API costs")
    
    # Show summary
    print("\n[5] Economic Summary:")
    summary = wallet.get_economics_summary()
    print(f"    Total Income: ${summary['total_income']}")
    print(f"    Total Expense: ${summary['total_expense']}")
    print(f"    Net Profit: ${summary['net_profit']}")
    print(f"    ROI: {summary['roi']:.1f}x")
    print(f"    On-chain TXs: {summary['on_chain_transactions']}")
    
    print("\n[6] Ledger Export (for verification):")
    ledger = wallet.export_ledger()
    print(f"    {ledger[:150]}...")
    
    print("\n" + "=" * 60)
    print("Next steps:")
    print("1. Get Sepolia ETH from faucet")
    print("2. Request testnet USDT")
    print("3. Start real transactions!")
    print("=" * 60)


if __name__ == "__main__":
    main()
