# Investminder MCP Server & Agent Skills — AI investment research, strategy backtesting and portfolio tracking

[![MCP](https://img.shields.io/badge/MCP-remote%20server-6E56CF)](https://modelcontextprotocol.io)
[![Transport](https://img.shields.io/badge/transport-Streamable%20HTTP-0A7EA4)](#connection-details)
[![Auth](https://img.shields.io/badge/auth-OAuth-2EA44F)](#authentication-and-security)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-agentskills.io-6E56CF)](#agent-skills)
[![Website](https://img.shields.io/badge/website-investminder.com-111111)](https://www.investminder.com)

> **Français :** [Lire la version française (README.fr.md)](README.fr.md)

**[Investminder](https://www.investminder.com)** is an independent investment strategy platform for individual investors. This repository provides both the **Investminder MCP server** configuration/documentation ([Model Context Protocol](https://modelcontextprotocol.io)) and the official **[Agent Skills](https://agentskills.io)** pack (`skills/`) to get the full quantitative power out of it: ask Claude, Claude Code, ChatGPT, Cursor, or Cline to search stocks and ETFs, screen the market, audit a local Excel/CSV portfolio, compute correlation matrices, build and backtest rules-based strategies, and track your portfolios — in plain language.

```text
https://api.investminder.com/mcp
```

> One URL, no install, no API key. On Claude, add **[Investminder from the Claude directory](https://claude.ai/directory/investminder)**; on Claude Code, ChatGPT, Cursor, or Cline, add the URL above. Sign in to Investminder and start asking.

---

## Contents

- [What you can do](#what-you-can-do)
- [Quick start](#quick-start)
- [MCP prompts](#mcp-prompts)
- [Agent Skills](#agent-skills)
- [Example prompts](#example-prompts)
- [Available tools](#available-tools)
- [Connection details](#connection-details)
- [Authentication and security](#authentication-and-security)
- [Plans and limits](#plans-and-limits)
- [FAQ](#faq)
- [Contributing and validation](#contributing-and-validation)
- [Support](#support)

---

## What you can do

| Use case | What you ask your assistant | Tools behind it |
|---|---|---|
| **Find a stock or an ETF** | "Find the MSCI World UCITS ETFs and give me their fees" | `searchSecurities` |
| **Analyze a security** | "Show me Apple's revenue, margins and dividends over 10 years" | `analyzeSecurities` |
| **Screen the market** | "S&P 500 stocks with ROE above 20 % and a P/E under 15" | `screenSecurities`, `listScreeners`, `createScreener` |
| **Check diversification** | "How correlated are SPY, QQQ, GLD and TLT since 2015?" | `getCorrelationMatrix` |
| **Start from a proven strategy** | "Show me passive, highly diversified ETF strategies" | `listPreBuiltStrategies` |
| **Build & publish your strategy** | "Create a 60/40 ETF portfolio rebalanced every quarter" | `createStrategy`, `updateStrategy`, `publishStrategy` |
| **Backtest it** | "Backtest it from 2008 with $10,000 plus $300 a month, against SPY" | `startBacktest`, `listBacktests` |
| **Track & link your portfolio** | "Create a GBP portfolio and record my 50 shares of ULVR.L at £45" | `createPortfolio`, `addPortfolioPosition`, `addPortfolioCash`, `linkPortfolioStrategy` |
| **Sync your broker** | "Connect my brokerage account" | `listInstitutions`, `connectPortfolio` |
| **Get started** | "What can Investminder do for me?" | `startOnboarding`, prompt `onboarding` |

Coverage includes stocks, ETFs and forex listed in the United States (Nasdaq) and on the London, Frankfurt, Paris, Amsterdam, Madrid and Zurich exchanges, with constituents of the S&P 500 🇺🇸, Nasdaq-100 🇺🇸, Russell 2000 🇺🇸, MSCI World 🌍, STOXX Europe 600 🇪🇺, Euro Stoxx 50 🇪🇺, CAC 40 🇫🇷, DAX 🇩🇪, FTSE 100 🇬🇧, IBEX 35 🇪🇸, AEX 🇳🇱, SMI 🇨🇭 and Nikkei 225 🇯🇵, and UCITS 🇪🇺 / PEA 🇫🇷 eligibility filters for European investors.

Responses are available in **English, French, Spanish and German**.

---

## Quick start

The server is a **remote MCP server** (Streamable HTTP). It is officially supported on Claude, Claude Code and ChatGPT, and compatible with MCP editors supporting Streamable HTTP + OAuth (Cursor, Cline).

- **Claude** (web, desktop and mobile): open **[Investminder in the Claude directory](https://claude.ai/directory/investminder)** and connect it.
- **Claude Code**: `claude mcp add --transport http investminder https://api.investminder.com/mcp`
- **ChatGPT** (web): in [Plugins](https://chatgpt.com/plugins), click **+ → Add custom MCP server** with the URL `https://api.investminder.com/mcp` and OAuth authentication.
- **Cursor / Cline**: add `https://api.investminder.com/mcp` as a remote Streamable HTTP server with OAuth.

Then sign in to Investminder and ask: *"What can Investminder do for me?"*

Step-by-step setup and troubleshooting for each client: [docs/clients.md](docs/clients.md).

---

## MCP prompts

The server exposes five guided MCP prompts that adapt to your account status (market-data steps work without an Investminder profile, and the prompt offers to create a free Basic profile when a workflow needs one):

| Prompt | What it does | Optional argument |
|---|---|---|
| `onboarding` | Guided introduction: profile, 4-question quiz, recommended pre-built strategies, and first step (also available as the `startOnboarding` tool). | None |
| `audit-portfolio` | Quantitative audit of an Excel/CSV file or an Investminder portfolio: correlations, 12-month volatility and drawdown, UCITS/PEA ETF alternatives, and allocation backtest. | None |
| `backtest-strategy` | Turns a plain-English thesis or a catalog strategy (with official UCITS/PEA variants) into a strategy draft, runs a backtest against a benchmark, and delivers a pre-mortem. | `thesis` (starting strategy idea or pre-built approach) |
| `analyze-stock` | Technical diagnostic (moving averages, RSI, MACD, 12-month volatility and drawdown) and fundamental review (financial statements, dividends, P/E history with an Investminder profile). | `ticker` (name, ticker symbol, or ISIN) |
| `screen-market` | Screens US and European stocks and ETFs (including UCITS and PEA filters) using Investminder presets or custom criteria. | None |

- **Claude** (web, desktop and mobile): launch any prompt from the prompts / connectors menu.
- **Claude Code**: invoke prompts as slash commands using `/mcp__investminder__<name>` (for example, `/mcp__investminder__analyze-stock ASML.AS`).

MCP prompts are available in MCP clients that support prompts; in other clients, use natural-language requests (see [Example prompts](#example-prompts) and [docs/examples.md](docs/examples.md)). Prompts launch a guided workflow in one click from the client, whereas the [Agent Skills](#agent-skills) below guide assistants that have installed them (`audit-portfolio` ↔ `excel-to-quant-audit`, `backtest-strategy` ↔ `quant-strategy-backtest`, `analyze-stock` ↔ `technical-regime-check` + `fundamental-quality-xray`, `screen-market` ↔ `securities-screener-workflow`).

---

## Agent Skills

Install the official **[Agent Skills](https://agentskills.io)** bundled in this repository so your AI assistant follows disciplined, multi-step quantitative workflows (zero mental math, strict non-advisory guardrails) on top of the Investminder MCP server:

```bash
npx skills add investminder/mcp
```

| Skill | Purpose | Verified MCP tools orchestrated |
|---|---|---|
| **[`excel-to-quant-audit`](skills/excel-to-quant-audit/SKILL.md)** | Reads an `.xlsx`/`.csv` portfolio tracker or broker export (IBKR, DEGIRO, Trade Republic, BoursoBank, Saxo, Trading 212 — remove personal identifiers before sharing since files are sent to your AI assistant provider), resolves tickers/ISINs, runs correlation, volatility, ETF fee checks, and a historical backtest on the declared target allocation (`TargetWeightPct` in [sample-portfolio.csv](skills/excel-to-quant-audit/assets/sample-portfolio.csv)), and offers read-only broker sync or manual portfolio import. | `searchSecurities`, `getCorrelationMatrix`, `analyzeSecurities`, `screenSecurities`, `createStrategy`, `startBacktest`, `listBacktests`, `listInstitutions`, `connectPortfolio`, `createPortfolio`, `addPortfolioCash`, `addPortfolioPosition`, `listPortfolios`, `startOnboarding`, `upsertUser` |
| **[`multi-asset-correlation-xray`](skills/multi-asset-correlation-xray/SKILL.md)** | Computes multi-window daily-return Pearson correlation matrices across 2–20 stocks, ETFs, bonds, and commodities to surface redundant clusters (`r >= 0.80`) and true diversifiers. | `searchSecurities`, `getCorrelationMatrix`, `analyzeSecurities`, `screenSecurities`, `listPortfolios` |
| **[`quant-strategy-backtest`](skills/quant-strategy-backtest/SKILL.md)** | Translates a plain-English thesis (or pre-built template, applying official UCITS/PEA `variants` directly) into a `REBALANCED`, `PROGRESSIVE`, or `RANKED` strategy draft, runs an async historical backtest with inflows/outflows, and delivers a 6-point risk pre-mortem. | `listPreBuiltStrategies`, `listUserStrategies`, `searchSecurities`, `screenSecurities`, `analyzeSecurities`, `createStrategy`, `updateStrategy`, `startBacktest`, `listBacktests`, `publishStrategy`, `linkPortfolioStrategy`, `deleteStrategy`, `getCorrelationMatrix` |
| **[`withdrawal-stress-test`](skills/withdrawal-stress-test/SKILL.md)** | Stress-tests retirement / FIRE decumulation (`outflowRules`, fixed-amount vs. percentage modes) across harsh historical start dates (2000, 2008, 2022) to evaluate sequence-of-returns risk, `totalOutflow`, `maxDrawdown`, and `annualReturns`. | `listPreBuiltStrategies`, `listUserStrategies`, `searchSecurities`, `analyzeSecurities`, `createStrategy`, `startBacktest`, `listBacktests` |
| **[`fundamental-quality-xray`](skills/fundamental-quality-xray/SKILL.md)** | Audits multi-year financial statements (`YEARLY`/`QUARTERLY`), margins, FCF, debt, dividend sustainability, historical P/E ranges, and `scoreFinancial.global.score`, with optional peer screening. | `searchSecurities`, `analyzeSecurities`, `screenSecurities` |
| **[`securities-screener-workflow`](skills/securities-screener-workflow/SKILL.md)** | Builds schema-valid `screenSecurities` filters across US & European equities/ETFs (S&P 500, Nasdaq-100, MSCI World, STOXX Europe 600, Euro Stoxx 50, CAC 40, DAX, FTSE 100, SMI, IBEX 35, AEX, Nikkei 225, with `UCITS` / `PEA` filters), replays saved screeners/presets, and tightens loose universes iteratively. | `listScreeners`, `screenSecurities`, `searchSecurities`, `analyzeSecurities`, `getCorrelationMatrix` |
| **[`technical-regime-check`](skills/technical-regime-check/SKILL.md)** | Objectively classifies trend (`performance.price` vs. `ema20`, `ema50`, `sma100`, `sma200`), momentum (`rsi14`, `rsi21`, `macd`, `macdSignal`), volatility (`atr`, `volatility12m`), drawdown, `scoreTechnical.global.score`, and `VOLUME_PROFILE`. | `searchSecurities`, `analyzeSecurities`, `screenSecurities`, `getCorrelationMatrix`, `createStrategy`, `startBacktest`, `listBacktests` |
| **[`cashflow-rebalance-planner`](skills/cashflow-rebalance-planner/SKILL.md)** | Analyzes allocation drift vs. a linked strategy or custom target and presents illustrative deposit arithmetic under user-chosen rules without selling existing holdings. | `listPortfolios`, `listUserStrategies`, `searchSecurities`, `analyzeSecurities`, `linkPortfolioStrategy`, `addPortfolioCash`, `addPortfolioPosition` |
| **[`weekly-quant-brief`](skills/weekly-quant-brief/SKILL.md)** | Produces a structured weekly portfolio & watchlist check-in covering cash balances, 7-day transactions, summary allocation drift vs. linked strategy, technical regimes, and correlation watch. | `listPortfolios`, `listPortfolioTransactions`, `listUserStrategies`, `searchSecurities`, `analyzeSecurities`, `getCorrelationMatrix`, `screenSecurities`, `startBacktest` |

Compliance and decision-support boundaries for all skills: [docs/compliance-guardrails.md](docs/compliance-guardrails.md).

---

## Example prompts

Copy any of these into your assistant once the connector is enabled:

- *"Audit `skills/excel-to-quant-audit/assets/sample-portfolio.csv` using `excel-to-quant-audit`: resolve the tickers, run a 5-year correlation matrix, check 12-month volatility and drawdowns, and backtest this allocation from 2020 against SPY."*
- *"Start the Investminder onboarding and recommend a strategy that fits me."*
- *"Find UCITS ETFs that track the S&P 500, listed in Amsterdam or Frankfurt, and compare their 5-year performance."*
- *"Screen Nasdaq-100 stocks with a gross margin above 60 %, debt/equity below 0.5 and positive 12-month momentum."*
- *"Give me Microsoft's quarterly income statements and P/E history since 2019."*
- *"Compute the correlation matrix of VWCE.DE, EUNA.DE, IGLN.L and SPY over the last 5 years and tell me what actually diversifies."*
- *"Take the best-rated trend-following pre-built strategy, swap its ETFs for UCITS equivalents and backtest it from 2007 against SPY."*
- *"Build a dividend strategy on 5 ETFs, buy when RSI 14 drops below 35, and backtest it with $500 a month."*
- *"Show me my portfolios with their positions and cash."*

More recipes, from first steps to advanced strategy design: [docs/examples.md](docs/examples.md).

---

## Available tools

| Tool | Description | Investminder profile needed |
|---|---|---|
| `startOnboarding` | Guided introduction and first steps | No |
| `upsertUser` | Create or update your Investminder profile (country, currency, language, investor profile) | No |
| `searchSecurities` | Find stocks, ETFs and forex pairs by name, ticker or ISIN | No |
| `screenSecurities` | Filter securities on fundamentals, valuation, momentum, index, country, UCITS 🇪🇺 / PEA 🇫🇷… | No |
| `analyzeSecurities` | Quotes, performance, technical indicators, volume profile; financial statements, dividends and P/E history | Partly |
| `getCorrelationMatrix` | Pearson correlation of daily returns for 2 to 20 tickers | No |
| `listScreeners` | Your saved screeners and the Investminder presets | No for the presets |
| `createScreener` / `updateScreener` / `deleteScreener` | Save a screen as a screener of your own, edit it or delete it; it shows up in the web app's Screener | Yes |
| `listPreBuiltStrategies` | Catalog of ready-made strategies, filterable by approach, diversification and activity | Yes |
| `createStrategy` / `updateStrategy` / `publishStrategy` / `deleteStrategy` | Build, edit, publish and delete rules-based strategies (`REBALANCED`, `PROGRESSIVE`, `RANKED`) | Yes |
| `listUserStrategies` | Your strategies with their editable draft and live version | Yes |
| `startBacktest` / `listBacktests` | Run a backtest with contributions and withdrawals, then read its results vs. a benchmark | Yes |
| `createPortfolio` / `addPortfolioCash` / `addPortfolioPosition` | Track a manual portfolio | Yes |
| `listPortfolios` / `listPortfolioTransactions` | Read portfolios, positions, cash and history | Yes |
| `linkPortfolioStrategy` | Link an unlocked portfolio to a published strategy for tracking and alerts | Yes |
| `listInstitutions` / `connectPortfolio` | Connect a broker or bank, read-only, through a hosted flow run by licensed open banking partners. Investminder never sees your banking credentials | Yes |

Full reference with parameters and tips: [docs/tools.md](docs/tools.md).

---

## Connection details

| | |
|---|---|
| **Server URL** | `https://api.investminder.com/mcp` |
| **Transport** | Streamable HTTP |
| **Authentication** | OAuth (sign in with your Investminder account) |
| **Languages** | en, fr, es, de |
| **Local install** | None — the server is hosted by Investminder |

---

## Authentication and security

- You sign in on Investminder's own page. Your assistant never sees your password.
- **Investminder has no access to your banking information.** Broker and bank connections go through two licensed open banking partners, [Powens](https://www.powens.com) 🇪🇺 and [SnapTrade](https://snaptrade.com) 🇺🇸: you authenticate on their hosted authorization page, never on Investminder's.
- **Broker and bank access is read-only.** Investminder can read your positions, cash and transactions to keep your portfolios up to date. It cannot move money or place orders.
- **Never send banking information in a chat, and never send it to the Investminder team** (password, code, card number, IBAN…). Neither the assistant nor anyone at Investminder will ever ask you for it.
- Every tool is scoped to the signed-in account: an assistant can only read and change your own strategies and portfolios.
- **Investminder never places orders.** It helps you decide; your broker executes. See [the place of Investminder in your financial ecosystem](https://help.investminder.com/en/how-to-use/the-place-of-investminder-in-your-financial-ecosystem-1wm3ccl/) and [SECURITY.md](SECURITY.md).

This repository contains documentation, configuration examples, and Agent Skills only. The server itself is closed source and operated by Investminder.

---

## Plans and limits

Market data tools (search, screening, quotes, performance, technical indicators, correlation) work as soon as you sign in, even before you create your Investminder profile. Financial statement and dividend history depth, the strategy catalog, the number of strategies, backtests, portfolios and broker connections depend on your Investminder plan. When a limit applies, the assistant tells you.

---

## FAQ

**What is an MCP server?**
The [Model Context Protocol](https://modelcontextprotocol.io) is an open standard that lets AI assistants call external tools. The Investminder MCP server exposes Investminder's market data, strategy builder, backtesting engine and portfolio tracker as tools your assistant can use.

**Do I need an Investminder account?**
You sign in once when you connect, which identifies you to Investminder. Market data tools work right away. To build strategies or track portfolios you also need an Investminder profile (country, currency, language): the assistant creates it for you through the onboarding.

**Which AI assistants are supported?**
Claude (web, desktop and mobile, from the [Claude directory](https://claude.ai/directory/investminder)), Claude Code, ChatGPT, and MCP clients supporting remote Streamable HTTP + OAuth such as Cursor and Cline.

**Is it financial advice?**
No. Investminder provides data, analysis and simulation tools. Past performance and backtests do not guarantee future results. Decisions and their execution remain yours.

**Can the assistant trade for me?**
No. Investminder has no order execution. It records the trades you tell it about and synchronizes the accounts you connect, but it never sends orders to your broker.

**Where does the data come from, and how fresh is it?**
Every `analyzeSecurities` response carries `earliestDate` and `latestDate`, the first and last known quote dates of the security, so you always know the as-of date of the data.

---

## Contributing and validation

Validate all Agent Skills YAML frontmatter, guardrails, relative Markdown links, and MCP tool references locally:

```bash
python scripts/validate_skills.py --check-mcp-tools
```

See [CONTRIBUTING.md](CONTRIBUTING.md) and [LICENSE](LICENSE) (MIT).

---

## Support

- Website: **[investminder.com](https://www.investminder.com)**
- Claude connector: [Investminder in the Claude directory](https://claude.ai/directory/investminder)
- Help center: [help.investminder.com](https://help.investminder.com/en/)
- Getting started: [complete your onboarding](https://help.investminder.com/en/onboarding/how-to-complete-your-onboarding-and-get-your-first-strategy-recommendation-90expl/)
- Strategy builder: [how to build a strategy](https://help.investminder.com/en/how-to-use/how-to-build-a-strategy-ez04de/)
- Contact: email [support@investminder.com](mailto:support@investminder.com), or use the chat assistant once signed in to your Investminder account

---

<sub>Investminder is not a bank, a broker or an investment advisor. Content provided for information purposes only. Investing involves risk of capital loss.</sub>
