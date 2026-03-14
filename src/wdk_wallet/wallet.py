#!/usr/bin/env python3
"""
WDK Wallet Interface for Atlas
Wallet Development Kit integration for self-custodial agent wallet
"""
import os
import json
import hashlib
from datetime import datetime
from typing import Optional, Dict, List

class AtlasWallet:
    """
    Self-custodial wallet for Atlas bounty hunter agent.
    
    This is a WDK-compatible interface. In production, it connects to
    Tether's WDK for real on-chain operations. For hackathon demo,
    it can operate on testnet.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.path.expanduser("~/.atlas/wallet.json")
        self.wallet_data = self._load_wallet()
        
    def _load_wallet(self) -> Dict:
        """Load wallet from storage or create new."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {
            "address": None,
            "network": "testnet",  # default to testnet
            "balances": {},
            "transactions": [],
            "created_at": datetime.now().isoformat(),
            "agent_id": "atlas_v1"
        }
    
    def _save_wallet(self):
        """Persist wallet to storage."""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.wallet_data, f, indent=2)
    
    def generate_wallet(self, network: str = "testnet") -> str:
        """
        Generate new self-custodial wallet.
        
        In production: Uses WDK key generation
        For demo: Generates deterministic mock address
        """
        # Mock address generation (replace with WDK in production)
        seed = f"atlas_{network}_{datetime.now().timestamp()}"
        address = "0x" + hashlib.sha256(seed.encode()).hexdigest()[:40]
        
        self.wallet_data["address"] = address
        self.wallet_data["network"] = network
        self.wallet_data["balances"] = {"USDT": 0.0, "ETH": 0.0}
        self._save_wallet()
        
        return address
    
    def get_address(self) -> Optional[str]:
        """Get wallet address."""
        return self.wallet_data.get("address")
    
    def get_balance(self, token: str = "USDT") -> float:
        """Get token balance."""
        return self.wallet_data.get("balances", {}).get(token, 0.0)
    
    def get_all_balances(self) -> Dict[str, float]:
        """Get all token balances."""
        return self.wallet_data.get("balances", {})
    
    def record_income(self, amount: float, token: str, source: str, 
                      tx_hash: Optional[str] = None) -> Dict:
        """
        Record bounty income.
        
        Args:
            amount: Income amount
            token: Token symbol (USDT, USDC, etc.)
            source: Source of income (e.g., "GitHub #1152")
            tx_hash: On-chain transaction hash
        """
        # Update balance
        current = self.wallet_data.get("balances", {}).get(token, 0.0)
        self.wallet_data["balances"][token] = current + amount
        
        # Record transaction
        tx = {
            "type": "income",
            "amount": amount,
            "token": token,
            "source": source,
            "tx_hash": tx_hash,
            "timestamp": datetime.now().isoformat()
        }
        self.wallet_data["transactions"].append(tx)
        self._save_wallet()
        
        return tx
    
    def record_expense(self, amount: float, token: str, category: str,
                       tx_hash: Optional[str] = None) -> Dict:
        """
        Record operational expense (API costs, etc.).
        
        Args:
            amount: Expense amount
            token: Token symbol
            category: Expense category ("api_cost", "infrastructure", etc.)
            tx_hash: On-chain transaction hash
        """
        # Check balance
        current = self.wallet_data.get("balances", {}).get(token, 0.0)
        if current < amount:
            raise ValueError(f"Insufficient balance: {current} < {amount}")
        
        # Update balance
        self.wallet_data["balances"][token] = current - amount
        
        # Record transaction
        tx = {
            "type": "expense",
            "amount": amount,
            "token": token,
            "category": category,
            "tx_hash": tx_hash,
            "timestamp": datetime.now().isoformat()
        }
        self.wallet_data["transactions"].append(tx)
        self._save_wallet()
        
        return tx
    
    def get_transaction_history(self, limit: int = 50) -> List[Dict]:
        """Get recent transactions."""
        txs = self.wallet_data.get("transactions", [])
        return sorted(txs, key=lambda x: x["timestamp"], reverse=True)[:limit]
    
    def get_economics_summary(self) -> Dict:
        """Get economic summary for dashboard."""
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
            "roi": (total_income - total_expense) / total_expense if total_expense > 0 else 0
        }
    
    def export_ledger(self) -> str:
        """Export ledger for on-chain verification."""
        ledger = {
            "agent": "atlas_v1",
            "address": self.wallet_data.get("address"),
            "exported_at": datetime.now().isoformat(),
            "transactions": self.wallet_data.get("transactions", [])
        }
        
        # Generate hash for integrity
        ledger_json = json.dumps(ledger, sort_keys=True)
        ledger_hash = hashlib.sha256(ledger_json.encode()).hexdigest()
        ledger["integrity_hash"] = ledger_hash
        
        return json.dumps(ledger, indent=2)


def main():
    """CLI demo"""
    print("=" * 60)
    print("Atlas WDK Wallet Interface Demo")
    print("=" * 60)
    
    # Create wallet
    wallet = AtlasWallet()
    
    if not wallet.get_address():
        print("\n[1] Generating new wallet...")
        address = wallet.generate_wallet("testnet")
        print(f"    Address: {address}")
    else:
        print(f"\n[1] Loaded existing wallet: {wallet.get_address()}")
    
    # Simulate operations
    print("\n[2] Simulating operations...")
    
    # Record income
    wallet.record_income(100.0, "USDT", "Bounty #1152 - MCP Server")
    wallet.record_income(50.0, "USDT", "Bounty #1153 - Bug Fix")
    
    # Record expenses
    wallet.record_expense(2.0, "USDT", "api_cost")
    wallet.record_expense(5.0, "USDT", "infrastructure")
    
    # Show summary
    print("\n[3] Economic Summary:")
    summary = wallet.get_economics_summary()
    print(f"    Address: {summary['address']}")
    print(f"    Balance: {summary['balances']} USDT")
    print(f"    Total Income: ${summary['total_income']}")
    print(f"    Total Expense: ${summary['total_expense']}")
    print(f"    Net Profit: ${summary['net_profit']}")
    print(f"    ROI: {summary['roi']:.2f}x")
    
    # Export ledger
    print("\n[4] Ledger Export (for on-chain verification):")
    ledger = wallet.export_ledger()
    print(f"    {ledger[:200]}...")
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
