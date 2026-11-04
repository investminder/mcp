# Connect the Investminder MCP server to your AI assistant

Server URL: `https://api.investminder.com/mcp` — Streamable HTTP, OAuth sign-in with your [Investminder](https://www.investminder.com) account.

Investminder currently supports Claude, Claude Code and ChatGPT.

Back to the [README](../README.md).

## Claude (web, desktop and mobile)

1. Open **[Investminder in the Claude directory](https://claude.ai/directory/investminder)** and click **Connect**.
2. Sign in to Investminder in the window that opens.
3. In a chat, open the tools menu and make sure **Investminder** is enabled.

You can also add it as a custom connector: **Settings → Connectors → Add custom connector**, name `Investminder`, URL `https://api.investminder.com/mcp`, then **Connect**.

Connectors added on claude.ai are available in Claude Desktop and the mobile apps too. On Team and Enterprise plans, an owner adds the connector for the organization, then each member connects their own Investminder account.

The server also exposes an **onboarding** prompt: pick it from the prompts menu, or just say *"Start the Investminder onboarding"*.

## ChatGPT

1. Open **[Plugins](https://chatgpt.com/plugins)** in ChatGPT on the web.
2. Click **+**, then **Add custom MCP server**.
3. Fill in the fields:

   | Field | Value |
   |---|---|
   | Name | `Investminder` |
   | MCP server URL | `https://api.investminder.com/mcp` |
   | Authentication | `OAuth` |

4. Read ChatGPT's warning, tick the box to continue, then click **Create as a plugin**.
5. Install the plugin. When the sign-in window opens, sign in to your Investminder account and authorize the connection.

In a new chat, type `@` and select **Investminder**. To check that it works, ask: *"Show me the list of my Investminder portfolios."*

If **Add custom MCP server** does not appear, check that you are in the right workspace. On a team account, ask your admin to check your permissions.

## Claude Code

```bash
claude mcp add --transport http investminder https://api.investminder.com/mcp
```

Run `/mcp` and choose **investminder → Authenticate**. Add `--scope user` to make it available in every project.

## Troubleshooting

| Symptom | What to do |
|---|---|
| The sign-in window does not open | Allow pop-ups for your assistant, then reconnect the connector. |
| "No account exists" | You are signed in, but your Investminder profile does not exist yet. Ask *"Start the Investminder onboarding"* and the assistant creates it. Market data tools work without it. |
| A tool says your plan does not allow it | Some features depend on your plan. Compare the plans on [investminder.com/pricing](https://www.investminder.com/pricing). |
| A ticker is not found | Ask the assistant to search by name or ISIN first: tickers differ by exchange (e.g. `ASML` in New York, `ASML.AS` in Amsterdam). |
| A backtest stays `PENDING` | Backtests run asynchronously. Ask the assistant to check again in a few seconds. |
| Someone asks for my banking details | Never send banking information in a chat or to the Investminder team. Neither the assistant nor Investminder will ever ask for it: broker and bank connections are read-only and handled on the hosted page of our open banking partners, [Powens](https://www.powens.com) 🇪🇺 and [SnapTrade](https://snaptrade.com) 🇺🇸. |
| The connector disappeared after an update | Remove it and add it again with the same URL. |

Still stuck? Visit the [Investminder help center](https://help.investminder.com), email [support@investminder.com](mailto:support@investminder.com) or use the chat assistant once signed in to your Investminder account.
