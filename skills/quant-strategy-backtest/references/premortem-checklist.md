# Strategy Backtest Pre-Mortem Checklist

Before a user treats any `listBacktests` output as decision-ready, walk through these six diagnostic checks using the actual tool outputs:

## 1. Effective Start Date & Regime Coverage
- Did `startBacktest` move `startDate` forward because one ETF (often a newer UCITS fund) had a later `earliestDate`?
- Does the effective period include **at least two distinct stress regimes** (e.g., 2008 Global Financial Crisis, 2020 COVID shock, 2022 inflation & rate-hike drawdown)? A backtest starting in 2023 only tests a bull market.

## 2. Overfitting & Rule Complexity
- How many indicators, thresholds, and parameters were tuned in `createStrategy` (`RSI_14`, `SMA_200`, `MOMENTUM_3_6_12`, tranches)?
- Simpler rules that remain robust across slightly shifted parameters are historically less fragile than finely tuned thresholds that fit past noise.

## 3. Drawdown & Behavioral Endurance
- Look at the backtest's `maxDrawdown` and the lowest entry in `annualReturns` (noting whether the first or last year is a partial calendar year).
- Ask the user plainly: *"Could you realistically keep following these rules without abandoning the plan during a `-X%` drawdown lasting several months or years?"*

## 4. Turnover, Fees & Tax Drag
- Inspect whether a `PROGRESSIVE` or `RANKED` strategy trades frequently (check `TRANSACTIONS` if needed).
- Remind the user that backtests model configured brokerage commissions, but **not** capital gains taxes, dividend withholding taxes, bid-ask spreads, or ETF tracking error (unless reflected in total-return prices).

## 5. Hidden Concentration & Currency Exposure
- Run `getCorrelationMatrix` on the strategy's holdings to verify that multiple tickers are not just repackaging the same underlying equity factor.
- Flag currency mismatch (e.g., a EUR investor holding unhedged USD assets).

## 6. Benchmark Fairness
- Verify that the benchmark matches the strategy's risk profile (e.g., comparing a 60/40 balanced strategy against 100% `SPY` should compare `maxDrawdown` and `annualReturns` dispersion alongside `annualPerf` and `globalPerf`, not bull-market return alone).
