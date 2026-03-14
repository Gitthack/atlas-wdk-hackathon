# WDK Integration Research & Implementation

## Finding WDK Resources

### Step 1: Check Hackathon Discord
The WDK documentation should be linked in:
- Discord #resources channel
- Hackathon main page
- DoraHacks project submission page

### Step 2: WDK GitHub (Expected Structure)
Based on typical wallet SDKs, WDK likely has:
```
Tether/WDK or similar repo
├── docs/
│   ├── quickstart.md
│   └── api-reference.md
├── sdk/
│   ├── python/
│   ├── typescript/
│   └── rust/
└── examples/
    └── basic-wallet/
```

### Step 3: Testnet Faucet
Usually available at:
- Tether testnet portal
- ETH testnet faucets (Goerli/Sepolia)
- USDT testnet contracts

---

## Implementation Strategy (Without Full Docs)

Since WDK docs may be limited, we'll implement:

### Option A: Ethers.js/Web3.py Integration (Compatible with WDK)
Most wallet SDKs are wrappers around standard libraries.

```python
# Using web3.py for Ethereum testnet
from web3 import Web3

# Connect to testnet
w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/YOUR_KEY'))

# USDT Testnet Contract
USDT_CONTRACT = '0x...'  # Sepolia USDT
```

### Option B: Direct WDK API Calls
If WDK has REST API:
```python
import requests

WDK_API = 'https://api.wdk.tether.io/v1'

# Create wallet
response = requests.post(f'{WDK_API}/wallets', json={...})
```

---

## Immediate Action Plan

Since we need to move forward, let's:

1. **Create testnet-ready wallet code** that can switch between mock and real
2. **Set up Sepolia testnet** (Ethereum testnet that supports USDT)
3. **Get testnet ETH + USDT** from faucets
4. **Document the integration** for hackathon judges

This approach shows technical competence even if WDK specific docs are sparse.

---

## Sepolia Testnet Setup (Ethereum)

### Why Sepolia?
- Standard Ethereum testnet
- USDT testnet contracts available
- Easy faucet access
- Compatible with WDK architecture

### Steps:
1. Get Sepolia ETH from faucet
2. Deploy/interact with USDT testnet contract
3. Record transactions on testnet
4. Show explorer links as proof

---

## Code Structure Update

We'll create:
1. `wallet_real.py` - Real testnet integration
2. `config_testnet.yaml` - Testnet configuration  
3. `faucet_guide.md` - How to get testnet funds

This gives us real on-chain activity to show judges.
