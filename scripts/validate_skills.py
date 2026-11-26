#!/usr/bin/env python3
"""Validate Agent Skills in investminder/mcp against the Agent Skills standard,
compliance guardrails, relative Markdown links, and verified MCP tool inventory."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
MAX_SKILL_LINES = 350
MAX_DESCRIPTION_LEN = 1024

# Verified tool inventory extracted directly from investminder/mcp & Investminder MCP gateway
VERIFIED_MCP_TOOLS = {
    "startOnboarding",
    "upsertUser",
    "searchSecurities",
    "screenSecurities",
    "analyzeSecurities",
    "getCorrelationMatrix",
    "listScreeners",
    "listPreBuiltStrategies",
    "listUserStrategies",
    "createStrategy",
    "updateStrategy",
    "publishStrategy",
    "deleteStrategy",
    "startBacktest",
    "listBacktests",
    "createPortfolio",
    "addPortfolioPosition",
    "addPortfolioCash",
    "listPortfolios",
    "listPortfolioTransactions",
    "linkPortfolioStrategy",
    "listInstitutions",
    "connectPortfolio",
}

# Known camelCase parameter/field names that appear in backticks inside skills/ (not MCP tool names)
KNOWN_CAMEL_IDENTIFIERS = {
    "annualGrowthEps",
    "annualGrowthFreeCashFlow",
    "annualGrowthNetProfit",
    "annualGrowthSharesNumber",
    "annualGrowthTotalRevenue",
    "annualPerf",
    "annualReturns",
    "assetClass",
    "backtestId",
    "cashManagement",
    "currentRatio",
    "debtEquityRatio",
    "delayYears",
    "distributionFrequency",
    "distributionPolicy",
    "dividendPayoutRatio",
    "dividendYield",
    "earliestDate",
    "endDate",
    "globalPerf",
    "grossMargin",
    "holdingsCount",
    "inflowRules",
    "lastUpdated",
    "latestDate",
    "macdSignal",
    "marketCap",
    "marketCapUsd",
    "maxDrawdown",
    "maxDrawdown12m",
    "minDatetime",
    "netExpenseRatio",
    "netMargin",
    "operatingMargin",
    "outflowRules",
    "percentMax",
    "percentTarget",
    "perfOneMonth",
    "perfSixMonth",
    "perfThirtySixMonth",
    "perfThreeMonth",
    "perfTwelveMonth",
    "perfTwentyFourMonth",
    "portfolioId",
    "priceLast",
    "quoteFrequency",
    "regularAmount",
    "regularPercent",
    "regulatoryFramework",
    "scoreFinancial",
    "scoreTechnical",
    "shareholderReturn",
    "sharesMax",
    "sortBy",
    "sortOrder",
    "startDate",
    "statementFrequency",
    "stockIndex",
    "strategyId",
    "strategyModel",
    "technicalIndicators",
    "tickerRecognized",
    "totalAssets",
    "totalInflow",
    "totalOutflow",
    "unknownTickers",
    "valueAveraging",
}

# Verified uppercase enum values from the Investminder MCP server
VERIFIED_UPPERCASE_ENUMS = {
    # screenSecurities.sortBy (including CU-z8udzkrrj7)
    "ID",
    "TICKER",
    "NAME",
    "PERF_ONE_MONTH",
    "PERF_THREE_MONTH",
    "PERF_SIX_MONTH",
    "PERF_TWELVE_MONTH",
    "PERF_TWENTY_FOUR_MONTH",
    "PERF_THIRTY_SIX_MONTH",
    "MOMENTUM_1_3_6",
    "MOMENTUM_3_6_12",
    "MARKET_CAP",
    "TOTAL_ASSETS",
    "PEG",
    "NET_MARGIN",
    "DIVIDEND_YIELD",
    "RSI_14",
    "RSI_21",
    "SCORE_FINANCIAL",
    "SCORE_TECHNICAL",
    "VOLATILITY_12M",
    "MAX_DRAWDOWN_12M",
    # stockIndex
    "SP_500",
    "CAC_40",
    "DAX",
    "FTSE_100",
    "NASDAQ_100",
    "NIKKEI_225",
    "RUSSELL_2000",
    "MSCI_WORLD",
    "STOXX_EUROPE_600",
    "EURO_STOXX_50",
    "IBEX_35",
    "AEX",
    "SMI",
    # currency
    "USD",
    "EUR",
    "GBP",
    "GBX",
    "CHF",
    # category
    "BOND",
    "COMMODITY",
    "CRYPTO",
    "CURRENCY",
    "STOCK",
    # location
    "NORTH_AMERICA",
    "LATIN_AMERICA",
    "EUROPE",
    "ASIA",
    "WORLD",
    # distributionPolicy
    "ACCUMULATING",
    "DISTRIBUTING",
    # assetClass
    "ETF",
    "FOREX",
    # analyzeSecurities & searchSecurities fields
    "QUOTES",
    "PERFORMANCE",
    "TECHNICAL_INDICATORS",
    "FINANCIAL_STATEMENTS",
    "DIVIDENDS",
    "VOLUME_PROFILE",
    "PER",
    "DESCRIPTION",
    # frequencies & screener types
    "DAILY",
    "WEEKLY",
    "MONTHLY",
    "QUARTERLY",
    "YEARLY",
    "PRESET",
    # listBacktests fields, catalog types & statuses
    "HOLDINGS",
    "TRANSACTIONS",
    "ANNUAL_RETURNS",
    "PERFORMANCE_METRICS",
    "USER",
    "PRE_BUILT",
    "PENDING",
    "COMPLETED",
    "FAILED",
    # strategy indicators
    "DRAWDOWN",
    "EMA_20",
    "EMA_50",
    "SMA_100",
    "SMA_200",
    "MACD",
    "MACD_SIGNAL",
    "ATR",
    "PRICE",
    "PRICE_PREVIOUS",
    "ALLOCATION_GAP",
    "MONTH_INDEX",
    # strategy models & asset classes
    "REBALANCED",
    "PROGRESSIVE",
    "RANKED",
    "ETF_STOCKS",
    "ETF_BONDS",
    "ETF_COMMODITIES",
    "ETF_CURRENCIES",
    "ETF_CRYPTOS",
    "STOCKS",
    # regulatory frameworks, statuses & sort orders
    "UCITS",
    "PEA",
    "DRAFT",
    "LIVE",
    "ASC",
    "DESC",
    # operators & logic
    "EQUALS",
    "HIGHER_THAN",
    "LOWER_THAN",
    "HIGHER_THAN_OR_EQUALS",
    "LOWER_THAN_OR_EQUALS",
    "NOT_EQUAL",
    "AND",
    "OR",
    # listPreBuiltStrategies filters
    "TREND_FOLLOWING",
    "BALANCED",
    "DIVIDEND_FOCUSED",
    "CORE_SATELLITE",
    "MEAN_REVERSION",
    "PASSIVE_INVESTOR",
    "ACTIVE_INVESTOR",
}

# Short country codes, sample US tickers, and broker CSV column names used in backticks
ALLOWED_UPPERCASE_SHORTHANDS = {
    "USA",
    "FRA",
    "DEU",
    "GBR",
    "CHE",
    "NLD",
    "ESP",
    "ISIN",
    "ROE",
    "ROIC",
    "PRU",
    "CASH",
    "CCY",
    "SPY",
    "QQQ",
    "TLT",
    "GLD",
    "AAPL",
    "MSFT",
    "ASML",
}

PROHIBITED_ADVISORY_PATTERNS = [
    re.compile(r"\byou should (buy|sell|short|hold)\b", re.IGNORECASE),
    re.compile(r"\bstrong (buy|sell)\b", re.IGNORECASE),
    re.compile(r"\bbuy now\b", re.IGNORECASE),
    re.compile(r"\bsell immediately\b", re.IGNORECASE),
    re.compile(r"\bguaranteed returns?\b", re.IGNORECASE),
    re.compile(r"\brisk[- ]free profit\b", re.IGNORECASE),
    re.compile(r"\bprice target of\b", re.IGNORECASE),
]

NEGATION_CONTEXT = re.compile(
    r"\b(never|no|not|without|prohibit|forbid|avoid|do not|don't)\b", re.IGNORECASE
)

MD_LINK_RE = re.compile(r"(?<!\!)\[[^\]]+\]\(([^)]+)\)")
CAMEL_BACKTICK_RE = re.compile(r"`([a-z]+[A-Z][a-zA-Z0-9]*)`")
UPPER_BACKTICK_RE = re.compile(r"`([A-Z][A-Z0-9_]+)`")


def parse_frontmatter(text: str) -> tuple[dict[str, object] | None, str, str | None]:
    """Minimal YAML frontmatter parser (handles flat keys + one level of nested mapping)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text, "Missing opening YAML frontmatter delimiter '---'"

    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return None, text, "Missing closing YAML frontmatter delimiter '---'"

    fm_lines = lines[1:end_idx]
    body = "\n".join(lines[end_idx + 1 :])
    data: dict[str, object] = {}
    current_parent: str | None = None

    for idx, raw_line in enumerate(fm_lines, start=2):
        if not raw_line.strip() or raw_line.strip().startswith("#"):
            continue
        if raw_line.startswith("  ") and current_parent is not None:
            stripped = raw_line.strip()
            if ":" not in stripped:
                return None, body, f"Invalid nested YAML line {idx}: {raw_line!r}"
            k, v = stripped.split(":", 1)
            parent_dict = data.setdefault(current_parent, {})
            assert isinstance(parent_dict, dict)
            parent_dict[k.strip()] = v.strip().strip('"').strip("'")
        else:
            if ":" not in raw_line:
                return None, body, f"Invalid YAML line {idx}: {raw_line!r}"
            k, v = raw_line.split(":", 1)
            key = k.strip()
            val = v.strip().strip('"').strip("'")
            if val == "":
                data[key] = {}
                current_parent = key
            else:
                data[key] = val
                current_parent = None

    return data, body, None


def validate_skill_file(skill_md: Path, check_mcp_tools: bool) -> list[str]:
    errors: list[str] = []
    rel = skill_md.relative_to(ROOT).as_posix()
    dir_name = skill_md.parent.name
    content = skill_md.read_text(encoding="utf-8")
    lines = content.splitlines()

    if len(lines) > MAX_SKILL_LINES:
        errors.append(f"{rel}: exceeds {MAX_SKILL_LINES} lines ({len(lines)} lines)")

    fm, body, fm_err = parse_frontmatter(content)
    if fm_err or fm is None:
        errors.append(f"{rel}: {fm_err}")
        return errors

    name = fm.get("name")
    if name != dir_name:
        errors.append(f"{rel}: frontmatter name '{name}' != directory name '{dir_name}'")

    description = fm.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{rel}: missing or empty 'description'")
    elif len(description) > MAX_DESCRIPTION_LEN:
        errors.append(
            f"{rel}: description length {len(description)} exceeds {MAX_DESCRIPTION_LEN} chars"
        )

    for req_key in ("license", "compatibility"):
        val = fm.get(req_key)
        if not isinstance(val, str) or not val.strip():
            errors.append(f"{rel}: missing or empty '{req_key}'")

    metadata = fm.get("metadata")
    if not isinstance(metadata, dict):
        errors.append(f"{rel}: missing 'metadata' mapping")
    else:
        if metadata.get("author") != "Investminder":
            errors.append(f"{rel}: metadata.author must be 'Investminder'")
        if metadata.get("mcp_repo") != "https://github.com/investminder/mcp":
            errors.append(
                f"{rel}: metadata.mcp_repo must be 'https://github.com/investminder/mcp'"
            )

    if not re.search(r"^##\s+Guardrails\s*$", body, re.MULTILINE):
        errors.append(f"{rel}: missing required '## Guardrails' section")

    for line_no, line in enumerate(lines, start=1):
        for pat in PROHIBITED_ADVISORY_PATTERNS:
            if pat.search(line) and not NEGATION_CONTEXT.search(line):
                errors.append(
                    f"{rel}:{line_no}: prohibited advisory phrasing matched {pat.pattern!r}"
                )

    if check_mcp_tools:
        errors.extend(validate_camel_identifiers(skill_md, body))

    errors.extend(validate_uppercase_enums(skill_md, body))

    return errors


def validate_camel_identifiers(md_path: Path, body: str) -> list[str]:
    errors: list[str] = []
    rel = md_path.relative_to(ROOT).as_posix()
    body_no_code = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    for match in CAMEL_BACKTICK_RE.finditer(body_no_code):
        token = match.group(1)
        if token in VERIFIED_MCP_TOOLS or token in KNOWN_CAMEL_IDENTIFIERS:
            continue
        errors.append(
            f"{rel}: unverified camelCase tool/identifier `{token}` "
            "(not in verified investminder/mcp inventory)"
        )
    return errors


def validate_uppercase_enums(md_path: Path, body: str) -> list[str]:
    errors: list[str] = []
    rel = md_path.relative_to(ROOT).as_posix()
    body_no_code = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    for match in UPPER_BACKTICK_RE.finditer(body_no_code):
        token = match.group(1)
        if token in VERIFIED_UPPERCASE_ENUMS or token in ALLOWED_UPPERCASE_SHORTHANDS:
            continue
        errors.append(
            f"{rel}: unverified uppercase enum/token `{token}` "
            "(not in verified Investminder MCP enum whitelist)"
        )
    return errors


def validate_markdown_links(md_files: list[Path]) -> list[str]:
    errors: list[str] = []
    for md in md_files:
        rel = md.relative_to(ROOT).as_posix()
        text = md.read_text(encoding="utf-8")
        # Ignore fenced code blocks
        text_no_code = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        for match in MD_LINK_RE.finditer(text_no_code):
            target = match.group(1).strip()
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_part = target.split("#", 1)[0].strip()
            if not path_part:
                continue
            resolved = (md.parent / path_part).resolve()
            if not resolved.exists():
                errors.append(f"{rel}: broken relative link -> '{target}'")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate investminder/mcp Agent Skills.")
    parser.add_argument(
        "--check-mcp-tools",
        action="store_true",
        help="Verify all backticked MCP tool references match the investminder/mcp inventory.",
    )
    args = parser.parse_args()

    errors: list[str] = []

    if not SKILLS_DIR.is_dir():
        print("ERROR: skills/ directory not found.", file=sys.stderr)
        return 1

    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        print("ERROR: no skills/*/SKILL.md files found.", file=sys.stderr)
        return 1

    for skill_md in skill_files:
        errors.extend(validate_skill_file(skill_md, check_mcp_tools=args.check_mcp_tools))

    supporting_md_files = sorted(
        list(SKILLS_DIR.glob("*/references/*.md")) + list(SKILLS_DIR.glob("*/assets/*.md"))
    )
    for sup_md in supporting_md_files:
        sup_text = sup_md.read_text(encoding="utf-8")
        if args.check_mcp_tools:
            errors.extend(validate_camel_identifiers(sup_md, sup_text))
        errors.extend(validate_uppercase_enums(sup_md, sup_text))

    md_files = sorted(
        p
        for p in ROOT.rglob("*.md")
        if ".git" not in p.parts and ".agents" not in p.parts and "node_modules" not in p.parts
    )
    errors.extend(validate_markdown_links(md_files))

    if errors:
        print(f"VALIDATION FAILED ({len(errors)} error(s)):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(
        f"VALIDATION PASSED: {len(skill_files)} skills validated, "
        f"{len(md_files)} Markdown files link-checked"
        + (" (MCP tool inventory verified)." if args.check_mcp_tools else ".")
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
