# Investminder `screenSecurities` Criteria & Field Reference

Grounded directly in the [`investminder/mcp`](https://github.com/investminder/mcp) schema. All criteria in `screenSecurities` combine with **AND**, and each `field` may appear **at most once**.

## Criterion Shapes

1. **Single comparison:** `{"field": "roe", "operator": "HIGHER_THAN", "value": 15}`
2. **Multi-value list (any matches):** `{"field": "sector", "values": ["technology", "healthcare"]}`
3. **Numeric interval (strict bounds):** `{"field": "per", "min": 8, "max": 20}`

**Numeric operators:** `HIGHER_THAN`, `LOWER_THAN`, `HIGHER_THAN_OR_EQUALS`, `LOWER_THAN_OR_EQUALS`, `EQUALS`, `NOT_EQUAL` *(never LT or GT)*.  
**Categorical operator:** `EQUALS` *(or `values` array on multi-value fields; `assetClass`, `distributionPolicy`, and `distributionFrequency` accept only `operator: "EQUALS"` + `value`)*.

## Verified Criterion Fields (camelCase)

| Group | Exact `field` Names | Unit / Value Format |
|---|---|---|
| **Classification** | `assetClass`, `category`, `country`, `location`, `sector`, `industry`, `stockIndex`, `currency`, `provider` | `assetClass` (`EQUALS` + `value` only): `ETF`, `STOCK`, `FOREX`. `category`: `BOND`, `COMMODITY`, `CRYPTO`, `CURRENCY`, `STOCK`. `location`: `NORTH_AMERICA`, `LATIN_AMERICA`, `EUROPE`, `ASIA`, `WORLD`. `currency`: `USD`, `EUR`, `GBP`, `GBX` (British pence), `CHF`. `country`: ISO alpha-3 (`USA`, `FRA`, `DEU`, `GBR`, `CHE`, `NLD`, `ESP`). `sector`: `basic-materials`, `communication-services`, `consumer-cyclical`, `consumer-defensive`, `consumer-goods`, `energy`, `financial-services`, `healthcare`, `industrials`, `real-estate`, `technology`, `utilities`. |
| **Funds & ETFs** | `regulatoryFramework`, `distributionPolicy`, `distributionFrequency`, `netExpenseRatio`, `totalAssets`, `holdingsCount` | `regulatoryFramework`: `UCITS` (EU), `PEA` (France). `distributionPolicy` (`EQUALS` + `value` only): `ACCUMULATING`, `DISTRIBUTING`. `distributionFrequency`: `EQUALS` + `value` only. `netExpenseRatio`: percent (`0.2` = 0.2%). `totalAssets`: USD dollars. `holdingsCount`: integer. |
| **Valuation** | `per`, `peg`, `pbr`, `marketCap`, `dividendYield`, `dividendPayoutRatio` | `per`, `peg`, `pbr`: decimal ratio. `marketCap`: USD dollars (not millions). `dividendYield`, `dividendPayoutRatio`: percent (`4` = 4%). |
| **Quality & Balance Sheet** | `roe`, `roic`, `grossMargin`, `operatingMargin`, `netMargin`, `currentRatio`, `debtEquityRatio` | Margins, `roe`, `roic`: percent (`20` = 20%). `currentRatio`, `debtEquityRatio`: decimal ratio (`0.5` = 0.5x). |
| **Growth (Annual)** | `annualGrowthTotalRevenue`, `annualGrowthNetProfit`, `annualGrowthEps`, `annualGrowthFreeCashFlow`, `annualGrowthSharesNumber` | Percent (`10` = 10% YoY). |
| **Momentum, Risk & Technicals** | `perfOneMonth`, `perfThreeMonth`, `perfSixMonth`, `perfTwelveMonth`, `perfTwentyFourMonth`, `perfThirtySixMonth`, `momentum_1_3_6`, `momentum_3_6_12`, `rsi14`, `rsi21`, `volatility12m`, `maxDrawdown12m` | Percent (`15` = 15%). **`maxDrawdown12m` is negative** (`-20` = -20% loss; a smaller loss than 20% is `HIGHER_THAN -20`). |
| **Scores** | `scoreFinancial`, `scoreTechnical` | `0` to `10`. Do not use `scoreFinancial` for ETFs. |

## Sorting (`sortBy` & `sortOrder`)

- **Complete list of valid `sortBy` values (UPPER_SNAKE_CASE):** `ID`, `TICKER`, `NAME`, `PERF_ONE_MONTH`, `PERF_THREE_MONTH`, `PERF_SIX_MONTH`, `PERF_TWELVE_MONTH`, `PERF_TWENTY_FOUR_MONTH`, `PERF_THIRTY_SIX_MONTH`, `MOMENTUM_1_3_6`, `MOMENTUM_3_6_12`, `MARKET_CAP`, `TOTAL_ASSETS`, `PEG`, `NET_MARGIN`, `DIVIDEND_YIELD`, `RSI_14`, `RSI_21`, `SCORE_FINANCIAL`, `SCORE_TECHNICAL`, `VOLATILITY_12M`, `MAX_DRAWDOWN_12M`.
- `sortOrder`: `ASC` (default) or `DESC`.
- Note: `MAX_DRAWDOWN_12M` values are negative, so `DESC` puts the **smallest** drawdowns first (e.g., `-5%` before `-40%`). Securities without a value for `sortBy` appear last in both orders.

## Covered Stock Indices (`stockIndex` Values)

`SP_500`, `CAC_40`, `DAX`, `FTSE_100`, `NASDAQ_100`, `NIKKEI_225`, `RUSSELL_2000`, `MSCI_WORLD`, `STOXX_EUROPE_600`, `EURO_STOXX_50`, `IBEX_35`, `AEX`, `SMI`.
