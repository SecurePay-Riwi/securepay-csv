# AGENTS.md: securepay-csv

Context for AI assistants and new contributors. Keep it short; the full
documentation is at https://securepay-riwi.github.io/SecurePay/.

## What this repository is

File sources: downloads the Kaggle datasets (PaySim and Sparkov fraudTest) and uploads them to the Data Lake, and builds the daily partner statements from the generator output.

It is one of the SecurePay-Riwi repositories. The others are securepay-seed,
securepay-generator, securepay-csv and securepay-apis (simulated data sources)
and SecurePay (decision engine, consumers, infrastructure, documentation).

## Commands

Run everything from the repository root.

```bash
uv sync                 # install (Python 3.12, securepay-shared from PyPI)
uv run pytest           # tests; they need no database, internet or LocalStack
uv run python -m securepay_csv.kaggle_datasets       # needs KAGGLE_API_TOKEN
uv run python -m securepay_csv.partner_statements    # needs the generator output
```

## Structure rules (mandatory)

Follow these rules for every change. If a change seems to need breaking one,
stop and ask instead of working around it.

1. All code lives in the single package `src/securepay_csv/`. Do not add top-level
   Python folders or a second package.
2. Each component is a subpackage of `securepay_csv`. A new component gets its own
   subpackage, with an entry point in `__main__.py` when it is run with
   `python -m`.
3. Tests live in `tests/`, mirroring the subpackages (`tests/<component>/`).
   Never put tests inside `src/`.
4. Imports are absolute and start with `securepay_csv` or `securepay_shared`.
   Never import code from another SecurePay repository and never copy
   `securepay_shared` code here: add what is missing to that package instead.
5. Repositories exchange data only through files or S3, never through imports.
   A path to another repository is a default that an environment variable can
   override (for example `../securepay-generator/generated`).
6. Generated data and downloads (`generated/`, `data/`) are never committed.
7. Dependencies are managed only with uv (`uv add`, `uv add --dev`); commit
   `pyproject.toml` and `uv.lock` together.
8. Every environment variable the code reads is listed in `.env.example`, and
   `.env.example` lists nothing the code does not read.
9. When a command, variable or folder changes, update README.md and this file
   in the same change.

## Conventions

- Commit messages and pull requests in English, conventional commits
  (`feat:`, `fix:`, `refactor:`, `docs:`, `build:`, `chore:`).
- Existing Spanish names and comments stay; translate them only when editing
  that code anyway. Database table and column names stay as they are.
- Reproducibility: `SEED=42` and `FECHA_REFERENCIA=2026-10-01` (from
  `securepay_shared.config`) must give the same data on Windows and Linux.

## Known traps

- The package is `kaggle_datasets`, not `kaggle`: a local `kaggle` package
  hides the `kaggle` library and the download breaks.
- `kaggle` is imported inside the download function on purpose: the library
  tries to authenticate on import and would break the tests without a token.
- `partner_statements/money.py` is a small copy of the generator's rounding,
  so this repo does not depend on securepay-generator.
- `extracts_report.json` is the answer key of the reconciliation; keep its
  format stable.

## Where to read more

Read these before changing the design, not to work on the code:

- Architecture overview: https://securepay-riwi.github.io/SecurePay/docs/architecture/overview
- Decisions (ADRs): https://securepay-riwi.github.io/SecurePay/docs/architecture/decisions
- Team decisions: https://securepay-riwi.github.io/SecurePay/docs/architecture/team-decisions
- Open questions: https://securepay-riwi.github.io/SecurePay/docs/architecture/open-questions
- Data flow: https://securepay-riwi.github.io/SecurePay/docs/architecture/data-flow
- Logbook: https://securepay-riwi.github.io/SecurePay/docs/logbook
- Kaggle datasets: https://securepay-riwi.github.io/SecurePay/docs/components/kaggle-datasets
- Partner statements: https://securepay-riwi.github.io/SecurePay/docs/components/partner-statements
