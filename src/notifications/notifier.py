#!/usr/bin/env python3
"""
Atlas Notification System
Send alerts when bounties are found or tasks completed
"""
import os
import json
import requests
from datetime import datetime
from typing import Dict, Optional

class NotificationManager:
    """Manage notifications for Atlas agent."""
    
    def __init__(self):
        self.discord_webhook = os.getenv("DISCORD_WEBHOOK_URL")
        self.telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    def notify_bounty_found(self, task: Dict) -> bool:
        """Notify when a new bounty is found and approved."""
        message = f"""🎯 **New Bounty Found!**

**{task['title'][:80]}**
💰 Bounty: ${task['bounty']}
📊 ROI: {task.get('roi', 'N/A')}x
🔗 [View Task]({task['url']})

Atlas is evaluating..."""
        
        return self._send_discord(message) or self._send_telegram(message)
    
    def notify_task_approved(self, task: Dict, decision: Dict) -> bool:
        """Notify when a task is approved for execution."""
        message = f"""✅ **Task Approved for Execution**

**{task['title'][:80]}**
💰 Bounty: ${task['bounty']}
💸 Est. Cost: ${task.get('estimated_cost', 'N/A')}
📈 Expected Profit: ${decision.get('expected_profit', 'N/A')}
🎯 ROI: {decision.get('roi', 'N/A'):.1f}x

Atlas will execute this task autonomously."""
        
        return self._send_discord(message) or self._send_telegram(message)
    
    def notify_task_completed(self, task: Dict, result: Dict) -> bool:
        """Notify when a task is completed."""
        profit = result.get('profit', 0)
        profit_emoji = "🟢" if profit > 0 else "🔴"
        
        message = f"""{profit_emoji} **Task Completed**

**{task['title'][:80]}**
💰 Income: ${result.get('income', 0)}
💸 Cost: ${result.get('cost', 0)}
{'🟢' if profit > 0 else '🔴'} Profit: ${profit}

Wallet balance updated."""
        
        return self._send_discord(message) or self._send_telegram(message)
    
    def notify_daily_summary(self, stats: Dict) -> bool:
        """Send daily summary."""
        message = f"""📊 **Atlas Daily Summary**

💰 Total Income: ${stats.get('total_income', 0):.2f}
💸 Total Expenses: ${stats.get('total_expense', 0):.2f}
📈 Net Profit: ${stats.get('net_profit', 0):.2f}
🎯 ROI: {stats.get('roi', 0):.1f}x

📋 Activity:
• Tasks Evaluated: {stats.get('tasks_evaluated', 0)}
• Tasks Approved: {stats.get('tasks_approved', 0)}
• Tasks Executed: {stats.get('tasks_executed', 0)}

🔗 [View Dashboard](https://atlas-wdk-hackathon-production.up.railway.app/)"""
        
        return self._send_discord(message) or self._send_telegram(message)
    
    def _send_discord(self, message: str) -> bool:
        """Send message to Discord webhook."""
        if not self.discord_webhook:
            return False
        
        try:
            payload = {
                "content": message,
                "username": "Atlas Agent"
            }
            response = requests.post(
                self.discord_webhook,
                json=payload,
                timeout=10
            )
            return response.status_code == 204
        except Exception as e:
            print(f"Discord notification failed: {e}")
            return False
    
    def _send_telegram(self, message: str) -> bool:
        """Send message to Telegram."""
        if not self.telegram_bot_token or not self.telegram_chat_id:
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            payload = {
                "chat_id": self.telegram_chat_id,
                "text": message,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            }
            response = requests.post(url, json=payload, timeout=10)
            return response.json().get("ok", False)
        except Exception as e:
            print(f"Telegram notification failed: {e}")
            return False


def test_notifications():
    """Test notification system."""
    print("=" * 60)
    print("Atlas Notification System Test")
    print("=" * 60)
    
    notifier = NotificationManager()
    
    # Test task
    test_task = {
        "title": "Test Bounty Task - Smart Contract Development",
        "bounty": 500,
        "url": "https://github.com/example/test",
        "estimated_cost": 20,
        "roi": 24.0
    }
    
    print("\nSending test notifications...")
    
    print("\n[1] Bounty found notification")
    notifier.notify_bounty_found(test_task)
    
    print("[2] Task approved notification")
    notifier.notify_task_approved(test_task, {"expected_profit": 480, "roi": 24.0})
    
    print("[3] Task completed notification")
    notifier.notify_task_completed(test_task, {"income": 500, "cost": 20, "profit": 480})
    
    print("[4] Daily summary")
    notifier.notify_daily_summary({
        "total_income": 1500,
        "total_expense": 50,
        "net_profit": 1450,
        "roi": 29.0,
        "tasks_evaluated": 10,
        "tasks_approved": 3,
        "tasks_executed": 2
    })
    
    print("\n✅ Test complete!")
    print("\nTo enable notifications, set environment variables:")
    print("  DISCORD_WEBHOOK_URL=your_webhook_url")
    print("  TELEGRAM_BOT_TOKEN=your_bot_token")
    print("  TELEGRAM_CHAT_ID=your_chat_id")


if __name__ == "__main__":
    test_notifications()
