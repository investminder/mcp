# Contributing to `investminder/mcp`

Thank you for contributing to the official **Investminder MCP & Agent Skills** repository. All skills in `skills/` follow the [Agent Skills open standard](https://agentskills.io) and are grounded 100% in the real tools exposed by [`investminder/mcp`](https://github.com/investminder/mcp).

## Core Principles

1. **100% Grounded in Real MCP Tools**
   - Every MCP tool referenced in a `SKILL.md` must exist in the verified [`investminder/mcp`](https://github.com/investminder/mcp) tool inventory.
   - Never invent, rename, or alias MCP tools or parameters.
   - Never ask the LLM to estimate financial metrics mentally — all quotes, correlations, technical indicators, fundamentals, and backtest metrics must come from `investminder/mcp` tool outputs.

2. **Strict Non-Advisory Guardrails**
   - Every skill is **quantitative decision support only** — never personalized investment advice.
   - Every `SKILL.md` must contain a `## Guardrails` section prohibiting buy/sell/hold recommendations, price targets, and guaranteed-return claims.
   - See [docs/compliance-guardrails.md](docs/compliance-guardrails.md) for the complete policy.

3. **Agent Skills Open Standard Compliance**
   - Place each skill in `skills/<skill-name>/SKILL.md`.
   - Include valid YAML frontmatter with:
     - `name`: exact match to `<skill-name>` (lowercase kebab-case)
     - `description`: clear trigger conditions and capabilities (under 1024 characters)
     - `license: MIT`
     - `compatibility`: required MCP server and client notes
     - `metadata`:
       - `author: Investminder`
       - `mcp_repo: https://github.com/investminder/mcp`
   - Keep `SKILL.md` concise (**under 350 lines**). Move reference tables, broker schemas, glossaries, and output templates into `references/` or `assets/`.

## Local Validation

Before opening a pull request, run the CI validation script locally:

```bash
python scripts/validate_skills.py --check-mcp-tools
```

This verifies:
- YAML frontmatter syntax, required fields, `name == directory_name`, and `description` length.
- `SKILL.md` line count (`<= 350` lines).
- Presence of `## Guardrails` and absence of prohibited advisory phrases.
- All relative Markdown links across the repository.
- Every referenced MCP tool name matches the verified `investminder/mcp` tool inventory.

## Pull Request Checklist

- [ ] Skill follows the folder structure (`skills/<skill-name>/SKILL.md`, optional `references/` and `assets/`).
- [ ] All MCP tool calls match exact tool names and parameter shapes from `investminder/mcp`.
- [ ] `## Guardrails` section is present and aligned with [docs/compliance-guardrails.md](docs/compliance-guardrails.md).
- [ ] `python scripts/validate_skills.py --check-mcp-tools` passes with zero errors.
- [ ] `README.md` (and `README.fr.md` where applicable) is updated if adding a new skill or tool.
