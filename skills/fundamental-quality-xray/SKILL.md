---
name: fundamental-quality-xray
description: Audit a public company's multi-year financial quality, balance-sheet resilience, dividend sustainability, and historical P/E valuation using Investminder MCP (searchSecurities, analyzeSecurities with FINANCIAL_STATEMENTS, DIVIDENDS, PER, and PERFORMANCE, plus screenSecurities for peer context). Use when a user asks for a fundamental deep dive on a stock, multi-year revenue/margin/FCF history, dividend track record, or historical valuation multiples.
license: MIT
compatibility: Requires the Investminder remote MCP server (https://api.investminder.com/mcp) with OAuth sign-in and an Investminder profile (FINANCIAL_STATEMENTS, DIVIDENDS, and PER depth depend on the user's plan).
metadata:
  author: Investminder
  mcp_repo: https://github.com/investminder/mcp
---

# Fundamental Quality & Valuation X-Ray

Deliver a structured, multi-year fundamental audit of any covered US or European stock using deterministic financial statements, dividend history, and P/E series from [`investminder/mcp`](https://github.com/investminder/mcp).

## When to Use This Skill

- The user asks for a fundamental review of a stock (e.g., *"Analyze ASML.AS: 10 years of yearly revenue, margins, free cash flow, dividends, and P/E history"*).
- The user wants to check dividend regularity and payout sustainability before researching an income stock.
- The user wants to compare a company's current valuation and quality metrics against sector peers.

## Reference Files

- Fundamental quality, balance-sheet, dividend, and P/E interpretation framework: [references/fundamental-checklist.md](references/fundamental-checklist.md)

## Workflow

### Step 1: Resolve Canonical Stock Ticker

1. Call `searchSecurities` with the company name, ticker, or ISIN, `assetClass: "STOCK"`, and `fields: ["DESCRIPTION"]` if business context is needed.
2. Confirm the exact exchange listing (e.g., `ASML.AS` in Amsterdam vs. `ASML` on Nasdaq; `NESN.SW` in Zurich) and note its quote currency (`GBX` = British pence, not GBP).

### Step 2: Fetch Multi-Year Fundamental Data (`analyzeSecurities`)

Call `analyzeSecurities` on the canonical `ticker` with:
- `fields`: `["PERFORMANCE", "FINANCIAL_STATEMENTS", "DIVIDENDS", "PER"]`
- `statementFrequency`: `"YEARLY"` for multi-year structural trends (default) or `"QUARTERLY"` for recent inflection points
- `quoteFrequency`: `"WEEKLY"` (or `"DAILY"` for short windows) to keep `PER` series compact
- `startDate` / `endDate`: e.g., last 5–10 years (plan tier determines available history depth)
- `language`: `en`, `fr`, `es`, or `de`

**Coverage & data hygiene:**
- If `found: false` is returned, stop and report that the ticker is not covered; never invent financials.
- Report `earliestDate` and `latestDate`, and clearly distinguish **missing periods** from **zero values**.
- If a plan limit restricts statement or dividend depth, state what was returned transparently without extrapolating missing years.

### Step 3: Evaluate Five Fundamental Pillars

Apply [references/fundamental-checklist.md](references/fundamental-checklist.md) strictly to the returned numbers:

1. **Growth Trajectory:** Multi-year revenue, operating income, net income, EPS, and free cash flow trends (plus share count trend — dilution vs. buybacks).
2. **Profitability & Capital Efficiency:** Gross, operating, and net margins, plus `roe` and `roic` from `PERFORMANCE`.
3. **Balance-Sheet Resilience:** `debtEquityRatio`, `currentRatio`, and cash generation relative to obligations.
4. **Dividend Track Record (`DIVIDENDS`):** Payment consistency, growth or cuts across years, current `dividendYield`, and `dividendPayoutRatio`.
5. **Historical Valuation Context (`PER`):** Compare current P/E against the company's own historical P/E range over the returned window (never call it "cheap" or "expensive" as a buy/sell trigger; frame it as percentile/range context).

### Step 4: Peer Context (Optional via `screenSecurities`)

If the user asks how the company stacks up against peers:
- Call `screenSecurities` filtering by `assetClass: "STOCK"` and matching `sector` or `industry` (and optionally `stockIndex` or `country`), with `fields: ["PERFORMANCE"]` and `sortBy: "MARKET_CAP"`, `sortOrder: "DESC"`.
- Compare peer market caps strictly on `marketCapUsd` (never raw mixed-currency `marketCap`).

## Output Format

1. **Company & Data Scope Header** (Canonical Ticker, Currency, Statement Frequency, Periods Returned, `latestDate`).
2. **Multi-Year Financial Summary Table** (Fiscal Period, Revenue, Operating/Net Margin, Net Income, Free Cash Flow, Dividends Paid).
3. **Quality, Balance-Sheet & Valuation Snapshot** (`roe`, `roic`, `debtEquityRatio`, `currentRatio`, `dividendYield`, `dividendPayoutRatio`, Current vs. Historical `PER` range, `scoreFinancial.global.score` (0–10; note that `scoreFinancial` is an object with component sub-scores, which are `null` for ETFs except `shareholderReturn`)).
4. **Key Strengths & Risk Flags** (factual observations only, e.g., margin compression, rising debt, dividend cut, or elevated valuation vs. own history).

## Guardrails

- **Quantitative decision support only:** Never issue buy, sell, or hold ratings, never assign fair-value price targets, and never claim a stock is "undervalued — buy" or "overvalued — sell".
- **Zero mental math:** Report only figures returned by `analyzeSecurities`, `searchSecurities`, and `screenSecurities`. Do not fabricate missing historical fiscal years or estimate next-year EPS.
- **Strict currency & missing-data discipline:** State the reporting and quote currencies explicitly, distinguish missing data from zero, and compare cross-border peers on `marketCapUsd`.
- **Past fundamentals do not guarantee future results:** Remind the user that historical margins, dividends, and valuation ranges can change materially.
