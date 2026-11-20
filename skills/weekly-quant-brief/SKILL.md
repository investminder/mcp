---
name: weekly-quant-brief
description: Generate a structured weekly quantitative portfolio and watchlist brief combining Investminder MCP tools (listPortfolios, listPortfolioTransactions, listUserStrategies, analyzeSecurities, getCorrelationMatrix, and optional listBacktests). Use when a user asks for a weekly portfolio check-in, Sunday market review, allocation drift summary, or watchlist regime update.
license: MIT
compatibility: Requires the Investminder remote MCP server (https://api.investminder.com/mcp) with OAuth sign-in. Portfolio and strategy sections require an Investminder profile; watchlist-only briefs work without one.
metadata:
  author: Investminder
  mcp_repo: https://github.com/investminder/mcp
---

# Weekly Quantitative Portfolio & Watchlist Brief

Produce a calm, disciplined, 5-minute weekly check-in grounded 100% in [`investminder/mcp`](https://github.com/investminder/mcp) data — replacing ad-hoc news scrolling and manual spreadsheet updates.

## When to Use This Skill

- The user asks for their weekly portfolio brief, Sunday review, or a high-level allocation drift summary.
- The user wants a single structured summary of their Investminder portfolios, recent transactions, linked strategies, holding technical regimes, and watchlist tickers.
- The user provides a CSV/XLSX plus watchlist and wants a weekly quantitative snapshot. *(For a detailed cashflow allocation scenario, hand off to `cashflow-rebalance-planner`.)*

## Reference Files

- Output structure template: [assets/brief-output-template.md](assets/brief-output-template.md)

## Workflow

### Step 1: Load Portfolio Holdings, Cash & Recent Activity

If the user has an Investminder profile:
1. Call `listPortfolios` with `includePositions: true` and `includeCashes: true`.
   - Note any `locked: true` portfolios transparently (locked means plan-restricted access, not zero holdings).
   - Note any `tickerRecognized: false` custom positions and mixed currencies (no automatic FX aggregation).
2. For each active unlocked portfolio, call `listPortfolioTransactions` with `minDatetime` set to 7 days ago (`YYYY-MM-DDT00:00:00`, no timezone offset) to summarize the week's recorded deposits, withdrawals, buys, or sells.
3. Call `listUserStrategies` to check any linked `LIVE` strategies (via `portfolio.strategyId`) or active `DRAFT` strategies. If a portfolio is linked to a `REBALANCED` strategy, read that strategy with `strategyId` to produce a **summary** of current vs. target weights (showing the calculation transparently; hand off to `cashflow-rebalance-planner` if the user wants a new-cash contribution scenario).

*(If the user does not have an Investminder profile or asks for a watchlist-only brief, skip Step 1 and run Steps 2–4 on their supplied tickers.)*

### Step 2: Refresh Holding & Watchlist Regimes (`analyzeSecurities`)

1. Resolve any user-supplied watchlist names/ISINs via `searchSecurities`.
2. For the core holdings (up to top 10 by value) and watchlist tickers, call `analyzeSecurities` with `fields: ["PERFORMANCE", "TECHNICAL_INDICATORS"]`, a **short window (a few weeks)** so the daily `technicalIndicators` array stays compact, and `language` matching the user's language (`en`, `fr`, `es`, `de`).
3. Extract `latestDate`, `performance.price`, recent returns (`perfOneMonth`, `perfThreeMonth`, `perfTwelveMonth`), `volatility12m`, `maxDrawdown12m`, current `drawdown`, `scoreTechnical.global.score` (noting `scoreTechnical` also contains sub-scores), and from the **last entry** of `technicalIndicators`: `rsi14` and `sma200` (compared against `performance.price`; note `rsi14` ↔ `RSI_14` and `sma200` ↔ `SMA_200` in strategy rules).
4. **Missing or implausible risk data:**
   - Report any `found: false` ticker transparently without inventing numbers.
   - If `volatility12m` or `maxDrawdown12m` is absent (under 12 months of history or fewer than 200 returns), show **"not available"** — never treat it as zero or interpret it.
   - If a risk or drawdown figure looks implausible for the asset class (e.g., a drawdown beyond `-50%` on an investment-grade bond ETF), flag it as a **possible data anomaly** without commenting on it as a market fact.

### Step 3: Check Portfolio Co-Movement (`getCorrelationMatrix`)

If there are between 2 and 20 recognized tickers across the portfolio (or portfolio + watchlist):
1. Call `getCorrelationMatrix` over the trailing **1-year window** (to spot recent regime shifts) or **3-year window** if the user prefers medium-term stability.
2. Highlight the highest-correlated pair (`>= 0.80`) and lowest-correlated pair (`<= 0.30`).

### Step 4: Compile the Brief Using the Template

Fill in [assets/brief-output-template.md](assets/brief-output-template.md) cleanly:
- Keep the brief scannable (tables + bullet points).
- Surface **summary drift** (with a hand-off to `cashflow-rebalance-planner` for contribution scenarios), **regime flags** (e.g., *"Ticker X closed below `sma200`"*), and **data as-of dates**.
- End with optional research follow-ups without pushing any trade.

## Guardrails

- **Quantitative decision support only:** Never instruct the user to buy, sell, trim, add, or rebalance immediately. Present drift, volatility, drawdown, and regime facts neutrally.
- **Tool-grounded data & transparent arithmetic:** Never invent or estimate market data. Every price, return, volatility, drawdown, correlation, cash balance, and transaction must come from `investminder/mcp` tool outputs. Transparent arithmetic on returned values (such as position value = quantity × `priceLast`, weights, and drift) is permitted when you show the calculation steps (and use a code-execution tool if available). Never sum mixed-currency balances without user-confirmed FX rates.
- **No order execution or credential requests:** Never claim to execute rebalancing trades and never ask for brokerage credentials.
- **Transparent data limits:** Always include `latestDate` from `analyzeSecurities`, note `syncStatus.lastSync` for synchronized portfolios, flag missing risk metrics as `"not available"`, and remind the user that past performance does not guarantee future results.
