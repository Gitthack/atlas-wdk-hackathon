#!/usr/bin/env python3
"""
Atlas Autonomous Bounty Hunter - Full Integration
Connects scanner, validator, wallet, and dashboard
"""
import os
import sys
import json
import time
from datetime import datetime

# Add paths for imports
sys.path.insert(0, os.path.expanduser('~/.openclaw/workspace/scripts'))
sys.path.insert(0, 'src/wdk_wallet')
sys.path.insert(0, 'src/atlas_core')

from atlas_scanner import GitHubScanner
from atlas_task_validator import TaskValidator
from integration import AtlasWDKIntegration

WORKSPACE = os.path.expanduser('~/.openclaw/workspace')
STATE_DIR = os.path.join(WORKSPACE, 'atlas-hackathon', 'state')

class AutonomousAtlas:
    """
    Fully autonomous Atlas agent.
    
    Workflow:
    1. Scan for bounties
    2. Validate each task
    3. Check economic viability (ROI, budget)
    4. Execute if approved
    5. Record all economics
    """
    
    def __init__(self, github_token=None):
        self.scanner = GitHubScanner(token=github_token)
        self.validator = TaskValidator(github_token=github_token)
        self.economics = AtlasWDKIntegration()
        
        # Ensure state directory exists
        os.makedirs(STATE_DIR, exist_ok=True)
        
        # Load state
        self.state_file = os.path.join(STATE_DIR, 'atlas_autonomous_state.json')
        self.state = self._load_state()
    
    def _load_state(self) -> dict:
        """Load agent state."""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {
            "tasks_evaluated": [],
            "tasks_approved": [],
            "tasks_executed": [],
            "last_scan": None,
            "total_bounties_found": 0
        }
    
    def _save_state(self):
        """Save agent state."""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def scan_and_evaluate(self, max_tasks=5) -> list:
        """
        Scan for bounties and evaluate each one.
        
        Returns list of approved tasks ready for execution.
        """
        print("\n" + "=" * 60)
        print("🔍 Atlas Autonomous Scan")
        print("=" * 60)
        
        # Scan for tasks using the scanner module
        print("\n[1] Scanning GitHub for bounties...")
        
        # Import and run the scan function
        sys.path.insert(0, os.path.expanduser('~/.openclaw/workspace/scripts'))
        from atlas_scanner import scan_github, GITHUB_SEARCH_QUERIES
        
        # Manually scan using the scanner
        tasks = []
        for query in GITHUB_SEARCH_QUERIES[:2]:  # Limit to 2 queries for speed
            issues = self.scanner.search_issues(query, per_page=3)
            
            for issue in issues:
                title = issue.get("title", "")
                body = issue.get("body", "") or ""
                html_url = issue.get("html_url", "")
                
                # Extract bounty
                bounty = self.scanner.extract_bounty_amount(title, body)
                if not bounty or bounty < 50:
                    continue
                
                # Assess complexity
                complexity = self.scanner.assess_complexity(
                    title, body, issue.get("labels", [])
                )
                
                # Estimate cost based on complexity
                cost_map = {"low": 5, "medium": 15, "high": 50}
                estimated_cost = cost_map.get(complexity, 15)
                
                task = {
                    "id": issue.get("id"),
                    "title": title,
                    "url": html_url,
                    "bounty": bounty,
                    "complexity": complexity,
                    "estimated_cost": estimated_cost,
                    "platform": "github",
                    "found_at": datetime.now().isoformat(),
                    "status": "new"
                }
                tasks.append(task)
                
                if len(tasks) >= max_tasks:
                    break
            
            if len(tasks) >= max_tasks:
                break
        
        print(f"    Found {len(tasks)} potential tasks")
        
        approved_tasks = []
        
        for i, task in enumerate(tasks, 1):
            print(f"\n[2.{i}] Evaluating: {task['title'][:50]}...")
            
            # Skip if already evaluated
            task_id = f"{task['platform']}_{task['id']}"
            if task_id in self.state["tasks_evaluated"]:
                print(f"    ⚠️  Already evaluated, skipping")
                continue
            
            # Validate task
            validation = self._validate_task(task)
            self.state["tasks_evaluated"].append(task_id)
            
            if not validation["should_proceed"]:
                print(f"    ❌ Rejected: {validation['reason']}")
                continue
            
            # Check economic viability
            economic_decision = self.economics.autonomous_decision({
                "id": task['id'],
                "title": task['title'],
                "bounty": task.get('bounty', 0),
                "estimated_cost": task.get('estimated_cost', 10),
                "platform": task['platform']
            })
            
            if economic_decision["decision"] != "APPROVE":
                print(f"    ❌ Economic reject: {economic_decision['reason']}")
                continue
            
            # Task approved!
            print(f"    ✅ APPROVED!")
            print(f"       Expected profit: ${economic_decision['expected_profit']:.2f}")
            print(f"       ROI: {economic_decision['roi']:.1f}x")
            
            approved_tasks.append({
                **task,
                "validation": validation,
                "economic_decision": economic_decision
            })
            self.state["tasks_approved"].append(task_id)
        
        self.state["last_scan"] = datetime.now().isoformat()
        self.state["total_bounties_found"] += len(tasks)
        self._save_state()
        
        return approved_tasks
    
    def _validate_task(self, task: dict) -> dict:
        """Validate a single task."""
        if task["platform"] == "github":
            # Parse owner/repo from URL
            url_parts = task["url"].split("/")
            if len(url_parts) >= 7:
                owner = url_parts[-4]
                repo = url_parts[-3]
                issue_number = int(url_parts[-1])
                return self.validator.validate_github_issue(owner, repo, issue_number)
        
        # Default: medium risk, proceed with caution
        return {
            "should_proceed": True,
            "risk_level": "medium",
            "reason": "Manual validation required"
        }
    
    def simulate_execution(self, task: dict) -> dict:
        """
        Simulate task execution (for demo).
        
        In production, this would actually execute the task.
        """
        print(f"\n[3] Simulating execution: {task['title'][:40]}...")
        
        # Record estimated costs
        estimated_cost = task.get('estimated_cost', 10)
        
        try:
            # Record expense
            self.economics.record_task_cost(
                task_id=str(task['id']),
                cost=estimated_cost,
                description=f"API costs for {task['platform']} #{task['id']}"
            )
            print(f"    💸 Recorded expense: ${estimated_cost}")
            
            # Simulate completion and income
            bounty = task.get('bounty', 0)
            if bounty > 0:
                self.economics.record_bounty_income(
                    bounty_id=str(task['id']),
                    amount=bounty,
                    platform=task['platform']
                )
                print(f"    💰 Recorded income: ${bounty}")
            
            task_id = f"{task['platform']}_{task['id']}"
            self.state["tasks_executed"].append(task_id)
            self._save_state()
            
            return {
                "success": True,
                "cost": estimated_cost,
                "income": bounty,
                "profit": bounty - estimated_cost
            }
            
        except Exception as e:
            print(f"    ❌ Execution failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_dashboard_data(self) -> dict:
        """Get data for dashboard display."""
        economic_status = self.economics.get_economic_status()
        
        return {
            "agent_status": "operational",
            "economics": economic_status,
            "statistics": {
                "tasks_evaluated": len(self.state["tasks_evaluated"]),
                "tasks_approved": len(self.state["tasks_approved"]),
                "tasks_executed": len(self.state["tasks_executed"]),
                "total_bounties_found": self.state["total_bounties_found"],
                "last_scan": self.state["last_scan"]
            },
            "wallet_address": self.economics.wallet.get_address()
        }
    
    def run_cycle(self):
        """Run one complete autonomous cycle."""
        print("\n🤖 Atlas Autonomous Agent - Starting Cycle")
        print("=" * 60)
        
        # Step 1: Scan and evaluate
        approved = self.scan_and_evaluate(max_tasks=3)
        
        if not approved:
            print("\n📭 No viable tasks found this cycle")
            return
        
        print(f"\n🎯 Found {len(approved)} approved tasks")
        
        # Step 2: Execute (simulate for now)
        for task in approved:
            result = self.simulate_execution(task)
            if result["success"]:
                print(f"    ✅ Profit: ${result['profit']:.2f}")
        
        # Step 3: Show summary
        print("\n" + "=" * 60)
        print("📊 Cycle Complete")
        print("=" * 60)
        
        summary = self.get_dashboard_data()
        econ = summary["economics"]["wallet"]
        print(f"\n💰 Total Income: ${econ['total_income']:.2f}")
        print(f"💸 Total Expenses: ${econ['total_expense']:.2f}")
        print(f"📈 Net Profit: ${econ['net_profit']:.2f}")
        print(f"🎯 ROI: {econ['roi']:.1f}x")
        print(f"\n📋 Statistics:")
        print(f"   Tasks Evaluated: {summary['statistics']['tasks_evaluated']}")
        print(f"   Tasks Approved: {summary['statistics']['tasks_approved']}")
        print(f"   Tasks Executed: {summary['statistics']['tasks_executed']}")
        print(f"\n🔗 Wallet: {summary['wallet_address']}")


def main():
    """Run autonomous Atlas."""
    print("=" * 60)
    print("🤖 Atlas - Autonomous Bounty Hunter")
    print("Fully Integrated System")
    print("=" * 60)
    
    # Initialize
    github_token = os.getenv("GITHUB_TOKEN")
    atlas = AutonomousAtlas(github_token=github_token)
    
    # Run one cycle
    atlas.run_cycle()
    
    print("\n" + "=" * 60)
    print("✅ Autonomous cycle complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
