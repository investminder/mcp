# Prompt recipes for the Investminder MCP server

Ready-to-use prompts for Claude, ChatGPT, Cursor and any MCP client connected to [Investminder](https://www.investminder.com). Copy, adapt the tickers and amounts, and go.

Back to the [README](../README.md).

---

## 1. First steps

```text
Start the Investminder onboarding. I live in France and I invest in euros.
```

```text
Based on my investor profile, show me the 3 pre-built strategies that fit me best and explain the difference in plain words.
```

## 2. Research a stock or an ETF

```text
Find the ETFs that track the MSCI World and are eligible for the French PEA. Compare fees, distribution policy and 3-year performance in a table.
```

```text
Analyze Novo Nordisk: 10 years of yearly revenue, net margin and free cash flow, dividend history, and where the RSI 14 and the 200-day moving average stand today.
```

## 3. Screen the market

```text
Screen S&P 500 stocks with ROIC above 15 %, debt/equity below 1, revenue growth above 8 % a year and a PEG below 2. Show the 15 best with a one-line description each.
```

```text
Find European dividend stocks with a yield above 4 % and a payout ratio below 70 %, then flag the ones whose 12-month performance is negative.
```

## 4. Check diversification

```text
Compute the correlation matrix of SPY, QQQ, EFA, EEM, TLT, GLD and DBC over the last 10 years. Which pairs really diversify each other, and which are redundant?
```

## 5. Build and backtest a strategy

**A classic 60/40, rebalanced**

```text
Create a REBALANCED strategy in EUR: 60 % VWCE.DE, 40 % EUNA.DE, commission 0.1 %, benchmark SPY. Then backtest it from 2015 with €10,000 and €200 a month. Summarize CAGR, volatility, max drawdown and the worst year.
```

**Trend following on a broad index**

```text
Create a PROGRESSIVE strategy on SPY, max 100 %: buy when the price crosses above its SMA 200, sell when it crosses below. Park the cash in a money-market ETF. Backtest from 2000 with $10,000 and compare with buy-and-hold SPY.
```

Read the theory first: [How to Design a Trend Following Strategy on Broad Index ETFs](https://help.investminder.com/en/investment-academy/how-to-design-a-trend-following-strategy-on-broad-index-etfs-1boglwz/).

**Buy the dip with value averaging**

```text
Create a PROGRESSIVE strategy on QQQ capped at 100 %: buy when RSI 14 drops below 35, in 4 tranches, each tranche requiring an RSI 5 points lower. Never sell. Backtest from 2012 with $20,000.
```

**Start from the catalog**

```text
Read the pre-built dividend-focused strategies, pick the most diversified one, swap any non-UCITS ETF for a UCITS equivalent, and backtest the copy from 2016 in EUR.
```

Learn more: [How to Design a Dividend ETF Strategy](https://help.investminder.com/en/investment-academy/how-to-design-a-dividend-etf-strategy-u55edq/) · [How to design a Growth ETF Strategy](https://help.investminder.com/en/investment-academy/how-to-design-a-growth-etf-strategy-vo27dy/).

## 6. Plan withdrawals

```text
Backtest my strategy from 2000 with €300,000, no contributions, withdrawing 4 % a year starting after 1 year. Does the capital survive? What was the lowest point?
```

## 7. Track your portfolio

```text
Create a EUR portfolio called "PEA". Deposit €5,000, then record 6 shares of CW8.PA at €520 and 20 shares of PAEEM.PA at €27, no commission. Show me the result.
```

```text
Connect my brokerage account to Investminder.
```

```text
Show all my portfolios with their positions and cash, and tell me how far each one is from my strategy's target weights.
```

---

> Investminder provides data and simulations, not investment advice. Backtests do not guarantee future results.
