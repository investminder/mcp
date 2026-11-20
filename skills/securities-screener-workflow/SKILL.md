---
name: securities-screener-workflow
description: Orchestrate Investminder MCP's structured screening engine (screenSecurities, listScreeners, searchSecurities, analyzeSecurities) across US and European equities and ETFs (S&P 500, Nasdaq-100, Russell 2000, MSCI World, STOXX Europe 600, Euro Stoxx 50, CAC 40, DAX, FTSE 100, SMI, IBEX 35, AEX, Nikkei 225) with UCITS and French PEA eligibility filters, valuation, quality, growth, and momentum criteria. Use when a user asks to screen stocks or ETFs, replay a saved screener or preset, or narrow a large market universe into a disciplined shortlist.
license: MIT
compatibility: Requires the Investminder remote MCP server (https://api.investminder.com/mcp) with OAuth sign-in. Works immediately without an Investminder profile for screenSecurities, searchSecurities, and preset listScreeners.
metadata:
  author: Investminder
  mcp_repo: https://github.com/investminder/mcp
---

# US & European Securities Screener Workflow

Translate plain-English equity and ETF screening ideas into exact, schema-valid `screenSecurities` calls on [`investminder/mcp`](https://github.com/investminder/mcp), iteratively refine loose universes, and verify top candidates with `analyzeSecurities`.

## When to Use This Skill

- The user wants to screen US or European stocks on fundamentals, quality, valuation, growth, dividends, or momentum (e.g., S&P 500 quality compounders, STOXX Europe 600 dividend payers, Nasdaq-100 low-debt growth).
- The user wants to find low-cost `UCITS` or French `PEA`-eligible ETFs matching specific asset categories, distribution policies, or fee ceilings.
- The user wants to inspect or replay their saved screeners or Investminder presets via `listScreeners`.

## Reference Files

- Complete verified camelCase field names, operators, units, and `sortBy` enums: [references/screening-criteria-guide.md](references/screening-criteria-guide.md)

## Workflow

### Step 1: Check Presets or Saved Screeners (When Relevant)

If the user asks for ready-made screens or their own saved filters:
1. Call `listScreeners` (`type: "USER"` for saved screeners, `type: "PRESET"` for Investminder presets, or omit `type` for both; pass `language`: `en`, `fr`, `es`, `de`).
2. To replay a saved screener or preset in `screenSecurities`, preserve each `field`, keep `values`/`min`/`max` as-is, convert `comparator` to `operator` with typed numeric values, and pass `sort.sortBy` / `sort.sortOrder` directly.

### Step 2: Translate Intent into Exact `screenSecurities` Criteria

Follow the exact JSON schema from [references/screening-criteria-guide.md](references/screening-criteria-guide.md):

1. Every criterion is a JSON object with a camelCase `field` (each field used **at most once** — all criteria combine with `AND`).
2. Use one of three valid shapes per criterion:
   - `operator` + `value` (`EQUALS` for categorical fields; `HIGHER_THAN`, `LOWER_THAN`, `HIGHER_THAN_OR_EQUALS`, `LOWER_THAN_OR_EQUALS`, `EQUALS`, `NOT_EQUAL` for numeric fields — never LT/GT). Note: `assetClass`, `distributionPolicy`, and `distributionFrequency` accept only `operator: "EQUALS"` + `value` (not `values`).
   - `values`: list of accepted values for multi-value categorical fields (`sector`, `industry`, `country`, `currency`, `category`, `location`, `provider`, `regulatoryFramework`, `stockIndex`).
   - `min` and/or `max`: strict numeric interval bounds.
3. Respect exact units:
   - Percentages use **`15` for `15%`**, not `0.15` (e.g., `roe`, `roic`, `grossMargin`, `dividendYield`, `netExpenseRatio`, `perfTwelveMonth`).
   - `marketCap` and `totalAssets` are in **USD dollars** (not millions).
   - `country` uses **ISO 3166-1 alpha-3** (`USA`, `FRA`, `DEU`, `GBR`, `CHE`, `NLD`, `ESP`).
   - `maxDrawdown12m` is **negative** (`-20` for a 20% loss; a drawdown smaller than 20% is `HIGHER_THAN -20`).
   - `sortBy` uses **UPPER_SNAKE_CASE** (e.g., `MOMENTUM_3_6_12`, `PERF_TWELVE_MONTH`, `MARKET_CAP`, `MAX_DRAWDOWN_12M`), unlike camelCase criterion fields.
   - Do **not** sort or filter ETFs on `scoreFinancial` / `SCORE_FINANCIAL` (for funds, it rests on dividend yield alone).

### Step 3: Execute & Iteratively Tighten Loose Filters

1. Call `screenSecurities` with `criteria`, `sortBy`, `sortOrder`, `size` (default 10, max 50), `fields: ["PERFORMANCE"]` (add `"DESCRIPTION"` only on small final shortlists to keep payloads clean), and `language`.
2. Inspect `total` vs. `size`:
   - If `total` is far above `size` (e.g., 120 matches), report `total` and propose tightening 1–2 criteria (e.g., adding a quality, fee, or drawdown bound) rather than paging endlessly.
   - If `total == 0` or `total` looks unexpectedly small when filtering on `volatility12m` or `maxDrawdown12m`, note explicitly that `screenSecurities` excludes securities with less than 12 months of history (or fewer than 200 returns) because those risk fields are absent. Show which constraint was tightest so the user can relax it.
3. **Missing or implausible risk values:**
   - Report any absent `volatility12m` or `maxDrawdown12m` as **"not available"** — never zero or interpreted.
   - If a returned `volatility12m`, `maxDrawdown12m`, or `drawdown` value appears implausible for the asset class (for example, a drawdown beyond `-50%` on an investment-grade bond ETF), flag it as a **possible data anomaly** without commenting on it as a market fact.

### Step 4: Deep-Dive Top Candidates (Optional)

For 2–5 shortlisted tickers the user wants to inspect further:
- Call `analyzeSecurities` with `fields: ["PERFORMANCE", "TECHNICAL_INDICATORS"]` (and `"FINANCIAL_STATEMENTS"`, `"DIVIDENDS"`, `"PER"` if the user has an Investminder profile and wants fundamental history).
- Optionally run `getCorrelationMatrix` on the shortlist to check whether the top candidates are distinct or redundant.

## Output Format

1. **Applied Screening Criteria & Universe Count** (exact criteria sent, `sortBy`/`sortOrder`, `total` matches).
2. **Shortlist Comparison Table** (Ticker, Name, Exchange/Currency, Key Screened Metrics, `marketCapUsd` when comparing across currencies, and Data As-Of Date where analyzed).
3. **Refinement Options** (how to tighten if `total` is large, or relax if `total == 0`).

## Guardrails

- **Quantitative decision support only:** A screener shortlist is a factual filter output, never a list of buy recommendations. Never rank a security as a "top pick to buy" or provide price targets.
- **Zero mental math:** Report only values returned by `screenSecurities`, `searchSecurities`, and `analyzeSecurities`. Distinguish missing fields from zero values.
- **No fabricated matches:** If `screenSecurities` returns `total: 0`, state clearly that no covered securities met the filters; never invent tickers or adjust criteria silently without telling the user.
- **Currency & ETF score hygiene:** Always compare market caps on `marketCapUsd`, note `GBX` (pence) vs. `GBP`, and never evaluate ETFs on `scoreFinancial`.
