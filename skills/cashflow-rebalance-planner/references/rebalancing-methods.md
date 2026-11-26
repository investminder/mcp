# Rebalancing Methods & Multi-Currency Hygiene

Use this reference when explaining allocation drift and cashflow-only scenarios in `cashflow-rebalance-planner`.

## 1. Cashflow-Only Rebalancing (No Sells)

- **Mechanism:** Direct incoming savings (monthly deposit, dividend cash balance) exclusively to underweight assets — starting with the most underweight asset or proportionally across underweight gaps.
- **Advantages:** Avoids selling winners, which can reduce brokerage commissions and avoid triggering taxable capital-gains events in taxable accounts (e.g., French CTO or US brokerage accounts).
- **Limitation:** When a portfolio becomes large relative to monthly deposits, fresh cash alone may no longer eliminate large drift after a major market rally or crash.

## 2. Full Target Rebalancing (Reference Calculation)

- **Mechanism:** Computes the exact positive and negative monetary gaps required so every holding equals its exact `percentTarget`.
- **Trade-Offs:** Restores target risk immediately, but incurs commissions, bid-ask spreads, and potential capital-gains taxes in taxable wrappers (whereas tax-sheltered wrappers like a French **PEA** or retirement accounts generally do not trigger tax on internal switches).

## 3. Tolerance Bands (Avoiding Over-Trading)

Small daily drift (`1–2 pp`) is normal market noise. Investors often use objective thresholds to decide whether drift is material:
- **Absolute band:** e.g., flag drift exceeding `±5 percentage points` from target weight.
- **Relative band (5/25 rule):** flag drift exceeding `±5 pp` OR `±25%` of the asset's target weight (whichever is smaller — e.g., a `10%` gold sleeve triggers at `7.5%` or `12.5%`).

## 4. Multi-Currency & Unit Hygiene (`listPortfolios`)

- `listPortfolios` stores each position and cash balance in its **native currency** with **no automatic FX conversion**.
- **`GBX` means British pence** (`100 GBX = 1 GBP`), never pounds sterling.
- Never add `EUR`, `USD`, `GBP`, and `CHF` values together without flagging the currency boundary and confirming explicit FX rates with the user.
- If `priceLast` is `null` or `tickerRecognized` is `false`, exclude that line from automated weight totals and list it separately.
