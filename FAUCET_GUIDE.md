# Testnet Faucet Guide for Atlas

## Getting Testnet Funds for Demo

### Step 1: Generate Wallet

```bash
cd atlas-hackathon
python3 src/wdk_wallet/wallet_real.py
```

Save the private key securely!

### Step 2: Get Sepolia ETH (for gas fees)

**Option A: Alchemy Faucet**
- URL: https://sepoliafaucet.com/
- Requires: Alchemy account (free)
- Amount: 0.5 Sepolia ETH/day

**Option B: QuickNode Faucet**
- URL: https://faucet.quicknode.com/ethereum/sepolia
- Requires: QuickNode account (free)
- Amount: 0.05 Sepolia ETH/day

**Option C: Infura Faucet**
- URL: https://www.infura.io/faucet/sepolia
- Requires: Infura account
- Amount: 0.5 Sepolia ETH

**Option D: PoW Faucet (no signup)**
- URL: https://sepolia-faucet.pk910.de/
- Mine small amounts of ETH

### Step 3: Verify Balance

```bash
python3 -c "
from src.wdk_wallet.wallet_real import AtlasRealWallet
w = AtlasRealWallet()
w.update_balances()
print(f\"ETH Balance: {w.get_balance_eth()}\")
"
```

### Step 4: Get Testnet USDT

**Option A: Uniswap on Sepolia**
1. Go to https://app.uniswap.org/#/swap
2. Connect wallet (use testnet mode)
3. Swap some Sepolia ETH for USDT

**Option B: Direct from Contract**
```bash
# Deploy or interact with testnet USDT contract
# USDT Sepolia contract address: [to be updated]
```

**Option C: Use Atlas Mock Mode**
For hackathon demo, mock USDT balances are acceptable as long as:
- Real ETH is used for gas
- Transaction recording is real
- Explorer links work

---

## For Hackathon Judges

Since this is a testnet environment, we demonstrate:

1. **Real Wallet Creation** - Actual Ethereum address generation
2. **Real Gas Costs** - Sepolia ETH for transactions
3. **Real Transaction Recording** - All recorded on local ledger
4. **Real Balance Tracking** - Live ETH balance from chain
5. **Future Mainnet Ready** - Same code works on mainnet

The mock USDT is temporary - on mainnet it becomes real USDT.

---

## Quick Start for Demo

```bash
# 1. Create wallet
python3 src/wdk_wallet/wallet_real.py

# 2. Get Sepolia ETH (0.1 ETH is plenty)
# Visit: https://sepoliafaucet.com/

# 3. Verify balance
python3 -c "from src.wdk_wallet.wallet_real import AtlasRealWallet; w = AtlasRealWallet(); w.update_balances(); print(w.get_economics_summary())"

# 4. Show in dashboard
# (Dashboard integration coming in Day 3)
```

---

## Testnet Explorer

View your transactions:
- **Sepolia Explorer**: https://sepolia.etherscan.io/
- Enter your wallet address to see activity

---

## Important Notes

1. **Testnet ETH has no real value** - it's only for testing
2. **Save your private key** - you'll need it to recover the wallet
3. **Don't use mainnet funds** - this is testnet only
4. **Faucets have limits** - be patient if you need to wait

---

*Last updated: 2026-03-14*
