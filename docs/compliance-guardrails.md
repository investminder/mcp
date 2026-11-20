# Compliance & Decision-Support Guardrails

Every skill in [`investminder/mcp`](https://github.com/investminder/mcp) (`skills/`) is designed strictly for **quantitative research, education, and decision support** — never personalized investment advice. This policy mirrors the legal, security, and operational boundaries of [Investminder](https://www.investminder.com).

---

## 1. Non-Advisory Boundaries

Investminder is **not** a bank, a broker, or a registered investment advisor. Every `SKILL.md` enforces the following rules:

- **No buy, sell, or hold recommendations.** Present objective metrics, trade-offs, historical drawdown behavior, and rule-based comparisons. Never tell a user to buy, sell, hold, enter, or exit a specific security.
- **No price targets or return guarantees.** Never forecast future prices or promise future performance. Always note that historical correlations, technical regimes, and backtest results do not guarantee future outcomes.
- **No personalized suitability claims.** Do not tell a user that a security or strategy is "right for them" or "suitable for their financial situation." Present factual outputs so the user decides independently.
- **No order execution.** Investminder has no brokerage execution capability. If a user asks the assistant to place a trade or move funds, explicitly state that Investminder provides research, simulation, and portfolio tracking only, and that execution happens at their broker.

---

## 2. Quantitative Integrity Rules (Market Data vs. Transparent Arithmetic)

Distinguish clearly between **prohibited market-data fabrication** and **permitted arithmetic on returned values**:

- **Prohibited — inventing or estimating market data:** Never invent, extrapolate, or mentally estimate any market quote, return, volatility figure, drawdown, correlation coefficient, RSI, moving average, expense ratio, FX rate, or financial statement figure. Every market figure must come directly from an `investminder/mcp` tool response (`searchSecurities`, `screenSecurities`, `analyzeSecurities`, `getCorrelationMatrix`, `listBacktests`, `listPortfolios`). If a requested metric is not returned by any tool, state explicitly that it is unavailable and never estimate it.
- **Permitted — transparent arithmetic on tool outputs:** Basic arithmetic derived strictly from values returned by `investminder/mcp` (or user-confirmed inputs such as a deposit amount or FX rate) — for example, computing position value (`quantity × priceLast`), portfolio weights, allocation drift, cashflow scenarios, or reading the minimum entry in `annualReturns` — is permitted **only when** the assistant shows the calculation steps transparently and uses a code-execution tool whenever the client provides one.
- **Always report as-of dates:** Every `analyzeSecurities` response includes `earliestDate` and `latestDate`. Surface data boundaries and backtest date ranges clearly.
- **Handle uncovered tickers and missing metrics transparently:** If `analyzeSecurities` returns `found: false` or `getCorrelationMatrix` returns `unknownTickers`, never fabricate data or silently substitute another ticker. If a risk metric (`volatility12m`, `maxDrawdown12m`) is absent due to short history, report it as `"not available"`, never zero.
- **Respect currency units:** In `analyzeSecurities` (`PERFORMANCE`), `marketCap` is in the security's quote currency (`GBX` means British pence, not GBP) while `marketCapUsd` is in USD. Never sum mixed-currency holdings without user-confirmed FX rates.
- **Respect weight validation:** A `REBALANCED` strategy requires target weights (`percentTarget`) summing to exactly `100%` and matching `constraints.assetClasses`. Never silently normalize invalid weights; flag the mismatch and ask the user to confirm.

---

## 3. Banking & Privacy Guardrails

- **Never request or accept banking credentials in chat.** Passwords, 2FA codes, PINs, card numbers, and IBANs must never be entered in chat or sent to Investminder.
- **Read-only open banking only.** Broker and bank sync via `listInstitutions` and `connectPortfolio` redirects the user to the hosted authorization page of licensed open banking partners — [Powens](https://www.powens.com) (EU) and [SnapTrade](https://snaptrade.com) (US). Access is strictly read-only.
- **Spreadsheet data-sharing boundary:** When an AI assistant reads an `.xlsx` or `.csv` file (`excel-to-quant-audit`), the file's contents are transmitted to the AI assistant provider. Recommend that the user remove account numbers, personal names, addresses, IBANs, and tax IDs **before** sharing the file. Excluding personal identifiers during skill execution only limits what is sent to the Investminder MCP server and what appears in summaries.
- **Non-idempotent write warnings.** `addPortfolioPosition`, `addPortfolioCash`, and `createPortfolio` append operations rather than replacing balances. Always confirm with the user before writing and inspect `listPortfolios` / `listPortfolioTransactions` rather than blindly retrying.

---

<sub>Investminder is not a bank, a broker, or an investment advisor. Content is provided for informational and educational purposes only. Investing involves risk of capital loss.</sub>
