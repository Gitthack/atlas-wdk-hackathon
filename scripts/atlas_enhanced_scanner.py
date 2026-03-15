#!/usr/bin/env python3
"""
Atlas Enhanced Scanner
Multi-platform bounty hunter with AI execution capabilities
"""
import os
import sys
import json
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

@dataclass
class BountyTask:
    id: str
    title: str
    platform: str
    bounty_amount: float
    currency: str
    url: str
    difficulty: str
    tags: List[str]
    deadline: Optional[datetime]
    description: str = ""
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'platform': self.platform,
            'bounty_amount': self.bounty_amount,
            'currency': self.currency,
            'url': self.url,
            'difficulty': self.difficulty,
            'tags': self.tags,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'description': self.description
        }

class Code4renaScanner:
    """Scanner for Code4rena audit contests"""
    
    CONTESTS_URL = "https://code4rena.com/contests"
    
    async def scan(self) -> List[BountyTask]:
        """Scan active Code4rena contests"""
        tasks = []
        
        # Note: Code4rena doesn't have a public API
        # This is a template for web scraping or API integration
        # In production, use their GraphQL endpoint or RSS feed
        
        # Active contests (manually updated for demo)
        active_contests = [
            {
                'name': 'Chainlink Rewards',
                'prize_pool': 200000,
                'currency': 'USDC',
                'end_date': '2025-07-16',
                'difficulty': 'high',
                'tags': ['solidity', 'defi', 'rewards']
            },
            {
                'name': 'Hyperlane Interoperability',
                'prize_pool': 150000,
                'currency': 'USDC',
                'end_date': '2025-06-30',
                'difficulty': 'high',
                'tags': ['solidity', 'cross-chain', 'bridge']
            }
        ]
        
        for contest in active_contests:
            tasks.append(BountyTask(
                id=f"c4_{contest['name'].lower().replace(' ', '_')}",
                title=f"Audit: {contest['name']}",
                platform='code4rena',
                bounty_amount=contest['prize_pool'],
                currency=contest['currency'],
                url=f"https://code4rena.com/contests/{contest['name'].lower().replace(' ', '-')}",
                difficulty=contest['difficulty'],
                tags=contest['tags'],
                deadline=datetime.fromisoformat(contest['end_date'])
            ))
        
        return tasks

class ImmunefiScanner:
    """Scanner for Immunefi bug bounties"""
    
    API_URL = "https://immunefi.com/bugs/"
    
    async def scan(self) -> List[BountyTask]:
        """Scan active Immunefi bounties"""
        tasks = []
        
        # High-value targets from Immunefi (demo data)
        bounties = [
            {
                'project': 'Aave',
                'max_bounty': 1000000,
                'currency': 'USD',
                'category': 'lending',
                'blockchain': 'ethereum'
            },
            {
                'project': 'Uniswap',
                'max_bounty': 2000000,
                'currency': 'USD',
                'category': 'dex',
                'blockchain': 'ethereum'
            },
            {
                'project': 'LayerZero',
                'max_bounty': 1500000,
                'currency': 'USD',
                'category': 'bridge',
                'blockchain': 'multi-chain'
            }
        ]
        
        for bounty in bounties:
            tasks.append(BountyTask(
                id=f"immunefi_{bounty['project'].lower()}",
                title=f"Bug Bounty: {bounty['project']}",
                platform='immunefi',
                bounty_amount=bounty['max_bounty'],
                currency=bounty['currency'],
                url=f"https://immunefi.com/bug-bounty/{bounty['project'].lower()}",
                difficulty='critical',
                tags=[bounty['category'], bounty['blockchain'], 'security'],
                deadline=None
            ))
        
        return tasks

class EnhancedAtlasScanner:
    """Enhanced multi-platform scanner"""
    
    def __init__(self):
        self.scanners = {
            'code4rena': Code4renaScanner(),
            'immunefi': ImmunefiScanner(),
            # Add more scanners here
        }
        self.results_file = os.path.expanduser('~/.atlas/enhanced_scan_results.json')
        
    async def scan_all(self) -> Dict[str, List[BountyTask]]:
        """Scan all platforms concurrently"""
        results = {}
        
        print("🔍 Enhanced Atlas Scan Starting...")
        print("=" * 70)
        
        for name, scanner in self.scanners.items():
            try:
                print(f"\n[{name.upper()}] Scanning...")
                tasks = await scanner.scan()
                results[name] = tasks
                print(f"  ✓ Found {len(tasks)} high-value opportunities")
                
                # Show top bounties
                for task in tasks[:3]:
                    print(f"    💰 ${task.bounty_amount:,.0f} | {task.difficulty} | {task.title[:50]}...")
                    
            except Exception as e:
                print(f"  ✗ Error scanning {name}: {e}")
                results[name] = []
        
        # Save results
        self._save_results(results)
        
        # Summary
        total = sum(len(tasks) for tasks in results.values())
        total_value = sum(
            task.bounty_amount for tasks in results.values() for task in tasks
        )
        
        print("\n" + "=" * 70)
        print(f"📊 SCAN COMPLETE")
        print(f"   Total Opportunities: {total}")
        print(f"   Total Prize Pool: ${total_value:,.0f}")
        print(f"   Platforms: {len(self.scanners)}")
        print("=" * 70)
        
        return results
    
    def _save_results(self, results: Dict[str, List[BountyTask]]):
        """Save scan results to file"""
        os.makedirs(os.path.dirname(self.results_file), exist_ok=True)
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'platforms': {
                name: [task.to_dict() for task in tasks]
                for name, tasks in results.items()
            }
        }
        
        with open(self.results_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n💾 Results saved to: {self.results_file}")

async def main():
    scanner = EnhancedAtlasScanner()
    await scanner.scan_all()

if __name__ == "__main__":
    asyncio.run(main())
