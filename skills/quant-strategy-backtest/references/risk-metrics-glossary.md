# Quantitative Backtest & Security Risk Metrics Glossary

Use these concise, accurate definitions when explaining outputs from `listBacktests` and `analyzeSecurities`. Always cite the exact keys and numbers returned by `investminder/mcp`, and state explicitly when a requested metric is not returned by any tool.

## Backtest Metrics (`listBacktests` — Full Backtest Period)

With `fields: ["PERFORMANCE_METRICS", "ANNUAL_RETURNS"]`, `listBacktests` returns identical keys for both `result` (the strategy) and `benchmark`:

- **`annualPerf` (Annualized Performance):** Annualized percentage performance of the strategy (and benchmark) over the effective backtest period. Report verbatim without assuming a specific return-weighting methodology.
- **`globalPerf` (Cumulative Performance):** Total percentage performance over the full backtest period.
- **`maxDrawdown` (Full-Period Maximum Drawdown):** Largest peak-to-trough percentage decline experienced over the entire backtest window (expressed as a negative percentage, e.g., `-18.16%`). A `-50%` drawdown requires a `+100%` gain to break even.
- **`totalInflow` / `totalOutflow`:** Total monetary inflows contributed (`inflowRules`) and total monetary outflows withdrawn (`outflowRules`) across the backtest window.
- **`annualReturns` (`ANNUAL_RETURNS`):** Year-by-year percentage return map (`{"2016": -0.36, "2017": 10.29, ...}`). Read the worst calendar year directly as the lowest value in `annualReturns` — do not recalculate it, and note that the first and last years in the map may be partial calendar years.

*Not returned by `listBacktests` summary fields:* backtest volatility, risk-adjusted ratios, ending portfolio value, or lowest trough portfolio value. Do not estimate or reconstruct them from `PERFORMANCE_METRICS` / `ANNUAL_RETURNS`.

## Per-Security 12-Month & Quote Metrics (`analyzeSecurities` — `PERFORMANCE`)

- **`volatility12m`:** Annualized return volatility over the trailing 12 months for an individual security (in percent; absent when the security has less than 12 months of history).
- **`maxDrawdown12m`:** Worst peak-to-trough loss over the trailing 12 months for an individual security (negative percentage; absent before 12 months of history).
- **`drawdown`:** Current percentage gap between the security's latest close and its all-time highest close.

## Benchmark Comparison & Withdrawal Rules (`outflowRules`)

- **Benchmark Comparison:** Every `listBacktests` response pairs strategy metrics with the benchmark defined in the strategy (`annualPerf`, `globalPerf`, `maxDrawdown`, `totalInflow`, `totalOutflow`, `annualReturns`). Compare both return and `maxDrawdown` — higher return achieved solely through deeper drawdowns is not free alpha.
- **Withdrawal Modes (`outflowRules`):** `delayYears` (integer `>= 1`), `frequency`, `regularAmount`, and `regularPercent` are all required. A withdrawal is either a **fixed monetary amount** (`regularAmount > 0`, `regularPercent: 0`) or a **percentage of the portfolio** (`regularPercent > 0`, `regularAmount: 0`). A percentage withdrawal mathematically cannot deplete capital to zero — capital depletion risk applies only to fixed-amount withdrawals (`regularAmount`). Report `totalInflow`, `totalOutflow`, `globalPerf`, `annualPerf`, `maxDrawdown`, and `annualReturns` for both strategy and benchmark rather than estimating an ending value.
- **Commission & Drag:** Modeled commissions reduce net return, especially in active `PROGRESSIVE` or `RANKED` strategies with frequent turnover. Always state the commission rate used in the draft definition.
