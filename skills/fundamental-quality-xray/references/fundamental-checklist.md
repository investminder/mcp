# Fundamental Quality & Valuation Checklist

Use this framework to interpret `analyzeSecurities` (`FINANCIAL_STATEMENTS`, `DIVIDENDS`, `PER`, `PERFORMANCE`) objectively without advisory language.

## 1. Growth & Earnings Quality
- **Revenue & Profit Consistency:** Distinguish steady multi-year compounding from cyclical spikes or one-off gains.
- **Free Cash Flow (FCF) Conversion:** Compare net income with free cash flow over multiple years; persistent divergence can signal heavy capex or working-capital strain.
- **Share Count (`annualGrowthSharesNumber`):** Negative share growth indicates net buybacks; persistent positive growth indicates shareholder dilution.

## 2. Profitability & Capital Efficiency
- **Margins (`grossMargin`, `operatingMargin`, `netMargin`):** Track whether margins are expanding, stable, or compressing across the available periods.
- **Returns on Capital (`roe`, `roic`):** Compare `roe` alongside `debtEquityRatio` — high `roe` paired with high leverage carries different balance-sheet risk than high `roic` with low leverage.

## 3. Balance-Sheet & Liquidity
- **`debtEquityRatio`:** Decimal ratio (`0.5` = 0.5x). Note that financials, utilities, and REITs structurally operate with higher leverage than asset-light software firms.
- **`currentRatio`:** Short-term assets divided by short-term liabilities; values below `1.0` warrant noting liquidity structure (though subscription/retail models with negative working capital can operate normally below `1.0`).

## 4. Dividend Sustainability (`DIVIDENDS`)
- **Continuity:** Note consecutive years of payments, freezes, or cuts present in the returned `DIVIDENDS` series.
- **Payout Coverage:** Present `dividendPayoutRatio` and `dividendYield` alongside FCF trends; unusually high yields combined with elevated payout ratios often reflect market skepticism rather than guaranteed income.

## 5. Historical P/E Context (`PER`)
- Summarize the **minimum, maximum, and latest** `PER` observed in the returned history (only from actual returned points).
- Note that negative or near-zero earnings distort P/E ratios; flag loss-making periods explicitly rather than treating missing P/E values as zero.
- Reminder: `scoreFinancial` is an object containing component sub-scores; its overall 0–10 rating is `scoreFinancial.global.score`. It is meaningful for **stocks only** — for ETFs, all financial sub-scores are `null` except `shareholderReturn`.
