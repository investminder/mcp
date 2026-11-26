# Investminder MCP Server & Agent Skills (Français)

[![MCP](https://img.shields.io/badge/MCP-remote%20server-6E56CF)](https://modelcontextprotocol.io)
[![Transport](https://img.shields.io/badge/transport-Streamable%20HTTP-0A7EA4)](README.md#connection-details)
[![Auth](https://img.shields.io/badge/auth-OAuth-2EA44F)](README.md#authentication-and-security)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-agentskills.io-6E56CF)](#agent-skills)
[![Website](https://img.shields.io/badge/website-investminder.com-111111)](https://www.investminder.com)

> **English:** [Read the English version (README.md)](README.md)

**[Investminder](https://www.investminder.com)** est une plateforme indépendante de stratégies d'investissement pour investisseurs particuliers. Ce dépôt réunit la documentation et les manifestes du **serveur MCP Investminder** (`https://api.investminder.com/mcp`) ainsi que le pack officiel d'**[Agent Skills](https://agentskills.io)** (`skills/`) pour en exploiter tout le potentiel quantitatif dans Claude, Claude Code, ChatGPT, Cursor ou Cline — sans calcul mental approximatif et dans un cadre strict d'aide à la décision.

```text
https://api.investminder.com/mcp
```

---

## Démarrage rapide

### 1. Connecter le serveur MCP Investminder

Une seule URL distante (Streamable HTTP + OAuth), **aucune installation locale, aucune clé API** :

- **Claude** (web, desktop, mobile) : ajoutez **[Investminder depuis le répertoire Claude](https://claude.ai/directory/investminder)**.
- **Claude Code** : `claude mcp add --transport http investminder https://api.investminder.com/mcp`
- **ChatGPT** (web) : dans [Plugins](https://chatgpt.com/plugins), cliquez sur **+ → Add custom MCP server** avec l'URL `https://api.investminder.com/mcp` et l'authentification **OAuth**.
- **Cursor / Cline** : configurez le serveur distant Streamable HTTP `https://api.investminder.com/mcp` (OAuth).

Guide détaillé par client et dépannage : [docs/clients.md](docs/clients.md).

### 2. Installer les Agent Skills

```bash
npx skills add investminder/mcp
```

---

## Prompts MCP

Le serveur expose cinq prompts MCP guidés qui s'adaptent à votre compte (les étapes de données de marché fonctionnent sans profil Investminder, puis le prompt propose de créer un compte Basic gratuit lorsque le workflow en a besoin) :

| Prompt | Rôle | Argument optionnel |
|---|---|---|
| `onboarding` | Introduction guidée : profil, quiz de 4 questions, stratégies pré-construites recommandées et premier pas (existe aussi comme outil `startOnboarding`). | Aucun |
| `audit-portfolio` | Audit quantitatif d'un fichier Excel/CSV ou d'un portefeuille Investminder : corrélations, volatilité et drawdown sur 12 mois, ETF UCITS/PEA alternatifs et backtest de l'allocation. | Aucun |
| `backtest-strategy` | Traduit une thèse ou une stratégie du catalogue (avec ses variantes UCITS/PEA) en stratégie, lance un backtest contre un benchmark et produit un pré-mortem. | `thesis` (idée de stratégie ou approche pré-construite de départ) |
| `analyze-stock` | Diagnostic technique (moyennes mobiles, RSI, MACD, volatilité et drawdown 12 mois) et fondamental (états financiers, dividendes, historique du P/E avec un profil Investminder). | `ticker` (nom, ticker ou ISIN) |
| `screen-market` | Screening d'actions et ETF américains et européens (filtres UCITS et PEA), via les presets Investminder ou des critères personnalisés. | Aucun |

- **Claude** (web, desktop et mobile) : lancez un prompt depuis le menu des prompts / connecteurs.
- **Claude Code** : lancez un prompt en commande slash au format `/mcp__investminder__<name>` (par exemple `/mcp__investminder__analyze-stock ASML.AS`).

Les prompts MCP s'affichent uniquement dans les clients MCP qui les prennent en charge ; dans les autres clients, utilisez des requêtes en langage naturel (voir [docs/examples.md](docs/examples.md)). Un prompt lance un workflow guidé en un clic depuis le client, tandis que les [Agent Skills](#agent-skills) ci-dessous guident un assistant qui les a installés (`audit-portfolio` ↔ `excel-to-quant-audit`, `backtest-strategy` ↔ `quant-strategy-backtest`, `analyze-stock` ↔ `technical-regime-check` + `fundamental-quality-xray`, `screen-market` ↔ `securities-screener-workflow`).

---

## Pourquoi dépasser vos fichiers Excel et CSV de suivi de portefeuille ?

Un tableur Excel suit votre prix de revient (PRU) et affiche un camembert d'allocation, mais il ne sait pas mesurer la corrélation réelle entre vos lignes, simuler la perte maximale historique (drawdown) de votre portefeuille ni filtrer des ETF UCITS ou éligibles au PEA moins chargés en frais.

Avec le skill **`excel-to-quant-audit`**, votre assistant IA lit votre fichier `.xlsx` ou `.csv` (exports **BoursoBank**, **DEGIRO**, **Trade Republic**, **Interactive Brokers**, **Saxo**, **Trading 212** ou suivi maison — retirez vos numéros de compte, noms, adresses et identifiants fiscaux **avant** de partager le fichier, car son contenu est transmis au fournisseur de votre assistant IA), omet toute donnée personnelle des appels au serveur MCP Investminder, résout les tickers et codes ISIN officiels, puis exécute les moteurs quantitatifs d'Investminder :

1. **Révéler la concentration cachée** avec `getCorrelationMatrix` (corrélation de Pearson des rendements quotidiens sur 2 à 20 actifs).
2. **Mesurer la volatilité et les drawdowns ligne par ligne** avec `analyzeSecurities` (`volatility12m`, `maxDrawdown12m`, `drawdown`, `TECHNICAL_INDICATORS`).
3. **Filtrer des alternatives UCITS ou éligibles au PEA** avec `screenSecurities` (frais courants `netExpenseRatio`, capitalisation, performance, indice).
4. **Tester votre allocation exacte sur l'historique** avec `createStrategy` + `startBacktest` + `listBacktests` (versements programmés, retraits, commissions).
5. **Migrer hors d'Excel** via une synchronisation bancaire/courtier en lecture seule (`listInstitutions` + `connectPortfolio` via **Powens** 🇪🇺 et **SnapTrade** 🇺🇸) ou un portefeuille manuel Investminder (`createPortfolio` + `addPortfolioPosition`).

---

## Agent Skills

| Skill | Rôle | Outils MCP utilisés |
|---|---|---|
| **[`excel-to-quant-audit`](skills/excel-to-quant-audit/SKILL.md)** | Lit vos fichiers `.xlsx`/`.csv` (BoursoBank, DEGIRO, Trade Republic, IBKR, Saxo, Trading 212 — retirez vos données personnelles avant partage), résout les ISIN/tickers, lance corrélation, volatilité, screening ETF et backtest historique sur l'allocation cible déclarée (`TargetWeightPct` dans [sample-portfolio.csv](skills/excel-to-quant-audit/assets/sample-portfolio.csv)). | `searchSecurities`, `getCorrelationMatrix`, `analyzeSecurities`, `screenSecurities`, `createStrategy`, `startBacktest`, `listBacktests`, `listInstitutions`, `connectPortfolio`, `createPortfolio`, `addPortfolioCash`, `addPortfolioPosition`, `listPortfolios`, `startOnboarding`, `upsertUser` |
| **[`multi-asset-correlation-xray`](skills/multi-asset-correlation-xray/SKILL.md)** | Calcule la matrice de corrélation de Pearson sur 2 à 20 titres/ETF sur plusieurs fenêtres pour détecter les doublons et les vrais diversificateurs. | `searchSecurities`, `getCorrelationMatrix`, `analyzeSecurities`, `screenSecurities`, `listPortfolios` |
| **[`quant-strategy-backtest`](skills/quant-strategy-backtest/SKILL.md)** | Traduit une thèse d'investissement (ou un modèle pré-construit en appliquant ses `variants` officielles UCITS/PEA) en stratégie `REBALANCED`, `PROGRESSIVE` ou `RANKED`, exécute un backtest asynchrone et produit un pré-mortem en 6 points. | `listPreBuiltStrategies`, `listUserStrategies`, `searchSecurities`, `screenSecurities`, `analyzeSecurities`, `createStrategy`, `updateStrategy`, `startBacktest`, `listBacktests`, `publishStrategy`, `linkPortfolioStrategy`, `deleteStrategy`, `getCorrelationMatrix` |
| **[`withdrawal-stress-test`](skills/withdrawal-stress-test/SKILL.md)** | Teste un portefeuille en phase de retraits / retraite / FIRE (`outflowRules`, montant fixe ou pourcentage) face au risque de séquence de rendements (départs 2000, 2008, 2022) via `totalOutflow`, `maxDrawdown` et `annualReturns`. | `listPreBuiltStrategies`, `listUserStrategies`, `searchSecurities`, `analyzeSecurities`, `createStrategy`, `startBacktest`, `listBacktests` |
| **[`fundamental-quality-xray`](skills/fundamental-quality-xray/SKILL.md)** | Audite les états financiers pluriannuels (`YEARLY`/`QUARTERLY`), marges, FCF, dette, régularité des dividendes, historique de P/E et `scoreFinancial.global.score`, avec comparaison aux pairs. | `searchSecurities`, `analyzeSecurities`, `screenSecurities` |
| **[`securities-screener-workflow`](skills/securities-screener-workflow/SKILL.md)** | Filtre actions et ETF européens et américains (S&P 500, Nasdaq-100, MSCI World, STOXX Europe 600, Euro Stoxx 50, CAC 40, DAX, FTSE 100, SMI, IBEX 35, AEX, Nikkei 225) avec filtres `UCITS` et `PEA`. | `listScreeners`, `screenSecurities`, `searchSecurities`, `analyzeSecurities`, `getCorrelationMatrix` |
| **[`technical-regime-check`](skills/technical-regime-check/SKILL.md)** | Diagnostic objectif de tendance (`performance.price` vs. `ema20`, `ema50`, `sma100`, `sma200`), momentum (`rsi14`, `rsi21`, `macd`, `macdSignal`), volatilité (`atr`, `volatility12m`), drawdown, `scoreTechnical.global.score` et `VOLUME_PROFILE`. | `searchSecurities`, `analyzeSecurities`, `screenSecurities`, `getCorrelationMatrix`, `createStrategy`, `startBacktest`, `listBacktests` |
| **[`cashflow-rebalance-planner`](skills/cashflow-rebalance-planner/SKILL.md)** | Analyse la dérive d'allocation face à une stratégie liée ou cible et présente un scénario illustratif de versement selon une règle choisie par l'utilisateur, sans vente. | `listPortfolios`, `listUserStrategies`, `searchSecurities`, `analyzeSecurities`, `linkPortfolioStrategy`, `addPortfolioCash`, `addPortfolioPosition` |
| **[`weekly-quant-brief`](skills/weekly-quant-brief/SKILL.md)** | Compte-rendu hebdomadaire structuré de vos portefeuilles et de votre watchlist : liquidités, opérations des 7 derniers jours, synthèse de dérive d'allocation, régimes techniques et corrélations. | `listPortfolios`, `listPortfolioTransactions`, `listUserStrategies`, `searchSecurities`, `analyzeSecurities`, `getCorrelationMatrix`, `screenSecurities`, `startBacktest` |

### Tester immédiatement avec un exemple

Essayez l'audit sur le portefeuille d'exemple fourni ([`skills/excel-to-quant-audit/assets/sample-portfolio.csv`](skills/excel-to-quant-audit/assets/sample-portfolio.csv)) :

> *« Audite le fichier `skills/excel-to-quant-audit/assets/sample-portfolio.csv` avec `excel-to-quant-audit` : résous les tickers, calcule la matrice de corrélation sur 5 ans, affiche la volatilité et le drawdown sur 12 mois, puis backteste cette allocation depuis 2020 face à SPY. »*

---

## Couverture marchés, sécurité & conformité

- **Places boursières couvertes :** États-Unis (Nasdaq/NYSE), Paris, Francfort, Amsterdam, Londres, Madrid et Zurich, avec éligibilité **UCITS** et **PEA** pour les investisseurs européens.
- **Sécurité bancaire :** ne saisissez jamais vos identifiants bancaires, mots de passe, codes 2FA ou IBAN dans un chat. Les connexions courtiers sont en lecture seule via les pages hébergées de partenaires agréés (**Powens** 🇪🇺 et **SnapTrade** 🇺🇸).
- **Aide à la décision uniquement :** aucun conseil d'achat/vente, aucun objectif de cours, aucun passage d'ordre. Consultez [docs/compliance-guardrails.md](docs/compliance-guardrails.md) et [SECURITY.md](SECURITY.md).

---

## Validation locale & contribution

```bash
python scripts/validate_skills.py --check-mcp-tools
```

Voir [CONTRIBUTING.md](CONTRIBUTING.md) et la licence MIT dans [LICENSE](LICENSE).

<sub>Investminder n'est ni une banque, ni un courtier, ni un conseiller en investissement financier. Contenu fourni à titre informatif et pédagogique uniquement. Les performances passées et les backtests ne préjugent pas des résultats futurs. Investir comporte un risque de perte en capital.</sub>
