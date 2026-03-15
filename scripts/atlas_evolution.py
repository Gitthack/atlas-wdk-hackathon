#!/usr/bin/env python3
"""
Atlas Evolution - Combined A + B
New platforms + AI execution in one command
"""
import os
import sys
import asyncio
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from atlas_enhanced_scanner import EnhancedAtlasScanner, BountyTask
from atlas_ai_execution import AIExecutionEngine

class AtlasEvolution:
    """
    Combined scanner + AI execution
    Phase 1: New platforms (A)
    Phase 2: AI execution (B)
    """
    
    def __init__(self):
        self.scanner = EnhancedAtlasScanner()
        self.ai_engine = AIExecutionEngine()
        
    async def run(self):
        """Run full evolution cycle"""
        print("=" * 70)
        print("🚀 ATLAS EVOLUTION - Phase A + B")
        print("   New Platforms + AI Execution")
        print("=" * 70)
        print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Phase A: Scan new platforms
        print("\n" + "=" * 70)
        print("📡 PHASE A: Multi-Platform Scan")
        print("=" * 70)
        
        results = await self.scanner.scan_all()
        
        # Collect all tasks
        all_tasks = []
        for platform, tasks in results.items():
            all_tasks.extend(tasks)
        
        # Sort by bounty amount
        all_tasks.sort(key=lambda x: x.bounty_amount, reverse=True)
        
        print("\n📊 Top 5 High-Value Opportunities:")
        print("-" * 70)
        for i, task in enumerate(all_tasks[:5], 1):
            print(f"{i}. 💰 ${task.bounty_amount:,.0f} {task.currency}")
            print(f"   Platform: {task.platform}")
            print(f"   Title: {task.title}")
            print(f"   Difficulty: {task.difficulty}")
            print(f"   Tags: {', '.join(task.tags)}")
            print()
        
        # Phase B: AI Execution Analysis
        print("=" * 70)
        print("🤖 PHASE B: AI Execution Analysis")
        print("=" * 70)
        
        ai_executable = []
        human_required = []
        
        for task in all_tasks:
            # Categorize by executability
            if task.difficulty == 'critical':
                human_required.append(task)
            elif any(tag in ['documentation', 'tests', 'refactoring'] for tag in task.tags):
                ai_executable.append(task)
            else:
                human_required.append(task)
        
        print(f"\n📝 AI-Executable Tasks: {len(ai_executable)}")
        print(f"👤 Human-Required Tasks: {len(human_required)}")
        
        if ai_executable:
            print("\n🤖 AI Can Handle:")
            for task in ai_executable[:3]:
                print(f"   • {task.title} (${task.bounty_amount:,.0f})")
        
        if human_required:
            print("\n👤 Requires Human Expertise:")
            for task in human_required[:3]:
                print(f"   • {task.title} (${task.bounty_amount:,.0f}) [{task.difficulty}]")
        
        # Summary
        total_pool = sum(t.bounty_amount for t in all_tasks)
        ai_pool = sum(t.bounty_amount for t in ai_executable)
        
        print("\n" + "=" * 70)
        print("📈 EVOLUTION SUMMARY")
        print("=" * 70)
        print(f"Total Opportunities: {len(all_tasks)}")
        print(f"Total Prize Pool: ${total_pool:,.0f}")
        print(f"AI-Executable Pool: ${ai_pool:,.0f} ({ai_pool/total_pool*100:.1f}%)")
        print(f"Platforms: {len(results)}")
        print(f"New Platforms: Code4rena, Immunefi")
        print("=" * 70)
        
        return {
            'total_tasks': len(all_tasks),
            'total_value': total_pool,
            'ai_executable': len(ai_executable),
            'ai_value': ai_pool,
            'platforms': list(results.keys())
        }

async def main():
    atlas = AtlasEvolution()
    result = await atlas.run()
    
    print("\n✅ Atlas Evolution cycle complete!")
    print(f"   Next: Set up OPENAI_API_KEY for real AI execution")
    print(f"   Then: Run 'python3 atlas_ai_execution.py' for demo")

if __name__ == "__main__":
    asyncio.run(main())
