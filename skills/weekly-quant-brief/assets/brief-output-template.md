# Weekly Quantitative Brief — {{WEEK_ENDING_DATE}}

> **Scope:** Decision-support summary generated from Investminder MCP data. Not investment advice; past performance does not guarantee future results.

## 1. Portfolio Snapshot & Cash Balances

*Source: `listPortfolios` (`includePositions: true`, `includeCashes: true`)*

| Portfolio | Currency | Linked Strategy | Open Positions | Cash Balances (Native CCY) | Last Sync / Updated |
|---|---|---|---|---|---|
| {{PORTFOLIO_NAME}} | {{CCY}} | {{STRATEGY_NAME_OR_NONE}} | {{POS_COUNT}} | {{CASH_SUMMARY}} | {{LAST_UPDATED}} |

*Note: Cash and positions are displayed in their native currencies without automatic FX conversion.*

## 2. Allocation Drift Summary (If Linked to a `REBALANCED` Strategy)

*Source: `listPortfolios` + `listUserStrategies` (summary only — use `cashflow-rebalance-planner` for a new-cash contribution scenario)*

| Ticker | Current Weight (%) | Strategy Target (%) | Drift (pp) |
|---|---|---|---|
| {{TICKER}} | {{ACTUAL_PCT}} | {{TARGET_PCT}} | {{DRIFT_PP}} |

## 3. Trailing 7-Day Recorded Activity

*Source: `listPortfolioTransactions`*

- {{DATE}} — `{{TYPE}}` — {{NAME}} — {{AMOUNT}} {{CURRENCY}} (Fee: {{COMMISSION}})
- *(Or: No recorded transactions in the last 7 days.)*

## 4. Holdings & Watchlist Technical Regime

*Source: `analyzeSecurities` (`PERFORMANCE`, `TECHNICAL_INDICATORS` — last entry of daily `technicalIndicators` compared against `performance.price`)*

| Ticker | Group | As-Of Date | `performance.price` vs. `sma200` | `rsi14` | `volatility12m` | `drawdown` | `maxDrawdown12m` | `scoreTechnical.global.score` |
|---|---|---|---|---|---|---|---|---|
| {{TICKER}} | Holding / Watchlist | {{LATEST_DATE}} | Above / Below | {{RSI_14}} | {{VOL_12M_OR_NA}} | {{DRAWDOWN}} | {{MAX_DD_12M_OR_NA}} | {{TECH_SCORE}} |

*Note: Report absent 12-month metrics as "not available" (never zero), and flag any asset-class-implausible risk value as a possible data anomaly.*

## 5. Correlation Watch

*Source: `getCorrelationMatrix` ({{START_DATE}} to {{END_DATE}})*

- **Highest co-movement pair:** {{PAIR_HIGH}} (`r = {{R_HIGH}}`)
- **Lowest co-movement pair:** {{PAIR_LOW}} (`r = {{R_LOW}}`)
- **Uncovered tickers (if any):** {{UNKNOWN_TICKERS_OR_NONE}}

## 6. Optional Quantitative Follow-Ups

- Run a detailed contribution drift scenario (`cashflow-rebalance-planner`).
- Run a multi-window correlation comparison (`multi-asset-correlation-xray`).
- Backtest a draft adjustment (`quant-strategy-backtest`).
- Screen regulated UCITS / PEA alternatives (`securities-screener-workflow`).
