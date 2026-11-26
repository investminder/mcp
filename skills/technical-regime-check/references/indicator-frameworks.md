# Objective Technical Indicator Frameworks

Use this reference to classify `analyzeSecurities` (`TECHNICAL_INDICATORS`, `PERFORMANCE`, `VOLUME_PROFILE`) outputs neutrally and consistently without advisory language.

## Reading `analyzeSecurities` Technical Responses

- `technicalIndicators` is a **daily array** covering `[startDate, endDate]`; read the **last entry** for current values. Request a short window (a few weeks) when only current values are needed.
- `technicalIndicators` keys are lowercase/camelCase: `date`, `atr`, `drawdown`, `ema20`, `ema50`, `ema100`, `ema200`, `sma20`, `sma50`, `sma100`, `sma200`, `macd`, `macdSignal`, `rsi14`, `rsi21`, `momentum_1_3_6`, `momentum_3_6_12`.
- There is no price column inside `technicalIndicators` — use `performance.price` (from `PERFORMANCE`) as the latest price in the security's quote currency.
- **Strategy-engine mapping (`createStrategy`):** `ema20` ↔ `EMA_20`, `ema50` ↔ `EMA_50`, `sma100` ↔ `SMA_100`, `sma200` ↔ `SMA_200`, `rsi14` ↔ `RSI_14`, `rsi21` ↔ `RSI_21`, `macd` ↔ `MACD`, `macdSignal` ↔ `MACD_SIGNAL`, `atr` ↔ `ATR`, `drawdown` ↔ `DRAWDOWN`, `performance.price` ↔ `PRICE`.

## 1. Trend Structure (Moving Averages)

Compare `performance.price` against the last entry of `technicalIndicators`:

| Observation | Objective Regime Label |
|---|---|
| `performance.price` `> sma200` and `ema50 > sma200` | **Primary Uptrend** |
| `performance.price` `> sma200` but `ema20 < ema50` | **Primary Uptrend — Short-Term Pullback / Consolidation** |
| `performance.price` `< sma200` and `ema50 < sma200` | **Primary Downtrend** |
| `performance.price` `< sma200` but `ema20 > ema50` | **Primary Downtrend — Counter-Trend Bounce** |
| `performance.price` oscillating closely around `sma200` / flat `sma100` | **Range-Bound / Transition Regime** |

## 2. Momentum Oscillators (`rsi14`, `rsi21`, `macd`, `macdSignal`)

| Indicator Reading | Objective Classification |
|---|---|
| `rsi14 >= 70` | **Stretched / Overbought Momentum** (can persist in strong trends) |
| `50 < rsi14 < 70` | **Constructive / Positive Momentum** |
| `30 < rsi14 <= 50` | **Soft / Negative Momentum** |
| `rsi14 <= 30` | **Compressed / Oversold Momentum** (can persist in downtrends) |
| `macd > macdSignal` | **Positive Short-Term Momentum Spread** |
| `macd < macdSignal` | **Negative Short-Term Momentum Spread** |

## 3. Volatility, Drawdown & Technical Score (`PERFORMANCE` + `TECHNICAL_INDICATORS`)

- **`atr` (Average True Range):** Typical daily price range in the security's quote currency (last entry of `technicalIndicators`). If showing `atr / performance.price`, show the exact arithmetic using returned values.
- **`volatility12m` & `maxDrawdown12m`:** Trailing 12-month annualized volatility and worst peak-to-trough loss (in `performance`). Absent when the security has under 12 months of history or fewer than 200 returns — report as **"not available"**, never zero.
- **`drawdown`:** Current gap to all-time highest close (negative). If a drawdown or volatility figure looks implausible for the asset class (e.g., a drawdown beyond `-50%` on an investment-grade bond ETF), flag it as a possible data anomaly rather than interpreting it as a market fact.
- **`scoreTechnical.global.score` (0–10):** Overall technical score inside the `scoreTechnical` object (which also holds component sub-scores such as history, volume, RSI, moving averages, momentum, and drawdown).

## 4. Volume Profile (`VOLUME_PROFILE`)

- Summarizes historical traded volume distributed across price bins over `[startDate, endDate]`.
- High-volume price zones indicate where substantial historical trading occurred (liquidity concentration); low-volume gaps indicate price zones where price moved quickly with lighter volume.
- Present these strictly as **historical volume distribution facts**, never as guaranteed support or resistance floors.
