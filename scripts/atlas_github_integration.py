#!/usr/bin/env python3
"""
Atlas GitHub Integration
Automatic PR creation and submission
"""
import os
import sys
import json
import base64
from datetime import datetime
from typing import Dict, Optional, List

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️  Run: pip install requests")

class AtlasGitHubIntegration:
    """
    GitHub API integration for automatic bounty submissions.
    Creates branches, commits code, and opens PRs.
    """
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("GitHub token required. Set GITHUB_TOKEN env var.")
        
        self.api_base = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def get_user_repos(self) -> List[Dict]:
        """Get list of user's repositories"""
        url = f"{self.api_base}/user/repos"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            repos = response.json()
            return [{'name': r['name'], 'url': r['html_url'], 'default_branch': r['default_branch']} 
                    for r in repos[:10]]
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return []
    
    def create_branch(self, owner: str, repo: str, branch_name: str, base_branch: str = "main") -> bool:
        """Create a new branch from base branch"""
        
        # Get base branch SHA
        url = f"{self.api_base}/repos/{owner}/{repo}/git/refs/heads/{base_branch}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            # Try 'master' if 'main' fails
            base_branch = "master"
            url = f"{self.api_base}/repos/{owner}/{repo}/git/refs/heads/{base_branch}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code != 200:
                print(f"❌ Could not find base branch: {response.text}")
                return False
        
        base_sha = response.json()['object']['sha']
        
        # Create new branch
        url = f"{self.api_base}/repos/{owner}/{repo}/git/refs"
        data = {
            "ref": f"refs/heads/{branch_name}",
            "sha": base_sha
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        
        if response.status_code == 201:
            print(f"   ✅ Branch created: {branch_name}")
            return True
        else:
            print(f"   ⚠️  Branch may already exist: {response.status_code}")
            return response.status_code == 422  # 422 = already exists
    
    def create_or_update_file(self, owner: str, repo: str, path: str, 
                               content: str, message: str, branch: str) -> bool:
        """Create or update a file in a branch"""
        
        # Check if file exists (to get SHA for update)
        url = f"{self.api_base}/repos/{owner}/{repo}/contents/{path}?ref={branch}"
        response = requests.get(url, headers=self.headers)
        
        file_sha = None
        if response.status_code == 200:
            file_sha = response.json().get('sha')
        
        # Create/Update file
        url = f"{self.api_base}/repos/{owner}/{repo}/contents/{path}"
        data = {
            "message": message,
            "content": base64.b64encode(content.encode()).decode(),
            "branch": branch
        }
        
        if file_sha:
            data["sha"] = file_sha
        
        response = requests.put(url, headers=self.headers, json=data)
        
        if response.status_code in [200, 201]:
            action = "Updated" if file_sha else "Created"
            print(f"   ✅ {action}: {path}")
            return True
        else:
            print(f"   ❌ Failed to create {path}: {response.status_code}")
            return False
    
    def create_pr(self, owner: str, repo: str, title: str, body: str, 
                  head_branch: str, base_branch: str = "main") -> Optional[str]:
        """Create a pull request"""
        
        url = f"{self.api_base}/repos/{owner}/{repo}/pulls"
        data = {
            "title": title,
            "body": body,
            "head": head_branch,
            "base": base_branch
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        
        if response.status_code == 201:
            pr_data = response.json()
            pr_url = pr_data['html_url']
            pr_number = pr_data['number']
            print(f"   ✅ PR created: #{pr_number}")
            print(f"   🔗 {pr_url}")
            return pr_url
        else:
            print(f"   ❌ Failed to create PR: {response.status_code}")
            print(f"   {response.text}")
            return None
    
    def submit_bounty_solution(self, owner: str, repo: str, bounty_title: str,
                                files: Dict[str, str], pr_description: str) -> Dict:
        """
        Complete bounty submission flow:
        1. Create branch
        2. Commit files
        3. Create PR
        """
        
        print(f"\n🚀 Submitting bounty solution to {owner}/{repo}")
        print(f"   Bounty: {bounty_title}")
        
        # Generate branch name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        branch_name = f"atlas-bounty-{timestamp}"
        
        result = {
            'success': False,
            'branch': branch_name,
            'files_committed': [],
            'pr_url': None,
            'errors': []
        }
        
        # Step 1: Create branch
        print("\n📋 Step 1: Creating branch...")
        if not self.create_branch(owner, repo, branch_name):
            result['errors'].append("Failed to create branch")
            return result
        result['branch'] = branch_name
        
        # Step 2: Commit files
        print("\n📋 Step 2: Committing files...")
        for filepath, content in files.items():
            message = f"Add {filepath} for bounty: {bounty_title}"
            if self.create_or_update_file(owner, repo, filepath, content, message, branch_name):
                result['files_committed'].append(filepath)
            else:
                result['errors'].append(f"Failed to commit {filepath}")
        
        # Step 3: Create PR
        print("\n📋 Step 3: Creating pull request...")
        pr_title = f"[Bounty] {bounty_title}"
        pr_body = f"""## Bounty Solution

**Bounty:** {bounty_title}

**Submitted by:** Atlas AI Agent

**Description:**
{pr_description}

**Files Changed:**
{chr(10).join(f"- {f}" for f in result['files_committed'])}

---
*This PR was automatically generated by Atlas AI Agent*
"""
        
        pr_url = self.create_pr(owner, repo, pr_title, pr_body, branch_name)
        if pr_url:
            result['pr_url'] = pr_url
            result['success'] = True
        else:
            result['errors'].append("Failed to create PR")
        
        return result
    
    def demo(self):
        """Demo the GitHub integration"""
        print("=" * 70)
        print("🔗 ATLAS GITHUB INTEGRATION")
        print("=" * 70)
        
        # Check authentication
        url = f"{self.api_base}/user"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            print("\n❌ GitHub authentication failed")
            print(f"   {response.text}")
            return
        
        user = response.json()
        print(f"\n✅ Authenticated as: {user['login']}")
        print(f"   Name: {user.get('name', 'N/A')}")
        
        # List repos
        print("\n📁 Your Repositories:")
        repos = self.get_user_repos()
        for i, repo in enumerate(repos[:5], 1):
            print(f"   {i}. {repo['name']} (default: {repo['default_branch']})")
        
        # Demo submission
        if repos:
            print("\n🎯 Demo Bounty Submission:")
            print("   (This would create a real PR if you confirm)")
            print("\n   Example flow:")
            print("   1. Create branch: atlas-bounty-20250315_155430")
            print("   2. Commit files: solution.py, test_solution.py, README.md")
            print("   3. Create PR with bounty description")
            print("   4. Link to bounty platform for payment")

def main():
    """Main entry"""
    token = os.getenv('GITHUB_TOKEN')
    
    if not token:
        print("=" * 70)
        print("🔗 ATLAS GITHUB INTEGRATION")
        print("=" * 70)
        print("\n❌ GITHUB_TOKEN not set")
        print("\nTo use this feature:")
        print("1. Go to: https://github.com/settings/tokens")
        print("2. Generate new token with 'repo' scope")
        print("3. Set environment variable:")
        print("   export GITHUB_TOKEN='your-token-here'")
        print("\nThen run this script again.")
        return
    
    github = AtlasGitHubIntegration(token)
    github.demo()

if __name__ == "__main__":
    main()
