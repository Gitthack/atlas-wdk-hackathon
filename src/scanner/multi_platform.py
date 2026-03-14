#!/usr/bin/env python3
"""
Multi-Platform Bounty Scanner
Extends Atlas to scan multiple bounty platforms
"""
import os
import sys
import json
import re
import requests
from datetime import datetime
from typing import List, Dict, Optional

sys.path.insert(0, os.path.expanduser('~/.openclaw/workspace/scripts'))

class MultiPlatformScanner:
    """Scan multiple platforms for bounties."""
    
    def __init__(self, github_token=None):
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.headers = {}
        if self.github_token:
            self.headers["Authorization"] = f"token {self.github_token}"
        self.headers["Accept"] = "application/vnd.github.v3+json"
    
    def scan_all_platforms(self) -> List[Dict]:
        """Scan all supported platforms."""
        all_tasks = []
        
        print("\n🔍 Scanning all platforms...")
        
        # Platform 1: GitHub
        print("  [1/3] GitHub...")
        github_tasks = self.scan_github()
        all_tasks.extend(github_tasks)
        print(f"        Found {len(github_tasks)} tasks")
        
        # Platform 2: Gitcoin (via API or scraping)
        print("  [2/3] Gitcoin...")
        gitcoin_tasks = self.scan_gitcoin()
        all_tasks.extend(gitcoin_tasks)
        print(f"        Found {len(gitcoin_tasks)} tasks")
        
        # Platform 3: IssueHunt
        print("  [3/3] IssueHunt...")
        issuehunt_tasks = self.scan_issuehunt()
        all_tasks.extend(issuehunt_tasks)
        print(f"        Found {len(issuehunt_tasks)} tasks")
        
        print(f"\n📊 Total: {len(all_tasks)} tasks from {len(set(t['platform'] for t in all_tasks))} platforms")
        return all_tasks
    
    def scan_github(self) -> List[Dict]:
        """Scan GitHub for bounties."""
        queries = [
            'label:"help wanted" label:bounty language:python',
            'label:"good first issue" label:bounty language:rust',
            'label:bug-bounty is:open',
            'bounty reward is:issue is:open',
        ]
        
        tasks = []
        for query in queries[:2]:  # Limit for speed
            try:
                url = "https://api.github.com/search/issues"
                params = {
                    "q": query,
                    "sort": "updated",
                    "order": "desc",
                    "per_page": 5
                }
                
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
                response.raise_for_status()
                issues = response.json().get("items", [])
                
                for issue in issues:
                    task = self._parse_github_issue(issue)
                    if task:
                        tasks.append(task)
                        
            except Exception as e:
                print(f"        GitHub API error: {e}")
                continue
        
        return tasks
    
    def _parse_github_issue(self, issue: Dict) -> Optional[Dict]:
        """Parse GitHub issue into task format."""
        title = issue.get("title", "")
        body = issue.get("body", "") or ""
        
        # Extract bounty amount
        bounty = self._extract_bounty(title + " " + body)
        if not bounty or bounty < 50:
            return None
        
        # Assess complexity
        complexity = self._assess_complexity(title, body, issue.get("labels", []))
        cost_map = {"low": 5, "medium": 15, "high": 50}
        
        return {
            "id": str(issue.get("id")),
            "title": title[:100],
            "url": issue.get("html_url"),
            "bounty": bounty,
            "complexity": complexity,
            "estimated_cost": cost_map.get(complexity, 15),
            "platform": "github",
            "created_at": issue.get("created_at"),
            "found_at": datetime.now().isoformat()
        }
    
    def scan_gitcoin(self) -> List[Dict]:
        """Scan Gitcoin for bounties."""
        # Gitcoin API endpoint (simplified for demo)
        # In production, use their GraphQL API
        tasks = []
        
        # Simulated Gitcoin data for demo
        # In real implementation, call Gitcoin API
        demo_tasks = [
            {
                "id": "gitcoin_001",
                "title": "Smart Contract Audit - DeFi Protocol",
                "url": "https://gitcoin.co/issue/example",
                "bounty": 5000,
                "complexity": "high",
                "platform": "gitcoin",
                "created_at": datetime.now().isoformat(),
                "found_at": datetime.now().isoformat()
            },
            {
                "id": "gitcoin_002", 
                "title": "Frontend Bug Fix - Web3 Dashboard",
                "url": "https://gitcoin.co/issue/example2",
                "bounty": 300,
                "complexity": "low",
                "platform": "gitcoin",
                "created_at": datetime.now().isoformat(),
                "found_at": datetime.now().isoformat()
            }
        ]
        
        # Add cost estimates
        cost_map = {"low": 5, "medium": 15, "high": 50}
        for task in demo_tasks:
            task["estimated_cost"] = cost_map.get(task["complexity"], 15)
        
        return demo_tasks
    
    def scan_issuehunt(self) -> List[Dict]:
        """Scan IssueHunt for bounties."""
        # IssueHunt API or scraping
        # Simplified for demo
        tasks = []
        
        demo_tasks = [
            {
                "id": "ih_001",
                "title": "TypeScript Type Definition Fix",
                "url": "https://issuehunt.io/r/example",
                "bounty": 150,
                "complexity": "low",
                "platform": "issuehunt",
                "created_at": datetime.now().isoformat(),
                "found_at": datetime.now().isoformat()
            }
        ]
        
        cost_map = {"low": 5, "medium": 15, "high": 50}
        for task in demo_tasks:
            task["estimated_cost"] = cost_map.get(task["complexity"], 15)
        
        return tasks
    
    def _extract_bounty(self, text: str) -> Optional[float]:
        """Extract bounty amount from text."""
        patterns = [
            r'\$([\d,]+(?:\.\d{2})?)',
            r'bounty[:\s]+\$?([\d,]+)',
            r'reward[:\s]+\$?([\d,]+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                amounts = []
                for m in matches:
                    try:
                        amounts.append(float(m.replace(",", "")))
                    except ValueError:
                        continue
                return max(amounts) if amounts else None
        
        return None
    
    def _assess_complexity(self, title: str, body: str, labels: List) -> str:
        """Assess task complexity."""
        text = f"{title} {body}".lower()
        label_names = [l.get("name", "").lower() for l in labels]
        
        high_keywords = ["refactor", "architecture", "performance", "security", "audit", "smart contract"]
        low_keywords = ["typo", "documentation", "readme", "fix link", "good first issue"]
        medium_keywords = ["feature", "implement", "add support", "integration"]
        
        if any(k in text for k in high_keywords) or "hard" in label_names:
            return "high"
        elif any(k in text for k in low_keywords) or "easy" in label_names:
            return "low"
        elif any(k in text for k in medium_keywords):
            return "medium"
        
        return "medium"


def main():
    """Test multi-platform scanner."""
    print("=" * 60)
    print("Multi-Platform Bounty Scanner")
    print("=" * 60)
    
    scanner = MultiPlatformScanner()
    tasks = scanner.scan_all_platforms()
    
    print("\n" + "=" * 60)
    print(f"Found {len(tasks)} total bounties")
    print("=" * 60)
    
    for task in tasks[:5]:
        print(f"\n💰 ${task['bounty']} | {task['platform']} | {task['complexity']}")
        print(f"   {task['title'][:60]}...")
        print(f"   {task['url']}")


if __name__ == "__main__":
    main()
