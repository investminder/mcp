---
name: cashflow-rebalance-planner
description: Analyze current portfolio allocation drift against a linked or target strategy using Investminder MCP (listPortfolios, listUserStrategies, searchSecurities, analyzeSecurities), with illustrative calculation scenarios showing how an incoming cash deposit affects drift under user-chosen rules alongside a full-rebalance drift reference. Use when a user wants to check portfolio drift vs. target weights or inspect illustrative cashflow rebalancing math.
license: MIT
compatibility: Requires the Investminder remote MCP server (https://api.investminder.com/mcp) with OAuth sign-in and an Investminder profile (for listPortfolios and listUserStrategies). Works on user-supplied holdings + target weights without a stored portfolio.
metadata:
  author: Investminder
  mcp_repo: https://github.com/investminder/mcp
---

# Cashflow & Allocation Drift Rebalance Planner

Analyze live portfolio allocation drift against target weights and present illustrative cashflow arithmetic — strictly as transparent quantitative decision support powered by [`investminder/mcp`](https://github.com/investminder/mcp).

## When to Use This Skill

- The user wants to measure how far their Investminder portfolio (`listPortfolios`) has drifted from its linked `REBALANCED` strategy (`listUserStrategies`) or from a custom target allocation.
- The user wants an illustrative calculation of how an incoming cash deposit (e.g., €1,000 or $2,000) changes post-deposit weights under a specific mathematical rule **without selling** existing positions.
- The user wants a factual drift reference before deciding independently what (if anything) to do at their broker.

## Reference Files

- Cashflow-only vs. full rebalancing concepts, tolerance bands, and multi-currency rules: [references/rebalancing-methods.md](references/rebalancing-methods.md)

## Workflow

### Step 1: Load Portfolio Holdings & Cash (`listPortfolios`)

1. Call `listPortfolios` with `includePositions: true` and `includeCashes: true` (or target a specific `portfolioId`).
2. Check data boundaries immediately:
   - If `locked: true`, stop and inform the user that positions/cashes are restricted by their account plan (never assume zero holdings).
   - Flag any `tickerRecognized: false` custom positions or `priceLast == null` entries — do not invent prices.
   - Check currencies across positions and cashes: `listPortfolios` returns native currencies with **no automatic FX conversion**, and `GBX` is British pence (not GBP). If a portfolio holds mixed currencies, **do not silently sum them**; ask the user for their reference FX rates or evaluate single-currency sleeves separately.

### Step 2: Load Target Allocation (`listUserStrategies` or User Input)

1. If `portfolio.strategyId` is present, call `listUserStrategies` with `strategyId` to read the `live` (or `draft`) target weights (`percentTarget`).
2. Otherwise, use the target weights supplied by the user.
3. **Weight validation:** Verify target weights sum to **exactly 100%**. If they do not, stop and ask the user to confirm corrected target weights before computing drift.
4. For any target ticker not yet held in the portfolio, verify it via `searchSecurities` and fetch `performance.price` via `analyzeSecurities` (`fields: ["PERFORMANCE"]`) if needed, reporting `latestDate`.

### Step 3: Compute Factual Drift & Illustrative Cashflow Scenarios

Using [references/rebalancing-methods.md](references/rebalancing-methods.md) and **only** the returned position quantities, `priceLast` (or `performance.price`), and user-stated deposit amount — showing every calculation step transparently (and using a code-execution tool if the client provides one):

1. **Current vs. Target Drift Table:** For each ticker (in the same currency), show `quantity × priceLast`, current weight (%), target weight (%), and drift in percentage points (`Actual % - Target %`).
2. **Scenario A — Illustrative Cashflow-Only Calculation (No Sells):** Apply the **mathematical rule chosen by the user** (for example, *directing the deposit to the most underweight line* or *splitting pro-rata across underweight gaps*), framed strictly as an arithmetic illustration and not as guidance. If the user has not chosen a rule, present **both** rules side by side without preferring or recommending either.
3. **Scenario B — Full Target Rebalance (Reference Only):** Show the exact monetary gap needed to restore every ticker to its exact target weight (clearly labeled as a mathematical reference, not a trade instruction).
4. Note any tolerance band (e.g., `±5 pp` absolute or `±25%` relative) so small normal market drift is distinguished from material drift.

### Step 4: Optional Strategy & Portfolio Housekeeping

- If the user has a published strategy not yet linked to their portfolio and explicitly asks to link them, mention `linkPortfolioStrategy`.
- If the user later executes trades at their broker and wants to log them in a **manual** Investminder portfolio, confirm exact quantities, prices, and commissions before calling `addPortfolioCash` / `addPortfolioPosition` (never retry blindly).

## Output Format

1. **Portfolio & Strategy Scope** (Portfolio Name, Native Currency, `lastUpdated` / `syncStatus.lastSync`, Linked Strategy or Custom Target, Any Multi-Currency or Missing-Price Caveats).
2. **Current Allocation Drift Table** (Ticker, Units, `priceLast`, Current Value, Current %, Target %, Drift pp).
3. **Illustrative Cashflow Scenario Table** (Rule Applied, Pre-Deposit %, Illustrative Amount per Line, Post-Deposit %, Residual Drift pp — showing both rules neutrally if none was chosen).
4. **Full Rebalance Mathematical Reference** (Currency gap to exact target weights, highlighting tax/commission considerations).

## Guardrails

- **Quantitative decision support only:** Never instruct the user to buy, sell, or place orders. Never present any per-line amount in Scenario A or Scenario B as a buy instruction or allocation advice — label all outputs as illustrative drift arithmetic so the user decides independently.
- **Tool-grounded data & transparent arithmetic:** Never invent or estimate prices or FX rates. Use only `priceLast` from `listPortfolios` or `performance.price` from `analyzeSecurities`. Transparent arithmetic on returned values (`quantity × priceLast`, weights, drift, scenario math) is permitted when you show the calculation steps (and use a code-execution tool if available). Never sum mixed-currency positions without user-confirmed FX rates.
- **No silent weight normalization:** Halt and ask the user if target weights do not sum to 100%.
- **No order execution & no banking credentials:** Investminder never sends orders to brokers and never asks for brokerage passwords, 2FA codes, or IBANs.
