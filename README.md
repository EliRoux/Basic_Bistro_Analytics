# Basic Bistro Analytics â€” public synthetic portfolio

This portfolio project demonstrates restaurant sales analytics using fictional sales data, PostgreSQL, Python, SQL, and Power BI. The public workflow operates entirely on synthetic datasets and does not require access to original business records.

## Public workflow

1. Install Python 3.11+ and PostgreSQL. Create a virtual environment and install `pip install -r requirements-public.txt`.
2. Create a local `.env` from `.env.example`, using your own PostgreSQL credentials. Never commit `.env`.
3. Create the separate database once: `psql -U postgres -c "CREATE DATABASE basic_bistro_synthetic;"` (skip if it already exists).
4. Run `python System/python/run_public_pipeline.py` or `RUN_PUBLIC_PIPELINE.bat`.
5. To build or connect a Power BI dashboard, connect Power BI Desktop to the PostgreSQL database `basic_bistro_synthetic` and import the analytical views. The local `.pbix` dashboard file is excluded from this repository.

The generator reads the bundled synthetic CSVs as reference inputs and produces fictional transactions. It does not access private processed exports or connect to the original business database. The public pipeline regenerates synthetic CSVs before loading them. Use `--skip-generate` to load the existing synthetic CSVs without regenerating them.

## Analytics

PostgreSQL views created by the loader: `vw_sales_summary`, `vw_daily_sales`, `vw_department_performance`, `vw_product_performance`, `vw_payment_methods`, `vw_product_sales_analysis`. SQL analysis files are in `System/sql/`. Connect Power BI to the synthetic database and verify all query sources point there.

## Security and publishing

Only `System/data/synthetic/*.csv` is eligible for CSV tracking. The original source files, `.env`, Git metadata, local executables, build output, and PBIX are excluded. A `.gitignore` does not remove anything already committed: inspect `git ls-files`, `git log --all --name-only`, and `git status` before pushing. If credentials or confidential exports were ever committed, rotate credentials and clean Git history before publication. **No formal privacy guarantee** can be made about synthetic data derived from private distributions without a separate disclosure review.

## Verification

Run `python -m compileall -q System/python`, `python System/python/run_public_pipeline.py --skip-generate`, then in PostgreSQL run `SELECT current_database(); SELECT COUNT(*) FROM public.sales_invoices; SELECT * FROM public.vw_sales_summary;`. The PostgreSQL step requires a running local server and valid `.env` credentials.
