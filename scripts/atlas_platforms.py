#!/usr/bin/env python3
"""
Atlas Platform Integrations
Code4rena, Immunefi, and more
"""
import os
import sys
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class AuditSubmission:
    platform: str
    contest_id: str
    title: str
    findings: List[Dict]
    severity: str  # critical, high, medium, low
    reward_estimate: float
    submitted_at: str
    status: str  # submitted, judged, rewarded

class Code4renaIntegration:
    """
    Code4rena audit contest integration.
    Findings submission and tracking.
    """
    
    PLATFORM = "code4rena"
    
    def __init__(self):
        self.submissions_dir = os.path.expanduser("~/.atlas/submissions/code4rena")
        os.makedirs(self.submissions_dir, exist_ok=True)
    
    def get_active_contests(self) -> List[Dict]:
        """Get active Code4rena contests"""
        # In production, this would scrape or use API
        return [
            {
                'id': '2025-03-chainlink',
                'name': 'Chainlink CCIP v1.5',
                'prize_pool': 200000,
                'start_date': '2025-03-01',
                'end_date': '2025-03-15',
                'status': 'active',
                'tags': ['solidity', 'bridge', 'cross-chain'],
                'repo_url': 'https://github.com/code-423n4/2025-03-chainlink'
            },
            {
                'id': '2025-03-eigenlayer',
                'name': 'EigenLayer Restaking',
                'prize_pool': 350000,
                'start_date': '2025-03-10',
                'end_date': '2025-03-24',
                'status': 'active',
                'tags': ['solidity', 'restaking', 'defi'],
                'repo_url': 'https://github.com/code-423n4/2025-03-eigenlayer'
            }
        ]
    
    def generate_finding_report(self, contract: str, issue_type: str, 
                                severity: str, description: str) -> str:
        """Generate a Code4rena-formatted finding report"""
        
        report = f"""## [{severity.upper()}] {issue_type} in {contract}

### Summary
{description}

### Vulnerability Details
```solidity
// Vulnerable code location
{contract}
```

### Impact
[Describe the impact and potential loss]

### Proof of Concept
```solidity
// POC code showing the exploit
```

### Recommended Mitigation
[Provide fix recommendation]

### Tools Used
- Manual review
- Slither
- Foundry tests

---
*Submitted by Atlas AI Agent*
"""
        return report
    
    def submit_finding(self, contest_id: str, contract: str, issue_type: str,
                      severity: str, description: str) -> AuditSubmission:
        """
        Submit a finding to Code4rena.
        In production, this would create a GitHub issue/PR.
        """
        
        # Generate report
        report = self.generate_finding_report(contract, issue_type, severity, description)
        
        # Save locally
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{contest_id}_{severity}_{timestamp}.md"
        filepath = os.path.join(self.submissions_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(report)
        
        # Estimate reward based on severity
        reward_estimates = {
            'critical': 50000,
            'high': 15000,
            'medium': 3000,
            'low': 500
        }
        
        submission = AuditSubmission(
            platform=self.PLATFORM,
            contest_id=contest_id,
            title=f"{severity.upper()}: {issue_type} in {contract}",
            findings=[{
                'contract': contract,
                'issue_type': issue_type,
                'severity': severity
            }],
            severity=severity,
            reward_estimate=reward_estimates.get(severity, 100),
            submitted_at=datetime.now().isoformat(),
            status='submitted'
        )
        
        # Save submission record
        record_path = os.path.join(self.submissions_dir, f"{filename}.json")
        with open(record_path, 'w') as f:
            json.dump({
                'platform': submission.platform,
                'contest_id': submission.contest_id,
                'title': submission.title,
                'severity': submission.severity,
                'reward_estimate': submission.reward_estimate,
                'submitted_at': submission.submitted_at,
                'status': submission.status,
                'report_file': filepath
            }, f, indent=2)
        
        print(f"\n📄 Finding saved: {filepath}")
        print(f"   Severity: {severity.upper()}")
        print(f"   Estimated Reward: ${submission.reward_estimate:,}")
        print(f"\n   Next steps:")
        print(f"   1. Review the report")
        print(f"   2. Add POC code")
        print(f"   3. Submit to Code4rena GitHub")
        
        return submission

class ImmunefiIntegration:
    """
    Immunefi bug bounty integration.
    """
    
    PLATFORM = "immunefi"
    
    def __init__(self):
        self.submissions_dir = os.path.expanduser("~/.atlas/submissions/immunefi")
        os.makedirs(self.submissions_dir, exist_ok=True)
    
    def get_active_programs(self) -> List[Dict]:
        """Get active Immunefi bug bounty programs"""
        return [
            {
                'id': 'aave',
                'name': 'Aave Protocol',
                'max_bounty': 1000000,
                'assets': ['Smart Contracts', 'Web'],
                'scope': 'https://github.com/aave',
                'type': 'bug-bounty'
            },
            {
                'id': 'uniswap',
                'name': 'Uniswap',
                'max_bounty': 2000000,
                'assets': ['Smart Contracts', 'Governance'],
                'scope': 'https://github.com/Uniswap',
                'type': 'bug-bounty'
            },
            {
                'id': 'lido',
                'name': 'Lido Finance',
                'max_bounty': 500000,
                'assets': ['Liquid Staking', 'Node Operators'],
                'scope': 'https://github.com/lidofinance',
                'type': 'bug-bounty'
            }
        ]
    
    def generate_bug_report(self, program: str, severity: str, 
                           vulnerability: str, impact: str) -> str:
        """Generate Immunefi-formatted bug report"""
        
        report = f"""# Bug Report: {program}

## Severity
{severity.upper()}

## Summary
{vulnerability}

## Impact
{impact}

## Vulnerability Details
[Detailed technical description]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Proof of Concept
```solidity
// POC code
```

## Recommended Fix
[Fix recommendation]

## Assets in Scope
- [List affected contracts]

---
Submitted via Atlas AI Agent
"""
        return report
    
    def submit_bug(self, program: str, severity: str, vulnerability: str, 
                  impact: str) -> AuditSubmission:
        """Submit a bug report to Immunefi"""
        
        report = self.generate_bug_report(program, severity, vulnerability, impact)
        
        # Save locally
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"immunefi_{program}_{severity}_{timestamp}.md"
        filepath = os.path.join(self.submissions_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(report)
        
        # Estimate reward
        reward_estimates = {
            'critical': 500000,
            'high': 100000,
            'medium': 10000,
            'low': 1000
        }
        
        submission = AuditSubmission(
            platform=self.PLATFORM,
            contest_id=program,
            title=f"[{severity.upper()}] {vulnerability[:50]}...",
            findings=[{'vulnerability': vulnerability, 'impact': impact}],
            severity=severity,
            reward_estimate=reward_estimates.get(severity, 500),
            submitted_at=datetime.now().isoformat(),
            status='submitted'
        )
        
        # Save record
        record_path = os.path.join(self.submissions_dir, f"{filename}.json")
        with open(record_path, 'w') as f:
            json.dump({
                'platform': submission.platform,
                'program': program,
                'severity': submission.severity,
                'reward_estimate': submission.reward_estimate,
                'submitted_at': submission.submitted_at,
                'status': submission.status,
                'report_file': filepath
            }, f, indent=2)
        
        print(f"\n🐛 Bug report saved: {filepath}")
        print(f"   Program: {program}")
        print(f"   Severity: {severity.upper()}")
        print(f"   Max Reward: ${submission.reward_estimate:,}")
        print(f"\n   ⚠️  IMPORTANT: Review before submitting to Immunefi!")
        print(f"   Real security bugs should be carefully validated.")
        
        return submission

class AtlasPlatformManager:
    """Manage all platform integrations"""
    
    def __init__(self):
        self.code4rena = Code4renaIntegration()
        self.immunefi = ImmunefiIntegration()
    
    def show_opportunities(self):
        """Show all opportunities across platforms"""
        print("=" * 70)
        print("🎯 ATLAS PLATFORM OPPORTUNITIES")
        print("=" * 70)
        
        # Code4rena
        print("\n📋 Code4rena Active Contests:")
        contests = self.code4rena.get_active_contests()
        for c in contests:
            print(f"   💰 ${c['prize_pool']:,} | {c['name']}")
            print(f"      Ends: {c['end_date']} | Tags: {', '.join(c['tags'][:3])}")
        
        # Immunefi
        print("\n🐛 Immunefi Active Programs:")
        programs = self.immunefi.get_active_programs()
        for p in programs:
            print(f"   💰 Up to ${p['max_bounty']:,} | {p['name']}")
            print(f"      Scope: {p['assets'][0]}...")
        
        # Summary
        total_contests = sum(c['prize_pool'] for c in contests)
        total_programs = sum(p['max_bounty'] for p in programs)
        
        print("\n" + "=" * 70)
        print(f"📊 Summary:")
        print(f"   Code4rena Prize Pools: ${total_contests:,}")
        print(f"   Immunefi Max Bounties: ${total_programs:,}")
        print(f"   Total Opportunities: ${total_contests + total_programs:,}")
        print("=" * 70)
    
    def demo_submission(self):
        """Demo a finding submission"""
        print("\n" + "=" * 70)
        print("📝 DEMO: Finding Submission")
        print("=" * 70)
        
        # Demo Code4rena submission
        print("\n1. Code4rena Finding:")
        self.code4rena.submit_finding(
            contest_id='2025-03-chainlink',
            contract='CCIPRouter.sol',
            issue_type='Reentrancy',
            severity='high',
            description='The _ccipReceive function is vulnerable to reentrancy attacks when processing cross-chain messages.'
        )
        
        # Demo Immunefi submission
        print("\n2. Immunefi Bug Report:")
        self.immunefi.submit_bug(
            program='aave',
            severity='critical',
            vulnerability='Flash loan attack can drain reserves',
            impact='Attacker can steal all funds in the lending pool'
        )

def main():
    """Main entry"""
    manager = AtlasPlatformManager()
    manager.show_opportunities()
    manager.demo_submission()
    
    print("\n" + "=" * 70)
    print("✅ Atlas Platform Integrations Ready!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Review generated reports in ~/.atlas/submissions/")
    print("2. Add POC code to reports")
    print("3. Submit to platforms manually (or implement API integration)")
    print("4. Track submissions and rewards")

if __name__ == "__main__":
    main()
