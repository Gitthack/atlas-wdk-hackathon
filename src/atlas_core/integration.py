#!/usr/bin/env python3
"""
Atlas Core Integration
Connects existing Atlas bounty hunter with WDK wallet
"""
import os
import sys
import yaml
from datetime import datetime
from typing import Dict, List, Optional

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'wdk_wallet'))

from wallet_real import AtlasRealWallet as AtlasWallet

WORKSPACE = "/root/.openclaw/workspace"
ATLAS_CORE = os.path.join(WORKSPACE, "scripts")

class AtlasWDKIntegration:
    """
    Bridge between Atlas bounty hunter and WDK wallet.
    
    This is the core integration that makes Atlas economically autonomous.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), '..', '..', 'config', 'wdk_config.yaml'
        )
        self.config = self._load_config()
        self.wallet = AtlasWallet()
        
        # Ensure wallet exists
        if not self.wallet.get_address():
            print("[INIT] Generating new agent wallet...")
            address = self.wallet.generate_wallet(self.config.get('network', 'testnet'))
            print(f"[INIT] Wallet created: {address}")
    
    def _load_config(self) -> Dict:
        """Load WDK configuration."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def check_budget(self, estimated_cost: float) -> Dict:
        """
        Check if task is within budget constraints.
        
        Returns:
            {
                "approved": bool,
                "reason": str,
                "current_balance": float,
                "daily_budget": float,
                "remaining_budget": float
            }
        """
        balance = self.wallet.get_balance("USDT")
        daily_budget = self.config.get('economics', {}).get('daily_budget_usd', 50)
        
        # Check hard stop loss
        economics = self.wallet.get_economics_summary()
        if economics.get('net_profit', 0) < self.config.get('economics', {}).get('stop_loss_threshold', -20):
            return {
                "approved": False,
                "reason": "STOP_LOSS_TRIGGERED",
                "current_balance": balance,
                "daily_budget": daily_budget,
                "remaining_budget": 0
            }
        
        # Check if sufficient balance
        if balance < estimated_cost:
            return {
                "approved": False,
                "reason": "INSUFFICIENT_BALANCE",
                "current_balance": balance,
                "daily_budget": daily_budget,
                "remaining_budget": 0
            }
        
        return {
            "approved": True,
            "reason": "BUDGET_OK",
            "current_balance": balance,
            "daily_budget": daily_budget,
            "remaining_budget": balance - estimated_cost
        }
    
    def record_task_cost(self, task_id: str, cost: float, description: str) -> Dict:
        """Record operational cost for a task."""
        try:
            tx = self.wallet.record_expense(
                amount=cost,
                token="USDT",
                category=f"task_{task_id}",
                tx_hash=None  # Will be populated when on-chain
            )
            return {
                "success": True,
                "transaction": tx,
                "new_balance": self.wallet.get_balance("USDT")
            }
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def record_bounty_income(self, bounty_id: str, amount: float, platform: str) -> Dict:
        """Record bounty income."""
        tx = self.wallet.record_income(
            amount=amount,
            token="USDT",
            source=f"{platform} #{bounty_id}",
            tx_hash=None
        )
        return {
            "success": True,
            "transaction": tx,
            "new_balance": self.wallet.get_balance("USDT")
        }
    
    def get_economic_status(self) -> Dict:
        """Get complete economic status for dashboard."""
        wallet_summary = self.wallet.get_economics_summary()
        budget_check = self.check_budget(0)
        
        return {
            "wallet": wallet_summary,
            "budget": budget_check,
            "config": {
                "network": self.config.get('network'),
                "daily_budget": self.config.get('economics', {}).get('daily_budget_usd'),
                "stop_loss": self.config.get('economics', {}).get('stop_loss_threshold')
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def export_on_chain_proof(self) -> str:
        """Export ledger for on-chain verification."""
        return self.wallet.export_ledger()
    
    def autonomous_decision(self, task: Dict) -> Dict:
        """
        Make autonomous decision whether to take a task.
        
        This is the core autonomy function - Atlas decides for itself.
        """
        bounty = task.get('bounty', 0)
        estimated_cost = task.get('estimated_cost', 0)
        
        # Check budget
        budget = self.check_budget(estimated_cost)
        if not budget["approved"]:
            return {
                "decision": "REJECT",
                "reason": budget["reason"],
                "task": task
            }
        
        # Check ROI
        roi = (bounty - estimated_cost) / estimated_cost if estimated_cost > 0 else 0
        min_roi = 3.0  # Minimum 3x ROI
        
        if roi < min_roi:
            return {
                "decision": "REJECT",
                "reason": f"ROI_TOO_LOW ({roi:.1f}x < {min_roi}x)",
                "task": task
            }
        
        return {
            "decision": "APPROVE",
            "reason": "ECONOMICALLY_VIABLE",
            "expected_profit": bounty - estimated_cost,
            "roi": roi,
            "task": task
        }


def demo_integration():
    """Demonstrate Atlas-WDK integration."""
    print("=" * 60)
    print("Atlas + WDK Integration Demo")
    print("=" * 60)
    
    # Initialize integration
    atlas = AtlasWDKIntegration()
    
    print("\n[1] Wallet Status:")
    status = atlas.get_economic_status()
    print(f"    Address: {status['wallet']['address']}")
    print(f"    Balance: {status['wallet']['balances']} USDT")
    print(f"    Net Profit: ${status['wallet']['net_profit']}")
    
    print("\n[2] Simulating Bounty Task Decision:")
    task = {
        "id": "1152",
        "title": "RustChain MCP Server",
        "bounty": 75.0,
        "estimated_cost": 2.0,
        "platform": "GitHub"
    }
    
    decision = atlas.autonomous_decision(task)
    print(f"    Decision: {decision['decision']}")
    print(f"    Reason: {decision['reason']}")
    if decision['decision'] == 'APPROVE':
        print(f"    Expected Profit: ${decision['expected_profit']}")
        print(f"    ROI: {decision['roi']:.1f}x")
    
    print("\n[3] Recording Task Execution:")
    # Simulate completing the task
    cost_result = atlas.record_task_cost("1152", 2.0, "API costs for MCP development")
    print(f"    Cost recorded: ${2.0} USDT")
    
    income_result = atlas.record_bounty_income("1152", 75.0, "GitHub")
    print(f"    Income recorded: ${75.0} USDT")
    
    print("\n[4] Updated Economic Status:")
    final_status = atlas.get_economic_status()
    print(f"    New Balance: {final_status['wallet']['balances']} USDT")
    print(f"    Total Profit: ${final_status['wallet']['net_profit']}")
    
    print("\n[5] On-Chain Proof Export:")
    proof = atlas.export_on_chain_proof()
    print(f"    Proof hash: {proof[:100]}...")
    
    print("\n" + "=" * 60)
    print("Demo complete! Atlas is now economically autonomous.")
    print("=" * 60)


if __name__ == "__main__":
    demo_integration()
