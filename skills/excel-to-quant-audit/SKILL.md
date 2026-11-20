---
name: excel-to-quant-audit
description: Inspect an Excel (.xlsx) or CSV (.csv) portfolio tracker or broker export (IBKR, Degiro, Trade Republic, BoursoBank, Saxo, Trading 212), resolve tickers/ISINs via Investminder MCP, and run a deterministic quantitative audit (cross-asset correlation matrix, drawdown & volatility diagnostics, ETF fee/alternative screening, and historical strategy backtest). Use when a user shares a portfolio spreadsheet, asks to audit their Excel/CSV tracker, or wants to migrate from static spreadsheets to Investminder.
license: MIT
compatibility: Requires the Investminder remote MCP server (https://api.investminder.com/mcp) with OAuth sign-in. Strategy backtesting and portfolio sync require an Investminder profile.
metadata:
  author: Investminder
  mcp_repo: https://github.com/investminder/mcp
---

# Excel & CSV to Quantitative Portfolio Audit

Transform a static `.xlsx` or `.csv` portfolio tracker into a structured quantitative audit powered by [`investminder/mcp`](https://github.com/investminder/mcp).

## When to Use This Skill

- The user shares an `.xlsx` or `.csv` file (manual tracker or broker export from IBKR, Degiro, Trade Republic, BoursoBank, Saxo, or Trading 212).
- The user wants to see what their spreadsheet misses: cross-asset correlation, historical drawdown stress-tests, 12-month volatility, or lower-fee UCITS/PEA alternatives.
- The user wants to migrate their spreadsheet holdings into an Investminder manual portfolio or a read-only synchronized broker connection.

## Reference Files

- Column mappings for major US & EU brokers: [references/broker-csv-schemas.md](references/broker-csv-schemas.md)
- Why static spreadsheets fail on risk: [references/spreadsheet-blindspots.md](references/spreadsheet-blindspots.md)
- Sample multi-asset CSV for dry-run demos: [assets/sample-portfolio.csv](assets/sample-portfolio.csv)

## Workflow

### Step 1: Parse the Spreadsheet & Handle Personal Data Transparently

1. **Before reading a user-provided file, note the privacy boundary:** when an AI assistant reads a spreadsheet, the file's contents are transmitted to the AI assistant provider. Recommend that the user remove account numbers, personal names, addresses, and tax IDs **before** sharing the file.
2. Read the `.xlsx` or `.csv` file (or use [assets/sample-portfolio.csv](assets/sample-portfolio.csv) if the user asks for a demo).
3. Map columns using [references/broker-csv-schemas.md](references/broker-csv-schemas.md) to extract only:
   - Identifier (`ISIN`, `Ticker`, or `Name`)
   - `Quantity` and `AvgPrice` / `Market Value` (input records) and/or `TargetWeightPct` (investor-declared target allocation, as in `sample-portfolio.csv`)
   - `Currency` (`EUR`, `USD`, `GBP`, `GBX`, `CHF`)
   - `Asset Class` (if present)
4. Omit any remaining personal identifiers (account numbers, holder names, IBANs, tax IDs) from all Investminder MCP tool calls and output summaries.
5. **Weights & multi-currency rule:**
   - When the file provides a declared `TargetWeightPct` column (such as [assets/sample-portfolio.csv](assets/sample-portfolio.csv)), use `TargetWeightPct` as the target allocation for a `REBALANCED` strategy; treat `Quantity` and `AvgPrice` as entry records, not weights.
   - Current weights **cannot** be computed across lines in different currencies (`EUR`, `USD`, `GBP`, `GBX`, `CHF`) without user-confirmed FX rates. Never silently sum mixed-currency holdings.
   - Flag cash balances separately. If target weights do not sum to `100%`, show the raw sum and ask the user to confirm before calling `createStrategy`.

### Step 2: Resolve Canonical Tickers & Coverage

For each unique holding (prioritizing `ISIN` when present, then ticker/name):

1. Call `searchSecurities` with `query` (ISIN, ticker, or name), optional `assetClass` (`STOCK`, `ETF`, `FOREX`), and `fields: ["PERFORMANCE"]` when fee/performance metadata is helpful.
2. Map each holding to its canonical exchange-qualified Investminder ticker (e.g., `VWCE.DE`, `CW8.PA`, `ASML.AS`, `SPY`, `IGLN.L`).
3. If a security is not covered, list it clearly as **Uncovered** and do not fabricate data or silently substitute another ticker. Offer to search for an equivalent index proxy via `searchSecurities` or `screenSecurities` only with user approval.

### Step 3: Run Quantitative Diagnostics (What Excel Cannot Compute)

Execute these verified `investminder/mcp` tools on the resolved tickers:

1. **Cross-Asset Correlation X-Ray (`getCorrelationMatrix`):**
   - Pass between 2 and 20 resolved tickers with `startDate` (e.g., 5 years ago or earliest common window) and `endDate` (today).
   - Flag `unknownTickers` if returned.
   - Identify hidden concentration clusters (pairwise correlation `>= 0.80`) and genuine diversifiers (`<= 0.30`).
2. **Per-Holding Risk & Regime Snapshot (`analyzeSecurities`):**
   - For the top holdings (or all holdings if `<= 10`), call `analyzeSecurities` with `fields: ["PERFORMANCE", "TECHNICAL_INDICATORS"]` and a short window (a few weeks) when only current technical values are needed.
   - Extract `earliestDate`, `latestDate`, `performance.price`, `volatility12m`, `maxDrawdown12m`, current `drawdown`, and the last entry of `technicalIndicators` (`rsi14`, `sma200`).
   - Note currency units explicitly (`GBX` = British pence, `marketCapUsd` for cross-currency comparison).
   - If `volatility12m` or `maxDrawdown12m` is absent (under 12 months of history or fewer than 200 returns), report it as **"not available"** — never zero or interpreted.
   - If a risk or drawdown figure appears implausible for the asset class (for example, a drawdown beyond `-50%` on an investment-grade bond ETF), flag it to the user as a **possible data anomaly** without commenting on it as a market fact.
3. **Lower-Cost / UCITS / PEA Alternative Check (`screenSecurities`, optional):**
   - For high-fee or non-UCITS ETFs held by European investors, run `screenSecurities` filtering by `assetClass: "ETF"`, `regulatoryFramework` (`UCITS` or `PEA`), `netExpenseRatio`, and `category` to surface comparable regulated alternatives.

### Step 4: Historical Allocation Stress-Test (`createStrategy` + `startBacktest` + `listBacktests`)

If the user has an Investminder profile (otherwise offer `startOnboarding` / `upsertUser`):

1. Propose replicating their declared target allocation (`TargetWeightPct`) as a `DRAFT` `REBALANCED` strategy using `createStrategy`:
   - Confirm target weights (`percentTarget` summing to `100`) and `constraints.assetClasses` (an individual stock maps to `STOCKS`, and an ETF maps to its category — e.g., for `sample-portfolio.csv`: `{"ETF_STOCKS": 60, "STOCKS": 15, "ETF_BONDS": 15, "ETF_COMMODITIES": 10}`).
   - Set an appropriate benchmark (e.g., `SPY` or `VWCE.DE`) and realistic commission.
2. Run `startBacktest` over a multi-regime historical window (e.g., 5–10 years, or the earliest common quote date) with the user's capital and optional monthly `inflowRules`.
3. Poll `listBacktests` with `type: "USER"` and `backtestId` until status is `COMPLETED` (request `fields: ["PERFORMANCE_METRICS", "ANNUAL_RETURNS"]`).
4. Present the exact metrics returned by `listBacktests` for both strategy and benchmark: `annualPerf` (annualized performance), `globalPerf`, `maxDrawdown`, `totalInflow`, `totalOutflow`, and `annualReturns` (reading the lowest entry as the worst calendar year, noting that the first and last years may be partial).

### Step 5: Offer Seamless Migration to Investminder

Present two optional, user-confirmed next steps so the user no longer maintains static spreadsheets:

- **Read-only broker sync:** Call `listInstitutions` to check if their broker is supported via Powens (EU) or SnapTrade (US), then `connectPortfolio` to generate a hosted authorization URL.
- **Manual portfolio import:** With explicit user confirmation, call `createPortfolio`, `addPortfolioCash`, and `addPortfolioPosition` (once per trade; never retry blindly since write calls append operations), then verify via `listPortfolios` with `includePositions: true` and `includeCashes: true`.

## Output Format

Deliver a structured **Spreadsheet-to-Quant Audit Report** with:

1. **Parsed Holdings & Ticker Resolution Table** (Input ID → Canonical Ticker, `TargetWeightPct` or same-currency weight, Currency, Coverage Status, Data As-Of Date).
2. **Hidden Correlation & Concentration Findings** (from `getCorrelationMatrix`).
3. **Risk & Volatility Breakdown** (`volatility12m`, `maxDrawdown12m`, `drawdown` from `analyzeSecurities`, with `"not available"` or data-anomaly flags where applicable).
4. **Historical Backtest Stress-Test** (from `listBacktests`, including benchmark comparison and lowest `annualReturns` entry).
5. **Migration Options** (read-only broker sync vs. manual Investminder portfolio).

## Guardrails

- **Quantitative decision support only:** Never issue buy, sell, or hold recommendations, never state price targets, and never claim a portfolio or alternative ETF is "best" or "suitable" for the user.
- **Tool-grounded data & transparent arithmetic:** Never invent or estimate market data. Every return, correlation, volatility, drawdown, expense ratio, and backtest metric must come from `investminder/mcp` tool outputs. Transparent arithmetic on returned or user-supplied values (such as single-currency position values or weight sums) is permitted when you show the calculation steps (and use a code-execution tool if available).
- **No silent ticker substitution, FX mixing, or weight normalization:** Report uncovered tickers (`found: false` / `unknownTickers`), mixed currencies without confirmed FX rates, and invalid weight sums transparently before proceeding.
- **No banking credentials in chat:** Never ask for broker passwords, 2FA codes, PINs, or IBANs. Broker sync happens solely on the hosted Powens/SnapTrade authorization page via `connectPortfolio`.
- **No order execution:** Investminder never places trades; all execution remains with the user's broker. Past performance and backtests do not guarantee future results.
