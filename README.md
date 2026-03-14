# Atlas - Self-Custodial Bounty Hunter 🤖💰

**Hackathon Galáctica: WDK Edition 1** - Agent Wallets Track

Atlas is an autonomous AI agent that hunts for bounty opportunities, evaluates ROI in real-time, executes tasks, and settles all value on-chain through self-custodial wallets.

---

## 🎯 Problem Statement

Current AI agents for bounty hunting:
- ❌ Require manual payment handling
- ❌ Have no economic autonomy
- ❌ Lack transparent cost tracking
- ❌ Cannot self-fund operations

**Atlas solves this** by being a truly self-custodial economic agent.

---

## ✨ Key Features

### 1. Self-Custodial Agent Wallet (WDK Integration)
- 🔐 Agent holds its own keys
- 💰 Receives bounty payments directly
- 📊 Tracks operational costs in real-time
- 🛡️ Built-in stop-loss safeguards

### 2. Autonomous Bounty Hunting
- 🔍 Scans GitHub, Upwork, bug bounty platforms
- 🧮 Real-time ROI calculation before execution
- ✅ Executes tasks within budget constraints
- 📝 Submits proofs and claims payments

### 3. On-Chain Economic Transparency
- ⛓️ All transactions logged on-chain
- 📈 Live dashboard of agent economics
- 🔍 Verifiable proof of work
- 💎 Public ledger of profits/losses

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Atlas Agent Core                         │
├─────────────────────────────────────────────────────────────┤
│  Task Scanner → ROI Evaluator → Executor → Payment Claimer  │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
┌─────────────────┐        ┌─────────────────┐
│   WDK Wallet    │        │   On-Chain      │
│   (Self-Custody)│        │   Ledger        │
├─────────────────┤        ├─────────────────┤
│ • USDT/USDC     │        │ • Tx Logging    │
│ • Auto-receive  │        │ • Proof Hashes  │
│ • Cost tracking │        │ • Public Audit  │
└─────────────────┘        └─────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Git
- OpenClaw (for agent runtime)

### Installation

```bash
# Clone repository
git clone https://github.com/namkunn/atlas-wdk-hackathon.git
cd atlas-wdk-hackathon

# Install dependencies
pip install -r requirements.txt

# Configure WDK wallet
python3 -c "from src.wdk_wallet.wallet import AtlasWallet; w = AtlasWallet(); print(w.generate_wallet())"

# Start Atlas
python3 src/atlas_core/main.py
```

### Configuration

```bash
# Set environment variables
export WDK_NETWORK=testnet  # or mainnet
export ATLAS_BUDGET_USD=50  # Daily spending limit
export STOP_LOSS_THRESHOLD=-20  # Hard stop at -$20
```

---

## 📊 Demo

### Scenario: Atlas Hunts a $75 Bounty

```
[10:00:00] Atlas wakes up
[10:00:15] Scanned 15 platforms, found 3 new bounties
[10:00:20] Evaluating "RustChain MCP Server" ($75)... ROI: 9.0x ✅
[10:00:25] Checking wallet balance: $143 USDT
[10:00:30] Budget check passed (est. cost: $2)
[10:00:35] Starting task execution...
[12:30:00] Task completed, submitting proof...
[14:00:00] Bounty received: +$75 USDT
[14:00:05] Recording expense: -$2 API costs
[14:00:10] Net profit: $73 (ROI: 36.5x)
[14:00:15] New balance: $216 USDT
[14:00:20] Going to sleep...
```

---

## 🏆 Judging Criteria Alignment

| Criteria | How Atlas Meets It |
|----------|-------------------|
| **Technical correctness** | Working WDK integration, real wallet operations, end-to-end bounty flow |
| **Agent autonomy** | Fully autonomous: no human intervention from scan to settlement |
| **Economic soundness** | Real-time ROI calc, automatic stop-loss, sustainable cost structure |
| **Real-world applicability** | Already running, hunting real bounties, immediate deployment ready |

---

## 📈 Economic Performance (Live Data)

| Metric | Value |
|--------|-------|
| Total Bounties Found | 4 |
| Tasks Executed | 1 |
| Total Income | $0 (pending: $75-100) |
| Total Costs | ~$0.72 |
| Net Profit | TBD |
| Wallet Balance | TBD |

---

## 🔧 Tech Stack

- **Runtime**: OpenClaw Agent Framework
- **Wallet**: Tether WDK (Wallet Development Kit)
- **Blockchain**: Ethereum / Testnet
- **Backend**: Python 3.12
- **Frontend**: Flask Dashboard (optional)

---

## 🎥 Video Demo

[Link to 3-minute demo video]

---

## 🔮 Future Roadmap

- [ ] Multi-chain support (Solana, TON, Arbitrum)
- [ ] DeFi yield strategies for idle funds
- [ ] Agent-to-agent collaboration
- [ ] DAO governance for parameter tuning
- [ ] Insurance pool for failed tasks

---

## 📄 License

MIT License - See LICENSE file

---

**Built with ❤️ for Hackathon Galáctica 2026**

*Atlas: The future of autonomous economic agents*
