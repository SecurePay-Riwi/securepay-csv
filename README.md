# securepay-csv

CSV data sources for the SecurePay Antifraude project.

## Sources

| ID | Source | Format | Frequency |
|----|--------|--------|-----------|
| F1 | PaySim — Synthetic Financial Datasets For Fraud Detection | CSV Kaggle | Historical |
| F2 | Sparkov — Credit Card Fraud Detection (`fraudTest.csv`) | CSV Kaggle | Historical |
| F5 | Partner payment statements (banks / correspondents) | CSV/TXT fixed-width | Daily |

> **Note:** F2 originally used `mlg-ulb/creditcardfraud`. The team replaced it with
> `kartik2112/fraud-detection` (`fraudTest.csv`) after agreement with the professor,
> because the anonymous V1..V28 columns of the original dataset cannot support real antifraud rules.

## Setup

```bash
git clone https://github.com/SecurePay-Riwi/securepay-csv.git
cd securepay-csv
cp .env.example .env   # fill in your credentials
uv sync
```

## Usage

```bash
# Download and load Kaggle datasets
uv run python -m kaggle.download
uv run python -m kaggle.load

# Process partner statements
uv run python -m partner_statements.process
```

## Dependencies

- [`securepay-shared`](https://pypi.org/project/securepay-shared/) — shared models, DB and config
