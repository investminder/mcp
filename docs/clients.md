# Connect the Investminder MCP server to your AI assistant

Server URL: `https://api.investminder.com/mcp` — Streamable HTTP, OAuth sign-in with your [Investminder](https://www.investminder.com) account.

Back to the [README](../README.md).

## Claude (web, desktop and mobile)

1. **Settings → Connectors → Add custom connector**.
2. Name `Investminder`, URL `https://api.investminder.com/mcp`.
3. **Connect**, then sign in to Investminder in the window that opens.
4. In a chat, open the tools menu and make sure **Investminder** is enabled.

Connectors added on claude.ai are available in Claude Desktop and the mobile apps too. On Team and Enterprise plans, an owner adds the connector for the organization, then each member connects their own Investminder account.

The server also exposes an **onboarding** prompt: pick it from the prompts menu, or just say *"Start the Investminder onboarding"*.

## ChatGPT

1. **Settings → Apps & Connectors**. If your plan requires it, enable **Developer mode** under the advanced settings.
2. **Create** a connector: name `Investminder`, URL `https://api.investminder.com/mcp`, authentication **OAuth**.
3. Sign in to Investminder, then add the connector to a new chat.

## Claude Code

```bash
claude mcp add --transport http investminder https://api.investminder.com/mcp
```

Run `/mcp` and choose **investminder → Authenticate**. Add `--scope user` to make it available in every project.

## Cursor

`~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (project):

```json
{
  "mcpServers": {
    "investminder": {
      "url": "https://api.investminder.com/mcp"
    }
  }
}
```

Open **Settings → MCP** and click **Connect** next to Investminder to sign in.

## VS Code (GitHub Copilot agent mode)

`.vscode/mcp.json`:

```json
{
  "servers": {
    "investminder": {
      "type": "http",
      "url": "https://api.investminder.com/mcp"
    }
  }
}
```

Click **Start** above the server entry, then sign in when prompted. Use Copilot Chat in **Agent** mode.

## Windsurf

`~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "investminder": {
      "serverUrl": "https://api.investminder.com/mcp"
    }
  }
}
```

## Gemini CLI

`~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "investminder": {
      "httpUrl": "https://api.investminder.com/mcp"
    }
  }
}
```

Run `/mcp auth investminder` to sign in.

## Other clients (stdio only)

Use the [`mcp-remote`](https://www.npmjs.com/package/mcp-remote) bridge (requires Node.js 18+):

```json
{
  "mcpServers": {
    "investminder": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://api.investminder.com/mcp"]
    }
  }
}
```

## Troubleshooting

| Symptom | What to do |
|---|---|
| The sign-in window does not open | Allow pop-ups for your assistant, then reconnect the connector. |
| "No account exists" | Normal for a new user: ask *"Start the Investminder onboarding"* and the assistant creates your profile. |
| A tool says your plan does not allow it | Some features depend on your plan. Check your plan on [investminder.com](https://www.investminder.com). |
| A ticker is not found | Ask the assistant to search by name or ISIN first: tickers differ by exchange (e.g. `CW8.PA`, `VWCE.DE`). |
| A backtest stays `PENDING` | Backtests run asynchronously. Ask the assistant to check again in a few seconds. |
| The connector disappeared after an update | Remove it and add it again with the same URL. |

Still stuck? Visit the [Investminder help center](https://help.investminder.com/en/) or [open an issue](https://github.com/investminder/investminder-mcp/issues).
