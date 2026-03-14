# Atlas WDK Hackathon Project
# Hackathon Galáctica: WDK Edition 1 - Agent Wallets Track

## Project: Atlas - Self-Custodial Bounty Hunter

### Elevator Pitch
Atlas is an autonomous AI agent that hunts for bounty opportunities, evaluates ROI in real-time, executes tasks, and settles all value on-chain through self-custodial wallets. Built on OpenClaw with WDK wallet integration.

### Track
🤖 Agent Wallets (WDK / Openclaw and Agents Integration)

### Prize Target
- 1st Place: $3,000 USDT
- 2nd Place: $2,000 USDT

---

## Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Atlas Core System                        │
│                  (Already Running)                          │
├─────────────────────────────────────────────────────────────┤
│  • Task Scanner (GitHub/Upwork/Bug Bounty)                  │
│  • ROI Monitor (Real-time cost tracking)                    │
│  • Scheduler (Autonomous execution)                         │
│  • State Persistence (SQLite/JSON)                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
┌─────────────────┐        ┌─────────────────┐
│   WDK Wallet    │        │   On-Chain      │
│   (NEW)         │        │   Settlement    │
├─────────────────┤        │   (NEW)         │
│ • USDT Wallet   │        ├─────────────────┤
│ • Auto-receive  │        │ • Transaction   │
│ • Auto-pay      │        │   logging       │
│ • Balance check │        │ • Proof of work │
└─────────────────┘        │ • Revenue share │
                           └─────────────────┘
```

---

## Core Features for Hackathon

### 1. Self-Custodial Agent Wallet (WDK Integration)
- [ ] Generate/import wallet via WDK
- [ ] Display wallet address & QR
- [ ] Real-time USDT/USDC balance
- [ ] Transaction history

### 2. Economic Loop Closure
- [ ] Auto-deposit bounty earnings
- [ ] Auto-deduct operational costs
- [ ] Profit/loss calculation per task
- [ ] Treasury management

### 3. On-Chain Transparency
- [ ] All economic activity logged on-chain
- [ ] Verifiable proof of work
- [ ] Public dashboard of agent economics

### 4. Autonomous Safeguards
- [ ] Hard stop-loss (on-chain trigger)
- [ ] Daily spending limits
- [ ] Emergency pause mechanism

---

## File Structure

```
~/atlas-hackathon/
├── README.md                  # Project documentation
├── DEMO.md                    # Demo script & video script
├── SUBMISSION.md             # Hackathon submission form
├── src/
│   ├── atlas_core/           # Existing system (symlink/copy)
│   ├── wdk_wallet/
│   │   ├── __init__.py
│   │   ├── wallet.py         # WDK wallet interface
│   │   ├── transactions.py   # USDT/USDC operations
│   │   └── safeguards.py     # Stop-loss & limits
│   ├── on_chain/
│   │   ├── ledger.py         # On-chain activity logging
│   │   └── proofs.py         # Proof of work generation
│   └── api/
│       └── dashboard.py      # Flask/FastAPI dashboard
├── config/
│   └── wdk_config.yaml       # WDK configuration
├── tests/
│   └── test_integration.py   # Integration tests
└── demo/
    └── demo_video.mp4        # Demo video
```

---

## 8-Day Sprint Plan

### Day 1 (Mar 15) - Foundation
- [ ] Register on DoraHacks
- [ ] Join Discord, announce participation
- [ ] Set up project repo
- [ ] Read WDK documentation
- [ ] Generate WDK wallet

### Day 2 (Mar 16) - Wallet Integration
- [ ] Implement wallet.py (WDK wrapper)
- [ ] Balance checking
- [ ] Basic USDT operations
- [ ] Wallet CLI interface

### Day 3 (Mar 17) - Economic Loop
- [ ] Connect Atlas ROI to wallet
- [ ] Auto-cost tracking
- [ ] Profit calculation per task
- [ ] Update INCOME_MANAGEMENT.md

### Day 4 (Mar 18) - On-Chain Logging
- [ ] Implement ledger.py
- [ ] Transaction logging
- [ ] Proof of work hashes
- [ ] Smart contract interaction (if time)

### Day 5 (Mar 19) - Dashboard & UI
- [ ] Build web dashboard
- [ ] Wallet balance display
- [ ] Task history with TX links
- [ ] Real-time metrics

### Day 6 (Mar 20) - Testing & Demo
- [ ] Integration tests
- [ ] Record demo video
- [ ] Write documentation
- [ ] Testnet transactions

### Day 7 (Mar 21) - Polish
- [ ] Code review & optimization
- [ ] Final demo recording
- [ ] Submission form draft
- [ ] Stress test

### Day 8 (Mar 22) - Submit
- [ ] Final submission
- [ ] Double-check requirements
- [ ] Submit before deadline

---

## Judging Criteria Mapping

| Criteria | How Atlas Meets It |
|----------|-------------------|
| **Technical correctness** | Working system with real WDK integration, not mock |
| **Agent autonomy** | Fully autonomous: scan → evaluate → execute → settle |
| **Economic soundness** | Real ROI tracking, stop-loss, cost-benefit analysis |
| **Real-world applicability** | Already hunting real bounties, immediate deployability |

---

## Competitive Advantages

1. **Production Reality** - Not a demo, already running
2. **Self-Custodial** - True agent ownership of funds
3. **Economic Transparency** - All on-chain, auditable
4. **OpenClaw Native** - Fits WDK track perfectly

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| WDK integration issues | Start with wallet generation immediately |
| Time constraint | Focus on core loop, skip nice-to-haves |
| Demo failure | Pre-record critical paths, have backup |

---

## Success Metrics

- [ ] Wallet generates and holds testnet USDT
- [ ] Atlas tracks costs in real USDT terms
- [ ] At least 1 on-chain transaction recorded
- [ ] Dashboard shows live data
- [ ] Demo video < 3 minutes

---

*Project started: 2026-03-14*
*Deadline: 2026-03-22*
*Status: Sprint begins now*
