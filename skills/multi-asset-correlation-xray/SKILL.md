---
name: multi-asset-correlation-xray
description: Expose hidden concentration and redundant factor overlap across ETFs, stocks, bonds, and commodities using Investminder MCP's daily-return Pearson correlation matrix (getCorrelationMatrix), security resolution (searchSecurities), and regime volatility metrics (analyzeSecurities). Use when a user asks how diversified their portfolio is, wants to compare correlations across 2 to 20 tickers, or wants to test whether adding a new asset actually diversifies their holdings.
license: MIT
compatibility: Requires the Investminder remote MCP server (https://api.investminder.com/mcp) with OAuth sign-in. Works immediately without an Investminder profile for market data tools.
metadata:
  author: Investminder
  mcp_repo: https://github.com/investminder/mcp
---

# Multi-Asset Correlation X-Ray

Measure true diversification across 2 to 20 securities using deterministic daily-return Pearson correlations from [`investminder/mcp`](https://github.com/investminder/mcp).

## When to Use This Skill

- The user provides a list of 2–20 stocks, ETFs, or forex pairs (or references an Investminder portfolio via `listPortfolios`) and asks whether they are genuinely diversified.
- The user wants to check if adding a candidate security (e.g., gold, aggregate bonds, or a regional equity ETF) lowers portfolio co-movement.
- The user wants to compare full-cycle correlation (e.g., 5–10 years) against a stress window (e.g., 2020 COVID shock or 2022 rate-hike drawdown).

## Reference Files

- Quantitative thresholds, regime shift notes, and cluster interpretation: [references/correlation-interpretation.md](references/correlation-interpretation.md)

## Workflow

### Step 1: Collect & Resolve Tickers (2 to 20)

1. Gather the tickers from the user's prompt, local CSV/XLSX, or `listPortfolios` (`includePositions: true`).
2. If any input is a company/fund name, ISIN, or ambiguous ticker, call `searchSecurities` to resolve the canonical Investminder ticker (e.g., `VWCE.DE`, `EUNA.DE`, `IGLN.L`, `SPY`, `QQQ`, `TLT`, `GLD`).
3. Respect `getCorrelationMatrix` limits: **minimum 2, maximum 20 tickers**. If the user provides more than 20 holdings, select the top 20 by portfolio weight (and state which smaller positions were excluded).

### Step 2: Check Data Overlap & Date Windows

1. If the user does not specify a date range, default to a **5-year window** (`startDate` = 5 years ago, `endDate` = today) and optionally run a **second regime window** (e.g., 1-year recent window or a historical stress year such as `2022-01-01` to `2022-12-31`) to illustrate how correlations shift under stress.
2. When inception dates are uncertain (common for newer UCITS ETFs), call `analyzeSecurities` with `fields: ["PERFORMANCE"]` to check `earliestDate` and `latestDate`, plus `volatility12m` and `maxDrawdown12m` for context.
   - If `volatility12m` or `maxDrawdown12m` is absent (under 12 months of history or fewer than 200 returns), report it as **"not available"** — never zero or interpreted.
   - If a risk or drawdown figure appears implausible for the asset class (for example, a drawdown beyond `-50%` on an investment-grade bond ETF), flag it as a **possible data anomaly** rather than commenting on it as a market fact.

### Step 3: Compute the Correlation Matrix

1. Call `getCorrelationMatrix` with:
   - `tickers`: list of 2–20 canonical tickers
   - `startDate`: `YYYY-MM-DD`
   - `endDate`: `YYYY-MM-DD`
2. Inspect `unknownTickers` in the response:
   - If any tickers are uncovered, report them explicitly to the user and offer to resolve equivalents with `searchSecurities` or `screenSecurities`.
   - Never silently swap or invent correlation values.

### Step 4: Diagnose Clusters, Redundancy & Diversifiers

Apply the thresholds in [references/correlation-interpretation.md](references/correlation-interpretation.md) strictly to the returned matrix:

1. **Redundant / Highly Correlated Pairs (`r >= 0.80`):** Flag pairs that move nearly in lockstep (e.g., `SPY` vs. `IWDA.AS` or overlapping US tech ETFs) and note that holding both adds minimal diversification.
2. **Moderate Co-Movement (`0.40 <= r < 0.80`):** Note partial diversification with shared macro sensitivity.
3. **Low / Uncorrelated Diversifiers (`-0.20 < r < 0.40`):** Highlight assets that dampen portfolio co-movement.
4. **Negative Correlation / Potential Hedges (`r <= -0.20`):** Highlight historically inverse pairs, while noting that equity-bond correlations can flip positive during inflation shocks (as in 2022).
5. **Candidate Diversifier Screening (Optional):** If the user asks what asset classes or regulated ETFs could broaden their universe, use `screenSecurities` (e.g., `assetClass: "ETF"`, `regulatoryFramework: "UCITS"`, `category` for bonds/commodities) and re-run `getCorrelationMatrix` with the candidate ticker(s).

## Output Format

1. **Analysis Window & Coverage Summary** (`startDate` to `endDate`, covered tickers, any `unknownTickers`).
2. **Pearson Correlation Matrix Table** (exact numbers from `getCorrelationMatrix`).
3. **Concentration & Redundancy Diagnosis** (top correlated clusters `>= 0.80` and lowest-correlated pairs `<= 0.30`).
4. **Regime Stability Note** (comparison across windows if two periods were run, plus explicit reminder that historical correlations are not static).

## Guardrails

- **Quantitative decision support only:** Never advise the user to sell overlapping holdings or buy a specific diversifier. Present objective co-movement data and trade-offs only.
- **Zero mental math:** Never guess, approximate, or extrapolate correlation coefficients. Every correlation value must come verbatim from `getCorrelationMatrix`.
- **Transparent coverage handling:** Always disclose `unknownTickers` and never fabricate correlations for uncovered securities.
- **Correlation is not causation or permanence:** Always state that Pearson correlation measures linear daily-return co-movement over the selected historical period and can spike toward `1.0` during systemic market stress.
