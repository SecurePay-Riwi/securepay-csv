# securepay-csv

File sources for the SecurePay Antifraude project.

| Source | Type |
|--------|------|
| PaySim, synthetic mobile money transactions | CSV from Kaggle (`ealaxi/paysim1`) |
| Sparkov fraudTest, labeled card transactions | CSV from Kaggle (`kartik2112/fraud-detection`) |
| Daily partner statements (4 payment partners) | CSV / fixed-width TXT generated locally |

> The original project spec listed `mlg-ulb/creditcardfraud` (`creditcard.csv`).
> The team replaced it with `kartik2112/fraud-detection` after agreeing with the
> professor: the anonymous V1..V28 columns cannot support real antifraud rules.

## Setup

```bash
git clone https://github.com/SecurePay-Riwi/securepay-csv.git
cd securepay-csv
cp .env.example .env   # set KAGGLE_API_TOKEN
uv sync                # installs securepay-shared from PyPI
```

## Local services

PostgreSQL (port 5433) and LocalStack run with the Docker Compose of the
[SecurePay](https://github.com/SecurePay-Riwi/SecurePay) repository (`docker compose up -d`).
LocalStack is needed to upload to the Data Lake (`EXT_OUTPUT=s3` and the Kaggle upload).

## Usage

```bash
# Download PaySim and fraudTest from Kaggle and upload them to the Data Lake
uv run python -m securepay_csv.kaggle_datasets

# Build the daily partner statements from the generator output
uv run python -m securepay_csv.partner_statements

# Run the tests (no internet or real CSVs needed)
uv run pytest
```

### Kaggle datasets

The CSVs are large and are **never committed**. They are downloaded to
`data/kaggle/` (`KAGGLE_DOWNLOAD_DIR`, Git-ignored) and uploaded to
`raw/kaggle/` in the Data Lake bucket. **securepay-seed** reads the same folder
when it is cloned next to this repository.

| File | Kaggle dataset | Size |
|------|----------------|------|
| `PS_20174392719_1491204439457_log.csv` | [ealaxi/paysim1](https://www.kaggle.com/datasets/ealaxi/paysim1) | ~470 MB |
| `fraudTest.csv` | [kartik2112/fraud-detection](https://www.kaggle.com/datasets/kartik2112/fraud-detection) | ~150 MB |

### Partner statements

They are built from the generator output (`generated/instance-*/events.jsonl`),
looked up here and in `../securepay-generator/generated/`, so they match what
the engine saw. Each partner sends one file per day in its own format, with the
defects the spec asks for. The files go to `generated/extractos/`, together with
`extracts_report.json`, the answer key for the reconciliation.

## Repository layout

```
src/securepay_csv/
├── kaggle_datasets/      # Kaggle download + upload: python -m securepay_csv.kaggle_datasets
└── partner_statements/   # daily statements: python -m securepay_csv.partner_statements
tests/
├── kaggle_datasets/
└── partner_statements/
```

All code lives in one package under `src/`; tests mirror it under `tests/`.
Read [AGENTS.md](AGENTS.md) before adding folders or modules.

## Working with the other repositories

The repositories pass data through files (and through S3 in AWS), never through
imports. Clone them side by side in the same folder and each one finds the files
the others produce, without setting paths by hand:

```
SecurePay-Riwi/
├── securepay-seed/        # PostgreSQL master data + restricted list export
├── securepay-generator/   # reads the seed, writes generated/instance-*/
├── securepay-csv/         # Kaggle downloads + partner statements (reads the generator)
└── securepay-apis/        # restricted-list service (reads the seed export)
```

Environment variables still override every path (see `.env.example`).


## Docker image (MAG-31)

Build the Python 3.12/uv image from this repository root. It installs locked production dependencies and runs partner-statement generation by default.

```bash
docker build -t securepay-csv .
docker run --rm --env-file .env securepay-csv
```

For the complete local environment, use Docker Compose in the `SecurePay` repository. It configures the shared generated-data volume and LocalStack access. Kaggle downloads are optional and require `KAGGLE_API_TOKEN`.
