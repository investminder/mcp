# Interpreting Multi-Asset Correlation Matrices

`getCorrelationMatrix` in [`investminder/mcp`](https://github.com/investminder/mcp) calculates the **Pearson correlation coefficient ($r$)** of **daily returns** between 2 and 20 securities over a specified `[startDate, endDate]` range.

## Correlation Threshold Bands

| Correlation Band ($r$) | Classification | Portfolio Risk Meaning |
|---|---|---|
| **`0.80` to `1.00`** | **Redundant / High Overlap** | Securities move largely in lockstep. Splitting capital across them creates an illusion of diversification without materially reducing drawdown risk. |
| **`0.50` to `0.79`** | **Moderate-to-High Co-Movement** | Shared macro or equity-beta driver (e.g., US equities vs. European equities). Some regional or sector dispersion, but joint drawdowns remain common. |
| **`0.20` to `0.49`** | **Moderate Diversification** | Meaningful independent return drivers; combining these assets typically lowers portfolio volatility relative to holding either alone. |
| **`-0.19` to `0.19`** | **Low / Uncorrelated** | Daily returns show little linear relationship over the sampled period (often seen between broad equities and physical gold or money-market funds). |
| **`-1.00` to `-0.20`** | **Inverse / Defensive Offset** | Assets tended to move in opposite directions during the sampled window (e.g., long-duration sovereign bonds vs. equities during deflationary shocks). |

## Four Critical Caveats for Retail Investors

1. **Correlations Are Regime-Dependent**
   - Stock-bond correlation was negative for much of 2000–2021, then turned sharply positive during the 2022 inflation and interest-rate shock.
   - Always test both a **long multi-year window** (5–10 years) and a **recent or stress window** (e.g., 12 months or calendar year 2022) when evaluating defensive assets.
2. **Daily Returns vs. Time-Zone Asynchrony**
   - Comparing a US-listed ETF (`SPY`, New York close) with a European-listed ETF (`VWCE.DE`, Xetra close) on daily returns can slightly understate true economic correlation because markets close at different hours.
   - When comparing identical exposures across US and EU exchanges, note the time-zone lag explicitly.
3. **Linear Relationship Only**
   - Pearson correlation captures linear co-movement, not tail-risk asymmetry or non-linear crash behavior. Combine correlation analysis with `analyzeSecurities` (`maxDrawdown12m`, `volatility12m`) and `startBacktest` / `listBacktests` to see actual drawdown behavior.
4. **Sample Length Matters**
   - Short windows (< 6 months) produce noisy correlations. Prefer at least 3–5 years when quote history (`earliestDate`) permits.
