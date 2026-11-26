---
name: quant-strategy-backtest
description: Translate a plain-English investment thesis or pre-built template into a structured Investminder strategy (REBALANCED, PROGRESSIVE, or RANKED) using createStrategy/updateStrategy, run an asynchronous historical simulation with startBacktest (including contributions, withdrawals, and commissions), poll results via listBacktests, and deliver a quantitative pre-mortem. Use when a user wants to design, modify, or backtest a rules-based ETF or stock strategy.
license: MIT
compatibility: Requires the Investminder remote MCP server (https://api.investminder.com/mcp) with OAuth sign-in and an Investminder profile (created via startOnboarding / upsertUser).
metadata:
  author: Investminder
  mcp_repo: https://github.com/investminder/mcp
---

# Quantitative Strategy Design, Backtest & Pre-Mortem

Convert a plain-English investment thesis into a deterministic, auditable historical backtest using [`investminder/mcp`](https://github.com/investminder/mcp), followed by a structured risk pre-mortem.

## When to Use This Skill

- The user describes a rules-based investment idea (e.g., 60/40 quarterly rebalanced ETFs, SMA 200 trend-following, or RSI dip-buying with value averaging). *(For systematic withdrawal / decumulation testing with `outflowRules`, hand off to `withdrawal-stress-test`.)*
- The user wants to adapt a ready-made strategy from Investminder's catalog (`listPreBuiltStrategies`), apply official UCITS/PEA `variants`, and backtest the modified draft.
- The user wants to iterate on an existing draft strategy (`listUserStrategies`, `updateStrategy`) and compare metrics against a benchmark.

## Reference Files

- Metric definitions and interpretation: [references/risk-metrics-glossary.md](references/risk-metrics-glossary.md)
- Overfitting, survivorship, and regime pre-mortem checklist: [references/premortem-checklist.md](references/premortem-checklist.md)

## Workflow

### Step 1: Verify Profile & Resolve Strategy Universe

1. If starting from a pre-built template, call `listPreBuiltStrategies` (filterable by `approach`: `TREND_FOLLOWING`, `BALANCED`, `DIVIDEND_FOCUSED`, `CORE_SATELLITE`, `MEAN_REVERSION`; `diversification`; `activity`: `PASSIVE_INVESTOR`, `ACTIVE_INVESTOR`). Read the chosen strategy alone with `strategyId` to retrieve its full `definition`, `constraints`, and official `variants`.
2. **Use official UCITS / PEA `variants` first:** Pre-built strategies already ship with curated `variants` (UCITS systematically, and PEA for eligible strategies), each specifying `currency`, `allocations` (`ticker` → `substitute`), and `cashManagement`. When a European investor asks for a UCITS or PEA version of a pre-built strategy, apply the matching variant directly rather than manually hunting substitutes with `screenSecurities`.
3. For custom theses (or holdings outside a pre-built variant), resolve every candidate ticker via `searchSecurities` or `screenSecurities`. Never pass unverified tickers to `createStrategy`.
4. Check quote history depth (`earliestDate`) with `analyzeSecurities` (`fields: ["PERFORMANCE"]`) if the user expects a long historical window (e.g., since 2008).

### Step 2: Construct & Validate the Strategy Draft

Choose the exact `strategyModel` matching the user's thesis:

- **`REBALANCED`**: Fixed target weights (`percentTarget`) summing to **exactly 100%**. Leave `percentMax`, `sharesMax`, and `valueAveraging` null. **Required:** pass `constraints.assetClasses` matching the allocations' asset classes (e.g., `{"ETF_STOCKS": 60, "ETF_BONDS": 40}`) and summing to 100%.
- **`PROGRESSIVE`**: Signal-driven exposure with per-asset caps (`percentMax` or `sharesMax`) and optional buy/sell triggers (`RSI_14`, `RSI_21`, `DRAWDOWN`, `MOMENTUM_1_3_6`, `MOMENTUM_3_6_12`, `EMA_20`, `EMA_50`, `SMA_100`, `SMA_200`, `MACD`, `MACD_SIGNAL`, `ATR`, `PRICE`, `ALLOCATION_GAP`, `MONTH_INDEX`) plus optional DCA or `valueAveraging`.
- **`RANKED`**: 2 to 50 candidate tickers with no fixed weights, `ranking` rules filled, and `dca` / `valueAveraging` left null.

**Validation rule:** If the user's proposed `REBALANCED` weights do not sum to 100% (e.g., 110%), **do not silently normalize them**. Flag the exact sum and ask the user to confirm corrected weights before calling `createStrategy` or `updateStrategy`.

Call `createStrategy` (passing `name` for a new strategy, or `strategyId` to open a new draft on a published strategy) with `definition` and `constraints` (including optional `regulatoryFramework`: `UCITS` or `PEA`). To revise an existing draft, call `updateStrategy` with the complete `definition`.

### Step 3: Run & Poll the Asynchronous Backtest

1. Call `startBacktest` on the draft `strategyId` with:
   - `startDate` and `endDate` (`YYYY-MM-DD`)
   - `inflowRules` (initial capital + optional recurring contributions)
   - `outflowRules` (optional withdrawal rules requiring `delayYears` >= 1, `frequency`, `regularAmount`, and `regularPercent` — either fixed amount with `regularPercent: 0` or percentage with `regularAmount: 0`)
2. `startBacktest` returns a `PENDING` backtest with a `backtestId`.
3. Poll `listBacktests` with `type: "USER"`, `backtestId`, and `fields: ["PERFORMANCE_METRICS", "ANNUAL_RETURNS"]` until status is `COMPLETED` or `FAILED`. Request `HOLDINGS`, `TRANSACTIONS`, or `DIVIDENDS` only if the user explicitly needs daily series.

### Step 4: Deliver Backtest Summary & Quantitative Pre-Mortem

1. Present strategy vs. benchmark metrics verbatim from `listBacktests` (see [references/risk-metrics-glossary.md](references/risk-metrics-glossary.md)): `annualPerf` (annualized performance), `globalPerf`, `maxDrawdown`, `totalInflow`, `totalOutflow`, and `annualReturns` (reading the lowest entry as the worst calendar year, noting that the first and last calendar years may be partial).
2. Note whether `startDate` was automatically moved forward due to a holding's inception date.
3. Run the 6-point pre-mortem from [references/premortem-checklist.md](references/premortem-checklist.md) covering lookback bias, regime coverage, fee/tax drag, correlation convergence, and behavioral drawdown tolerance.
4. Only if the user explicitly asks to go live or discard the draft:
   - `publishStrategy` promotes the draft to `LIVE` (and `linkPortfolioStrategy` links a portfolio to a published strategy).
   - `deleteStrategy` deletes an unwanted draft and its backtests.

## Guardrails

- **Quantitative decision support only:** Never recommend adopting, publishing, or trading a strategy. Present historical simulation outputs and risks neutrally so the user decides.
- **Zero mental math:** Report only metrics returned by `listBacktests` and `analyzeSecurities`. If a metric is not returned by any tool (such as backtest volatility or ending portfolio value), state explicitly that it is unavailable and never estimate it.
- **No silent weight normalization:** Always halt and ask the user if `REBALANCED` target weights do not sum to 100%.
- **Explicit backtest disclaimers:** Always state that backtests are hypothetical historical simulations, exclude personal taxes and slippage beyond modeled commissions, and do not guarantee future results.
- **No order execution:** Publishing or linking a strategy tracks rules and alerts only; Investminder never executes trades.
