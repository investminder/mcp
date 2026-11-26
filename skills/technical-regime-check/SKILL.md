---
name: technical-regime-check
description: Perform an objective technical trend, momentum, volatility, drawdown, and volume-profile regime check on one or more stocks or ETFs using Investminder MCP's analyzeSecurities and searchSecurities tools. Use when a user asks about a ticker's technical indicators (RSI, SMA/EMA moving averages, MACD, ATR), current drawdown from highs, 12-month volatility, or trend regime before evaluating a rules-based strategy.
license: MIT
compatibility: Requires the Investminder remote MCP server (https://api.investminder.com/mcp) with OAuth sign-in. Works immediately without an Investminder profile for QUOTES, PERFORMANCE, TECHNICAL_INDICATORS, and VOLUME_PROFILE.
metadata:
  author: Investminder
  mcp_repo: https://github.com/investminder/mcp
---

# Objective Technical Regime Check

Diagnose trend structure, momentum, volatility, drawdown, and volume distribution for any covered US or European security using deterministic outputs from [`investminder/mcp`](https://github.com/investminder/mcp).

## When to Use This Skill

- The user asks for a technical check-up on one or more stocks or ETFs (e.g., *"Where do ASML.AS's RSI 14, MACD, and 200-day moving average stand today?"*).
- The user wants to classify whether an index or ETF is currently in an uptrend, consolidation, or drawdown regime without subjective chart guessing.
- The user wants to verify technical indicator levels before encoding a `PROGRESSIVE` strategy trigger in `createStrategy`.

## Reference Files

- Indicator regime definitions, response keys, and strategy-engine mapping: [references/indicator-frameworks.md](references/indicator-frameworks.md)

## Workflow

### Step 1: Resolve Canonical Ticker(s)

1. If the user provides a company/ETF name, ISIN, or exchange-ambiguous ticker (e.g., `ASML` vs. `ASML.AS`, `Nestlé` → `NESN.SW`), call `searchSecurities` first to obtain the exact canonical Investminder ticker.
2. If analyzing multiple tickers (e.g., a watchlist of 3–8 assets), process each ticker explicitly and never extrapolate one listing's technicals to another exchange listing.

### Step 2: Fetch Deterministic Technical & Risk Sections (`analyzeSecurities`)

Call `analyzeSecurities` for each resolved `ticker` with:
- `fields`: `["PERFORMANCE", "TECHNICAL_INDICATORS"]` (add `"QUOTES"` with `quoteFrequency: "DAILY"` or `"WEEKLY"` if price trajectory context is needed, and `"VOLUME_PROFILE"` if the user asks for high-volume price nodes).
- `startDate` / `endDate`: `technicalIndicators` returns a **daily array** over `[startDate, endDate]` where the current reading is the **last entry**. Pass a **short window (a few weeks)** when only current indicator values are needed; use a longer window only when inspecting historical indicator series or `VOLUME_PROFILE`.
- `language`: `en`, `fr`, `es`, or `de`.

**Unknown ticker handling:** If `analyzeSecurities` returns `found: false`, stop immediately for that ticker — it is not an analysis. Report the ticker as uncovered and use `searchSecurities` or `screenSecurities` to find an equivalent only if the user wants one.

### Step 3: Classify the Technical Regime Objectively

Using [references/indicator-frameworks.md](references/indicator-frameworks.md) and **only** the returned tool data, summarize five dimensions:

1. **Data Freshness:** Report `earliestDate` and `latestDate` (the as-of quote date).
2. **Trend Structure:** `technicalIndicators` has no price column — compare `performance.price` against the last entry's `ema20`, `ema50`, `ema100`, `ema200`, `sma20`, `sma50`, `sma100`, and `sma200`.
3. **Momentum State:** Report the last entry's `rsi14` / `rsi21`, `macd` vs. `macdSignal`, and `performance` returns (`perfOneMonth`, `perfThreeMonth`, `perfSixMonth`, `perfTwelveMonth`, `momentum_1_3_6`, `momentum_3_6_12`).
4. **Volatility, Drawdown & Technical Score:** Report the last entry's `atr`, plus `performance` fields `volatility12m`, `maxDrawdown12m`, current `drawdown`, and `scoreTechnical.global.score` (0–10; note that `scoreTechnical` is an object that also contains component sub-scores).
   - If `volatility12m` or `maxDrawdown12m` is absent (under 12 months of history or fewer than 200 returns), report it as **"not available"** — never treat it as zero or interpret it.
   - If a risk or drawdown value appears implausible for the asset class (for example, a drawdown beyond `-50%` on an investment-grade bond ETF), flag it to the user as a **possible data anomaly** rather than commenting on it as a market fact.
5. **Volume Profile (when requested):** Summarize high-volume price concentration zones from `VOLUME_PROFILE` as factual historical liquidity levels, not guaranteed support/resistance.

### Step 4: Bridge to Rules-Based Testing (Optional)

Response keys in `analyzeSecurities` map to strategy-engine triggers in `createStrategy` (`ema20` ↔ `EMA_20`, `ema50` ↔ `EMA_50`, `sma100` ↔ `SMA_100`, `sma200` ↔ `SMA_200`, `rsi14` ↔ `RSI_14`, `rsi21` ↔ `RSI_21`, `macd` ↔ `MACD`, `macdSignal` ↔ `MACD_SIGNAL`, `atr` ↔ `ATR`, `performance.price` ↔ `PRICE`). If the user asks whether a technical signal (such as `PRICE` crossing `SMA_200` or `RSI_14 < 35`) would have worked historically, hand off to `quant-strategy-backtest` (`createStrategy` + `startBacktest` + `listBacktests`) rather than speculating on signal efficacy.

## Output Format

1. **Security & As-Of Header** (Canonical Ticker, Currency, `performance.price`, `earliestDate` → `latestDate`).
2. **Technical Regime Summary Table** (Trend vs. `sma200`/`ema50`, `rsi14`, `macd` vs. `macdSignal`, `atr`, `volatility12m`, `drawdown`, `maxDrawdown12m`, `scoreTechnical.global.score`).
3. **Objective Regime Classification** (e.g., *Above `sma200` / Neutral `rsi14`*) with a plain-English summary of conflicting signals or flagged data anomalies if any.
4. **Next-Step Options** (e.g., compare against peers via `screenSecurities`, check co-movement via `getCorrelationMatrix`, or backtest a rule via `quant-strategy-backtest`).

## Guardrails

- **Quantitative decision support only:** Never translate an oversold `rsi14`, `macd` crossover, or moving-average break into a "buy", "sell", or "hold" call, and never issue price targets or stop-loss advice.
- **No fabricated market data:** Never invent or estimate indicator values from memory. Every indicator, drawdown, volatility, and score must come directly from `analyzeSecurities`; if a metric is absent, state `"not available"`.
- **Uncovered ticker integrity:** If `found: false` is returned, do not fabricate a regime check; report the gap clearly.
- **No predictive guarantees:** State clearly that technical indicators summarize historical price and volume data and do not predict future price movements.
