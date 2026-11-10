# ChatGPT / Codex plugin submission

This repository includes a portable Agent Plugins package for the Investminder remote MCP endpoint:

- `plugin.json`: listing metadata, privacy/legal/support links, five positive review scenarios, three negative review scenarios and release notes.
- `mcp.json`: Streamable HTTP MCP endpoint and OAuth declaration.

## Prepare upload

1. Review the public listing copy and confirm the selected dashboard category.
2. Add Investminder's **approved square brand logo** (at least 48 × 48 px) under `assets/`, then set `extensions.com.openai.interface.logo` and `composerIcon` to included `./assets/...` paths. Do not substitute a new or unofficial logo.
3. Run the five positive and three negative cases against a dedicated populated ELITE reviewer account. Record evidence and adjust expected outputs if the live server differs.
4. Record a walkthrough of representative tool calls and add the **reviewer-accessible video URL** as `extensions.com.openai.review.demo_recording_url`.
5. Confirm the OAuth client registration method supported by production (DCR, CIMD or a provided client) and update `mcp.json` only if necessary.
6. Create a ZIP with `plugin.json`, `mcp.json`, and included assets **at the archive root**. Do not include reviewer credentials or a client secret.
7. In the verified OpenAI organization, upload the ZIP in the Plugins dashboard, complete domain verification with the exact challenge token shown there, connect OAuth, scan tools, fix findings, and submit for review.
8. Enter reviewer login details **only** in the portal's private Review details form.

## Submission gates

- Company identity: verified by owner on 10 Nov 2026.
- Apps Management Write permission: verify.
- Account: dedicated synthetic-data ELITE reviewer account, no MFA/OTP/magic-link approval.
- Logo, walkthrough URL and actual positive/negative scenario executions: pending.
- Privacy policy: public URL exists, but ensure the policy covers MCP tool data types and sharing precisely.
- Age: published Terms require Investminder account holders to be **at least 18**. The reviewer should confirm age-gating and teen-safe responses; do not advertise account creation for minors.
- Tools: source annotations include `openWorldHint`; verify full tool catalog and annotations via the production portal scan.

Reference: https://developers.openai.com/plugins/deploy/submission
