---
name: withdrawal-stress-test
description: Stress-test a portfolio or strategy for retirement decumulation, financial independence (FIRE), or periodic income withdrawals using Investminder MCP's startBacktest (with outflowRules) and listBacktests across multiple historical market regimes (such as 2000, 2008, and 2022). Use when a user wants to test sequence-of-returns risk, compare fixed-amount vs. percentage withdrawal modes, or inspect drawdowns and outflows during decumulation.
license: MIT
compatibility: Requires the Investminder remote MCP server (https://api.investminder.com/mcp) with OAuth sign-in and an Investminder profile (created via startOnboarding / upsertUser).
metadata:
  author: Investminder
  mcp_repo: https://github.com/investminder/mcp
---

# Retirement & Withdrawal Stress-Test (Sequence-of-Returns Risk)

Test how a strategy behaves under systematic withdrawals (`outflowRules`) across harsh historical start dates using [`investminder/mcp`](https://github.com/investminder/mcp).

## When to Use This Skill

- The user asks to simulate systematic withdrawals from a lump sum — either **fixed-amount withdrawals** (such as the classic 4% rule calculated on initial capital, e.g., *"Backtest €300,000 with no new contributions, withdrawing a fixed €12,000/year starting after 1 year"*, using `regularAmount: 12000, regularPercent: 0`) or **percentage-of-portfolio withdrawals** (e.g., *"withdrawing 4% of the portfolio value each year starting after 1 year"*, using `regularPercent: 4, regularAmount: 0`).
- The user wants to compare sequence-of-returns risk across different allocations (e.g., 100% equities vs. 60/40 vs. a pre-built strategy's UCITS/PEA variant) or across different withdrawal rates.
- The user wants to inspect `totalInflow`, `totalOutflow`, `globalPerf`, `annualPerf`, `maxDrawdown`, and `annualReturns` during decumulation. *(For designing or iterating on the underlying strategy rules themselves before testing withdrawals, hand off to `quant-strategy-backtest`.)*

## Reference Files

- Sequence-of-returns risk concepts, fixed vs. percentage withdrawal mechanics, and historical stress start dates: [references/sequence-risk-guide.md](references/sequence-risk-guide.md)

## Workflow

### Step 1: Select or Build the Strategy Draft

1. **Existing user strategy:** Call `listUserStrategies` (and read the chosen `strategyId` to inspect its `draft` or `live` definition). If it has no active `draft`, call `createStrategy` with its `strategyId` to open a new draft.
2. **Pre-built catalog strategy:** Call `listPreBuiltStrategies`, read the chosen `strategyId`, and — for European investors — apply its official UCITS or PEA `variants` (`currency`, `allocations[].substitute`, `cashManagement`) before copying it into a draft via `createStrategy`.
3. **Custom allocation:** Verify tickers via `searchSecurities`, confirm `REBALANCED` target weights sum to exactly `100%` (plus `constraints.assetClasses`), and create a `DRAFT` via `createStrategy`.
4. Check `earliestDate` via `analyzeSecurities` (`fields: ["PERFORMANCE"]`) on the strategy's tickers so the user knows which historical crises the tickers actually cover (if a newer UCITS ETF starts in 2019, note that 2000/2008 testing requires either a longer-lived proxy or acknowledging the shorter window).

### Step 2: Configure & Launch Withdrawal Backtests (`startBacktest`)

Run one or more asynchronous backtests with `startBacktest`:
- `strategyId`: the draft strategy ID
- `startDate` & `endDate`: test the user's requested window, and offer a **bad-timing stress test** starting right before a major drawdown covered by the holdings (e.g., `2000-01-01`, `2008-01-01`, or `2022-01-01` — see [references/sequence-risk-guide.md](references/sequence-risk-guide.md))
- `inflowRules`: initial capital (and `0` recurring contributions unless the user models an accumulation phase before withdrawals begin)
- `outflowRules`: all four fields are **required** — `delayYears` (integer `>= 1`), `frequency`, `regularAmount`, and `regularPercent`. Choose exactly one withdrawal mode and state it explicitly to the user:
  - **Fixed monetary amount** (`regularAmount > 0`, `regularPercent: 0`): models a constant nominal withdrawal (the classic "4% rule" computed on initial capital); this is the only mode in which capital depletion can occur.
  - **Percentage of portfolio** (`regularPercent > 0`, `regularAmount: 0`): withdraws a percentage of current portfolio value each period; withdrawals shrink during drawdowns, so the portfolio mathematically cannot deplete to zero.

### Step 3: Poll & Analyze Results (`listBacktests`)

1. Poll `listBacktests` with `type: "USER"`, `backtestId`, and `fields: ["PERFORMANCE_METRICS", "ANNUAL_RETURNS"]` until status is `COMPLETED` or `FAILED`.
2. Record whether `startDate` was automatically shifted forward due to quote availability.
3. Report **only** the exact keys returned for both `result` (strategy) and `benchmark`:
   - `totalInflow` and `totalOutflow`
   - `globalPerf` and `annualPerf` (annualized performance)
   - `maxDrawdown`
   - `annualReturns` (reading the lowest entry as the worst calendar year, noting that the first and last years may be partial)
4. Do **not** reconstruct or estimate an ending portfolio value or trough monetary value from these summary metrics; if asked for unavailable metrics, state explicitly that `PERFORMANCE_METRICS` and `ANNUAL_RETURNS` do not return them.

### Step 4: Compare Scenarios & Surface Decumulation Risks

If the user requested sensitivity testing (e.g., 3.5% vs. 4.5% withdrawal, or 60/40 vs. 80/20):
- Run each scenario through `startBacktest` + `listBacktests` and present a side-by-side comparison table using the exact returned keys.
- Highlight the **real-world exclusions** clearly: inflation adjustments (for fixed nominal `regularAmount` withdrawals), personal capital-gains/dividend taxes, and unexpected lump-sum expenses.

## Output Format

1. **Test Parameters & Effective Window** (Strategy, Initial Capital, Withdrawal Mode — fixed `regularAmount` vs. percentage `regularPercent`, `delayYears`, `frequency`, Commission, Requested vs. Effective `startDate` → `endDate`).
2. **Backtest Metrics Table (Strategy vs. Benchmark)** (`totalInflow`, `totalOutflow`, `globalPerf`, `annualPerf`, `maxDrawdown`, and lowest `annualReturns` entry with partial-year note).
3. **Sequence-of-Returns Observations** (Impact of early bear markets on `maxDrawdown` and `annualReturns`, fixed vs. percentage mode implications, and real-world tax/inflation caveats).

## Guardrails

- **Quantitative decision support only:** Never declare a withdrawal rate "safe", never certify retirement readiness, and never recommend a specific allocation or withdrawal plan.
- **Zero mental math:** Never project future retirement balances, Monte Carlo probabilities, ending portfolio values, or inflation-adjusted balances mentally. Report only deterministic outputs returned by `listBacktests` and `analyzeSecurities`, and state clearly when a requested metric is unavailable.
- **Transparent historical limits:** Always state that historical backtests do not include personal taxes, healthcare/inflation shocks, or future market regimes, and that past backtest outcomes do not guarantee future results.
- **No order execution:** Investminder simulates rules and tracks portfolios; it never executes trades or transfers funds.
