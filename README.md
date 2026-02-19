# Trading Bot — Binance Futures Style

A Python CLI trading bot that places Market, Limit, and Stop-Market
orders against a local mock exchange that simulates the Binance Futures API.
Built with clean layered architecture, structured logging, and full error handling.

---

## Project Structure
```
trading_bot/
├── bot/
│   ├── __init__.py          # Package marker
│   ├── client.py            # API client with HMAC-SHA256 signing
│   ├── logging_config.py    # File + console logging setup
│   ├── mock_exchange.py     # Local mock Binance Futures exchange
│   ├── orders.py            # Order placement logic
│   └── validators.py        # Input validation
├── frontend/
│   └── index.html           # Web UI (bonus)
├── logs/                    # Auto-generated log files
├── cli.py                   # CLI entry point
├── server.py                # Flask web server (bonus)
├── requirements.txt
├── Procfile                 # For Railway deployment
└── README.md
```

---

## Setup

### 1. Clone the Repository
```
git clone https://github.com/PrachiMishra7/trading_bot.git
cd trading_bot
```

### 2. Create Virtual Environment
```
python -m venv .venv
```

### 3. Activate Virtual Environment

Windows:
```
.venv\Scripts\activate
```

Mac/Linux:
```
source .venv/bin/activate
```

### 4. Install Dependencies
```
pip install -r requirements.txt
```

---

## How to Run (CLI)

### Market Buy
```
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Market Sell
```
python cli.py --symbol BTCUSDT --side SELL --type MARKET --quantity 0.001
```

### Limit Buy
```
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 95000
```

### Limit Sell
```
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 120000
```

### Stop-Market Sell (Bonus)
```
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 58000
```

---

## Expected Output
```
───────────────────────────────────────────────────────
  ORDER REQUEST SUMMARY
───────────────────────────────────────────────────────
  Symbol    : BTCUSDT
  Side      : BUY
  Type      : MARKET
  Quantity  : 0.001
───────────────────────────────────────────────────────
  ORDER RESPONSE
───────────────────────────────────────────────────────
  Order ID      : 1001
  Status        : FILLED
  Symbol        : BTCUSDT
  Side          : BUY
  Type          : MARKET
  Orig Qty      : 0.001
  Executed Qty  : 0.001
  Avg Price     : 97043.21
───────────────────────────────────────────────────────

  ✓ Success! orderId = 1001
```

---

## How to Run (Web UI)
```
python server.py
```

Then open your browser and go to:
```
http://localhost:8000
```

---

## CLI Options

| Flag | Required | Description |
|---|---|---|
| --symbol | ✅ Yes | Trading pair e.g. BTCUSDT |
| --side | ✅ Yes | BUY or SELL |
| --type | ✅ Yes | MARKET, LIMIT, or STOP_MARKET |
| --quantity | ✅ Yes | Positive number e.g. 0.001 |
| --price | LIMIT only | Limit price e.g. 95000 |
| --stop-price | STOP_MARKET only | Trigger price e.g. 58000 |
| --time-in-force | No | GTC, IOC, or FOK (default GTC) |

---

## Logging

Every run automatically logs to `logs/trading_bot_YYYYMMDD.log`

- **DEBUG** (file only) — full request and response details
- **INFO** (file + terminal) — order summary and result
- **ERROR** (file + terminal) — API errors and failures

Sample log output:
```
2026-02-19 10:22:01 | INFO     | trading_bot | Logging started
2026-02-19 10:22:01 | INFO     | trading_bot.orders | Placing MARKET BUY | symbol=BTCUSDT qty=0.001
2026-02-19 10:22:02 | INFO     | trading_bot.orders | Market order done. orderId=1001 avgPrice=97043.21
2026-02-19 10:22:02 | INFO     | trading_bot | Done.
```

---

## Error Handling

| Scenario | Behaviour |
|---|---|
| Missing --price for LIMIT | Rejected before API call with clear message |
| Invalid symbol | Rejected by validator with helpful message |
| Wrong side value | Rejected — must be BUY or SELL |
| Negative quantity | Rejected — must be greater than zero |
| API error | Logged and printed with error code and message |
| Network failure | Caught and logged with friendly message |

---

## Architecture
```
CLI (cli.py)
    ↓
validators.py     ← validates all inputs
    ↓
orders.py         ← builds order parameters
    ↓
client.py         ← signs and sends HTTP request
    ↓
mock_exchange.py  ← simulates Binance Futures API
```

---

## Assumptions

1. Uses a local mock exchange instead of real Binance Testnet
   so no API keys are needed to run and test
2. Mock exchange simulates real Binance Futures REST API responses
   including HMAC-SHA256 signing (same as real Binance)
3. STOP_MARKET included as bonus third order type
4. Supports BTCUSDT, ETHUSDT, and SOLUSDT pairs
5. Web UI available as bonus feature via python server.py

---

## Deployment

Deployed on Railway:
```
https://trading-bot-production.up.railway.app
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.x | Core language |
| Flask | Mock exchange + web server |
| Requests | HTTP client |
| argparse | CLI argument parsing |
| hmac + hashlib | Request signing (Binance style) |
| logging | Structured file and console logs |
