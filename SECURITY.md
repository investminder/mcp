# Security Policy

## Scope

This repository (`investminder/mcp`) contains documentation, MCP client configuration manifests, open-source Agent Skills (`skills/*/SKILL.md`), reference guides, sample CSV templates, and CI validation scripts. It does not contain the closed-source Investminder MCP server or backend infrastructure.

## Financial & Banking Data Boundaries

When using Investminder skills with any AI assistant connected to the [Investminder MCP server](https://github.com/investminder/mcp):

- **Never paste banking or brokerage credentials into chat.** Neither an AI assistant nor Investminder will ever ask for passwords, 2FA codes, card numbers, PINs, or IBANs.
- **Broker connections are read-only and hosted.** Synchronized portfolio connections (`listInstitutions` and `connectPortfolio`) authenticate exclusively on the hosted authorization pages of licensed open banking partners — [Powens](https://www.powens.com) (EU) and [SnapTrade](https://snaptrade.com) (US). Investminder never sees or stores your banking credentials.
- **No order execution.** Investminder never places trades or transfers funds. Decisions and execution remain strictly with you and your broker.
- **Spreadsheet privacy boundary:** When an AI assistant reads an `.xlsx` or `.csv` file during `excel-to-quant-audit`, the file's contents are transmitted to the AI assistant provider. Remove personal identifiers (account numbers, names, addresses, IBANs, tax IDs) **before** sharing the file. Stripping personal identifiers inside the skill only limits what is sent to the Investminder MCP server and what appears in summaries.

## Reporting a Vulnerability

If you discover a security issue in these skills (for example, prompt-injection vectors, unsafe file handling instructions, or compliance guardrail bypasses) or in the Investminder MCP service:

- **Email:** [security@investminder.com](mailto:security@investminder.com) or [support@investminder.com](mailto:support@investminder.com)
- **Please do not** open a public GitHub issue for security vulnerabilities.

We will acknowledge receipt within 48 hours and coordinate a fix before public disclosure.
