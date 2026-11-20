# Broker CSV & Excel Column Schemas

Use this mapping when parsing `.csv` or `.xlsx` exports during `excel-to-quant-audit`. Remind the user that when an AI assistant reads a file, its contents are sent to the AI assistant provider — recommend removing account numbers, holder names, IBANs, tax IDs, and addresses **before** sharing the file. Omit any remaining personal identifiers from all Investminder MCP tool calls and summaries.

## Major Retail Broker Export Mappings

| Broker | Primary Identifier Column(s) | Quantity Column | Value / Price Columns | Currency Column | Notes & Quirks |
|---|---|---|---|---|---|
| **Interactive Brokers (IBKR)** | `Symbol`, `ISIN` (in Flex Query / Open Positions) | `Quantity` | `MarkPrice`, `PositionValue`, `CostBasisPrice` | `CurrencyPrimary` | Multi-section CSVs include header rows (`Open Positions,Header,...`). Filter rows where `DataDiscriminator == Summary` or `Open Positions,Data`. |
| **DEGIRO** | `ISIN`, `Product` | `Amount` (or `Aantal` / `Quantité`) | `Closing` (price), `Local value`, `Value in EUR` | `Local value` (adjacent unnamed currency column) | European decimal comma (`1.234,56`) is common in FR/DE/NL exports. Prefer `ISIN` with `searchSecurities`. |
| **Trade Republic** | `ISIN`, `Name` / `Title` | `Shares` / `Quantity` | `Price`, `Value` / `Amount` | `Currency` (usually `EUR`) | Often exported via PDF-to-CSV tools or community scripts; `ISIN` is the most reliable key for Xetra/Lang & Schwarz UCITS ETFs. |
| **BoursoBank (Boursorama)** | `Code ISIN`, `Libellé`, `Mnémo` | `Quantité` | `Cours`, `Valorisation`, `PRU` | `Devise` (usually `EUR`) | French PEA and CTO exports use semicolons (`;`) and decimal commas. Check PEA eligibility via `screenSecurities` (`regulatoryFramework: "PEA"`). |
| **Saxo Bank** | `Instrument`, `Symbol`, `ISIN` | `Amount` / `Quantity` | `Current Price`, `Market Value`, `Open Price` | `Currency` | Symbols use exchange suffixes like `:xpar`, `:xetr`, `:xlon` — resolve via `ISIN` or strip Saxo suffix before calling `searchSecurities`. |
| **Trading 212** | `ISIN`, `Ticker`, `Name` | `No. of shares` | `Price / share`, `Total` | `Currency (Price / share)` | Fractional shares are common; UK stocks may be quoted in `GBX` (pence) while account currency is `GBP` or `EUR`. |
| **Custom Excel / Google Sheets** | `Ticker`, `Symbol`, `ISIN`, `Name`, `Asset` | `Shares`, `Qty`, `Units` | `Weight`, `Allocation %`, `Market Value`, `Avg Price` | `Currency`, `CCY` | Check whether weights are stored as decimals (`0.25`) or percentages (`25` or `25%`). Normalize carefully and confirm sum = `100%`. |

## Exchange Suffix Reference (Investminder Canonical Format)

When `ISIN` is unavailable, map local listings to canonical exchange suffixes via `searchSecurities`:

| Exchange | Country | Typical Suffix | Example |
|---|---|---|---|
| Nasdaq / NYSE | United States | *(none)* | `SPY`, `QQQ`, `MSFT`, `AAPL` |
| Xetra (Frankfurt) | Germany | `.DE` | `VWCE.DE`, `EUNA.DE`, `SXRW.DE` |
| Euronext Paris | France | `.PA` | `CW8.PA`, `MC.PA`, `AIR.PA` |
| Euronext Amsterdam | Netherlands | `.AS` | `IWDA.AS`, `ASML.AS` |
| London Stock Exchange | United Kingdom | `.L` | `IGLN.L`, `ULVR.L` *(watch `GBX` pence quotes)* |
| SIX Swiss Exchange | Switzerland | `.SW` | `NESN.SW`, `NOVN.SW` |
| Bolsa de Madrid | Spain | `.MC` | `IBE.MC`, `SAN.MC` |

## Parsing Hygiene Checklist

1. Detect delimiter (`,` vs. `;` vs. `\t`) and decimal separator (`.` vs. `,`).
2. Exclude cash rows (`CASH`, `EUR`, `USD`, `Money Market Cash`) from equity/ETF ticker resolution, but report total cash % separately.
3. Exclude closed positions (`Quantity == 0`) and summary/total footer rows.
4. When a ticker appears in multiple currencies or accounts, aggregate only positions sharing the same canonical security, or flag FX exposure explicitly.
