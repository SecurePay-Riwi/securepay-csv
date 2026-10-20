# securepay-csv

CSV data sources for the SecurePay Antifraude project.

## Data sources

| ID | Source | Type |
|----|--------|------|
| F1 | PaySim — synthetic financial transactions | CSV from Kaggle (`ealaxi/paysim1`) |
| F2 | Sparkov fraudTest — labeled card fraud transactions | CSV from Kaggle (`kartik2112/fraud-detection`) |
| F5 | Partner payment statements | Fixed-width TXT / CSV generated locally |

> **F2 note:** The original project spec listed `mlg-ulb/creditcardfraud` (`creditcard.csv`).
> The team replaced it with `kartik2112/fraud-detection` (`fraudTest.csv`) after agreement
> with the professor — the anonymous V1..V28 columns cannot support real antifraud rules.

## Setup

```bash
git clone https://github.com/SecurePay-Riwi/securepay-csv.git
cd securepay-csv
cp .env.example .env   # fill in your credentials
uv sync                # installs securepay-shared from PyPI automatically
```

## Required CSV files

The Kaggle CSVs are large and are **not committed to Git**. Download them and place
them in `data/kaggle/`:

| File | Kaggle dataset | Size |
|------|----------------|------|
| `PS_20174392719_1491204439457_log.csv` | [ealaxi/paysim1](https://www.kaggle.com/datasets/ealaxi/paysim1) | ~470 MB |
| `fraudTest.csv` | [kartik2112/fraud-detection](https://www.kaggle.com/datasets/kartik2112/fraud-detection) | ~150 MB |

## Usage

```bash
# Upload PaySim and fraudTest to the Data Lake (LocalStack)
uv run python -m sources.csv_files.kaggle

# Generate partner payment statements
uv run python -m sources.csv_files.partner_statements

# Run tests (no internet or real CSVs needed)
uv run pytest
```

## Dependencies

- [`securepay-shared`](https://pypi.org/project/securepay-shared/) — shared models, DB and config
- LocalStack running locally for S3 upload steps (see monorepo `infra/`)
