# Why Static Spreadsheets Hide Portfolio Risk

Retail investors who track portfolios in Excel or Google Sheets typically monitor **cost basis**, **unrealized P&L**, and **current allocation pie charts**. Those views are useful for accounting, but structurally blind to quantitative risk.

## Five Blindspots Solved by `investminder/mcp`

| Spreadsheet Blindspot | Why Excel Misses It | Deterministic Fix via `investminder/mcp` |
|---|---|---|
| **1. Illusion of Diversification** | Holding 5 ETFs or 10 stocks looks diversified in a pie chart, even when 4 of them track overlapping US mega-cap tech factors. | `getCorrelationMatrix` computes the exact Pearson correlation of daily returns across 2–20 tickers over multi-year windows, exposing redundant pairs (`r >= 0.80`). |
| **2. Unknown Drawdown & Volatility Exposure** | Static trackers show today's gain/loss, not how severely the allocation fell in 2020 or 2022 or each holding's 12-month volatility. | `analyzeSecurities` (`PERFORMANCE`) returns per-security `volatility12m`, `maxDrawdown12m`, and `drawdown` from all-time high; `startBacktest` + `listBacktests` return full-period `annualPerf`, `globalPerf`, `maxDrawdown`, `totalInflow`, `totalOutflow`, and `annualReturns` across historical regimes. |
| **3. Stale or Missing Rebalancing Impact** | Spreadsheets rarely model periodic rebalancing, cash inflows/outflows, or transaction commissions over time. | `createStrategy` (`REBALANCED` or `PROGRESSIVE`) + `startBacktest` simulate historical returns with realistic commissions, regular contributions (`inflowRules`), and retirement withdrawals (`outflowRules`). |
| **4. Silent Fee & Tax-Wrapper Drag** | Investors often hold higher-TER funds or non-UCITS / non-PEA funds without realizing lower-cost regulated equivalents exist. | `screenSecurities` filters European & US ETFs on `netExpenseRatio`, `regulatoryFramework` (`UCITS`, `PEA`), `distributionPolicy`, `totalAssets`, and multi-year performance. |
| **5. Manual Maintenance Drift** | Copy-pasting prices and trades breaks formulas and leaves portfolios stale for months. | `listInstitutions` + `connectPortfolio` enable read-only broker synchronization via licensed open banking partners (Powens EU, SnapTrade US), or `createPortfolio` + `addPortfolioPosition` maintain a structured cloud ledger. |

## Framing the Value to Spreadsheet Users

When presenting an `excel-to-quant-audit` report, highlight concrete numerical contrasts discovered by the MCP tools — for example:
- *"Your spreadsheet lists 6 separate positions, but `getCorrelationMatrix` shows 4 of them have pairwise daily correlations above `0.85`."*
- *"Your spreadsheet shows positive unrealized P&L today, while `listBacktests` shows this exact weight mix experienced a `-X%` maximum drawdown during its worst historical regime."*
