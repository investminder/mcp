# Sequence-of-Returns Risk & Withdrawal Stress-Testing Guide

Use this reference when framing `startBacktest` (`outflowRules`) and `listBacktests` results for decumulation and retirement withdrawal simulations.

## What Is Sequence-of-Returns Risk?

During **accumulation**, a market crash early on allows new contributions to buy at lower prices. During **decumulation (withdrawals)**, the exact opposite happens: selling assets during an early bear market permanently reduces the share count, amplifying drawdowns even if long-term average returns look strong.

## Fixed Amount vs. Percentage Withdrawals (`outflowRules`)

Every `outflowRules` object requires `delayYears` (integer `>= 1`), `frequency`, `regularAmount`, and `regularPercent`:

| Mode | Required Fields | Behavior During Drawdowns | Capital Depletion Risk |
|---|---|---|---|
| **Fixed monetary amount** | `regularAmount > 0`, `regularPercent: 0` | Withdraws the same nominal currency amount each period (this is how the classic "4% rule" computed on initial capital is modeled). | **Yes** — forced selling of larger share counts during bear markets can deplete the portfolio. |
| **Percentage of portfolio** | `regularPercent > 0`, `regularAmount: 0` | Withdraws a fixed share of current portfolio value each period; cash payouts drop automatically during bear markets. | **No** — mathematically cannot deplete capital to zero, shifting risk from depletion to income volatility. |

## Key Historical Stress Start Dates

When holdings have sufficient `earliestDate` coverage, these start dates test distinct failure modes:

| Start Window | Historical Stress Mode | Why It Matters for Withdrawals |
|---|---|---|
| **`2000-01-01`** | Dot-com bust + 2008 GFC ("lost decade" for US equities) | Severe early equity drawdown followed by a second crash within 8 years — the harshest modern test for equity-heavy portfolios. |
| **`2008-01-01`** | Global Financial Crisis (`-50%+` equity drawdown) | Immediate deep drawdown right as withdrawals begin, testing whether bonds/gold/cash buffers dampen `maxDrawdown`. |
| **`2022-01-01`** | Inflation & rapid interest-rate hike shock | Both equities and long-duration bonds fell simultaneously, exposing portfolios that assumed negative stock-bond correlation. |

## Important Modeling Caveats to Surface

1. **Nominal vs. Real (Inflation):** A fixed nominal `regularAmount` loses purchasing power over 20+ years of inflation; a `regularPercent` withdrawal fluctuates in currency terms during drawdowns.
2. **UCITS Inception Truncation:** Many European UCITS ETFs launched after 2010–2018. Because `startBacktest` automatically shifts `startDate` forward when quotes are unavailable, always verify the **effective** backtest start date before concluding a strategy was tested through 2008.
3. **Taxes & Fees:** Modeled brokerage commissions are included in `createStrategy`, but personal capital-gains taxes, social charges (e.g., French PFU / prélèvements sociaux), and dividend withholding taxes are **not** modeled in backtests.
4. **Summary Metric Scope:** `listBacktests` (`PERFORMANCE_METRICS`, `ANNUAL_RETURNS`) returns `totalInflow`, `totalOutflow`, `globalPerf`, `annualPerf`, `maxDrawdown`, and `annualReturns` for strategy and benchmark — not ending portfolio value or trough monetary value. Never invent formulas to reconstruct missing figures, and remember that past backtest outcomes do not guarantee future results.
