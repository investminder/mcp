# Investminder MCP tools reference

The [Investminder](https://www.investminder.com) MCP server exposes 21 tools. Your assistant picks them automatically; this page helps you know what to ask for and what to expect.

Back to the [README](../README.md).

- [Getting started](#getting-started)
- [Market data](#market-data)
- [Strategies](#strategies)
- [Backtests](#backtests)
- [Portfolios](#portfolios)

All tools that return text accept a `language` of `en`, `fr`, `es` or `de`. List tools return pages with `items`, `total`, `offset`, `size` (default 10, max 50) and `hasMore`.

---

## Getting started

### `startOnboarding`
Guided introduction to Investminder: presents the product and walks a new user through the first steps, adapted to what they have already done. Optional, works without an account.

> *"What can Investminder do for me?"*

### `upsertUser`
Creates or updates the Investminder profile of the signed-in identity: country (ISO 3166-1 alpha-2), currency you hold money in (`USD`, `EUR`, `GBP`, `CHF`), language and, optionally, the onboarding quiz answers (experience, management style, risk tolerance, wealth). Returns the pre-built strategies that fit the answers.

The currency is the one you hold money in, not the one you are billed in.

---

## Market data

### `searchSecurities`
Find stocks, ETFs and forex pairs by **name, ticker or ISIN**. Add `fields: ["DESCRIPTION"]` for the company or fund description, `["PERFORMANCE"]` for metrics and scores. Filter with `assetClass` (`STOCK`, `ETF`, `FOREX`).

> *"Find the iShares Core MSCI World ETF and its ISIN."*

### `screenSecurities`
Select securities on structured criteria combined with AND. Available fields include:

- **Classification**: asset class, category, country, location, sector, industry, stock index (S&P 500, Nasdaq-100, Russell 2000, MSCI World, STOXX Europe 600, Euro Stoxx 50, CAC 40, DAX, FTSE 100, IBEX 35, AEX, SMI, Nikkei 225), currency, provider
- **Funds**: regulatory framework (UCITS, PEA), distribution policy and frequency, net expense ratio, total assets, holdings count
- **Valuation**: P/E, PEG, P/B, market cap, dividend yield, payout ratio
- **Quality**: ROE, ROIC, gross / operating / net margin, current ratio, debt/equity
- **Growth**: annual growth of revenue, net profit, EPS, free cash flow, share count
- **Momentum and technicals**: performance over 1, 3, 6, 12, 24 and 36 months, composite momentum 1-3-6 and 3-6-12, RSI 14 and 21

Percentages are written as `15` for 15 %. A `total` far above `size` means the criteria are loose.

> *"Accumulating UCITS ETFs on world equities with fees below 0.2 %, sorted by 3-year performance."*

### `analyzeSecurities`
Detailed data for one ticker, section by section:

| Section | Content | Profile needed |
|---|---|---|
| `QUOTES` | Daily or weekly prices | No |
| `PERFORMANCE` | Returns and scores | No |
| `TECHNICAL_INDICATORS` | RSI, moving averages, MACD, ATR… | No |
| `VOLUME_PROFILE` | Volume distribution by price | No |
| `FINANCIAL_STATEMENTS` | Yearly or quarterly statements | Yes, depth depends on plan |
| `DIVIDENDS` | Dividend history | Yes, depth depends on plan |
| `PER` | P/E history | Yes, depth depends on plan |

Every response carries `earliestDate` and `latestDate`.

> *"Analyze ASML: 10 years of yearly financial statements, dividends and current technical indicators."*

### `getCorrelationMatrix`
Pearson correlation of daily returns between 2 and 20 tickers over a date range. Learn to read it: [Diversification & Correlation](https://help.investminder.com/en/investment-academy/diversification-correlation-1kcrnwe/).

### `listScreeners`
Your saved screeners and their criteria, ready to be replayed with `screenSecurities`.

---

## Strategies

An Investminder strategy is a set of rules: which assets, in what weights, when to buy, when to sell, where to park cash, with what fees and against which benchmark. Learn the method: [How to build a Strategy](https://help.investminder.com/en/how-to-use/how-to-build-a-strategy-ez04de/).

### `listPreBuiltStrategies`
The catalog of ready-made strategies available for your plan. Filter by `approach` (`TREND_FOLLOWING`, `BALANCED`, `DIVIDEND_FOCUSED`, `CORE_SATELLITE`, `MEAN_REVERSION`), `diversification`, `activity` (`PASSIVE_INVESTOR`, `ACTIVE_INVESTOR`). Read one strategy alone to get its full definition.

### `createStrategy`
Creates a strategy in **DRAFT**. Two execution models:

- **REBALANCED** — fixed target weights summing to 100 %, periodically rebalanced. Requires asset-class constraints.
- **PROGRESSIVE** — exposure built on signals, each asset capped by a maximum weight or share count.

Buy and sell rules combine triggers on indicators — `RSI_14`, `RSI_21`, `DRAWDOWN`, `MOMENTUM_1_3_6`, `MOMENTUM_3_6_12`, `EMA_20`, `EMA_50`, `SMA_100`, `SMA_200`, `MACD`, `MACD_SIGNAL`, `ATR`, `PRICE`, `ALLOCATION_GAP`, `MONTH_INDEX` — with comparators such as `CROSSING_UP`, `LOWER_THAN` or `MODULO` (periodic triggers), and optional DCA or value averaging. Constraints can restrict to UCITS or PEA-eligible funds.

To start from a pre-built strategy, read it and pass its definition back, adjusted or not.

### `updateStrategy`
Replaces the draft definition (send the complete definition every time).

### `listUserStrategies`
Your strategies, with their editable draft.

### `deleteStrategy`
Deletes a draft and its backtests; deletes the strategy if the draft was its only version.

---

## Backtests

### `startBacktest`
Runs a backtest of a strategy draft over a date range, with:

- **Inflows**: initial amount plus a regular amount (daily to yearly)
- **Outflows** (optional): fixed amount or percentage withdrawn after a delay in years — useful to test a retirement drawdown plan

Backtests are asynchronous: the tool returns a `PENDING` backtest.

### `listBacktests`
Polls a backtest by `backtestId` until `COMPLETED` or `FAILED`, and returns its performance metrics and annual returns, for the strategy and its benchmark. Ask for `HOLDINGS`, `TRANSACTIONS` or `DIVIDENDS` only when you need the daily series.

> *"Backtest my strategy from 2010 with $10,000 and $500 a month, then compare its max drawdown with SPY."*

---

## Portfolios

### `createPortfolio`
Creates an empty manual portfolio in `USD`, `EUR`, `GBP` or `CHF`.

### `addPortfolioCash` / `addPortfolioPosition`
Record deposits, withdrawals, buys and sells. Each call adds an operation — it does not replace a balance — so ask the assistant to check the result rather than retry.

### `listPortfolios`
All your portfolios, with positions and cash balances on request.

### `listPortfolioTransactions`
Transaction history, newest first, filterable by type and date.

### `listInstitutions` / `connectPortfolio`
List supported brokers and banks, then get a **hosted authorization link** to connect one. You authorize directly with the provider; the portfolio is then created and synchronized automatically. Never type banking credentials in a chat.

Learn more: [The Portfolio: the central element of your investment management](https://help.investminder.com/en/how-to-use/the-portfolio-the-central-element-of-your-investment-management-13844s4/).
