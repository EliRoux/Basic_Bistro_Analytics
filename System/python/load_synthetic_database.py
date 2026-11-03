
import sys
import pandas as pd
from pathlib import Path
from psycopg import sql
import os
import psycopg
from dotenv import load_dotenv


# ---------------------------------------------------------
# Project root
# ---------------------------------------------------------

if getattr(sys, "frozen", False):
    PROJECT_ROOT = Path(sys.executable).resolve().parent.parent
else:
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Load credentials without changing the configured database name.
load_dotenv(PROJECT_ROOT / ".env")


def get_connection():
    """Connect explicitly to the synthetic database."""

    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname="basic_bistro_synthetic",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

# ---------------------------------------------------------
# File locations
# ---------------------------------------------------------

PROCESSED_DIR = PROJECT_ROOT / "System" / "data" / "synthetic"


# ---------------------------------------------------------
# CSV files
# ---------------------------------------------------------

FILES = {
    "product_sales": PROCESSED_DIR / "product_sales.csv",
    "daily_turnover": PROCESSED_DIR / "daily_turnover.csv",
    "sales_invoices": PROCESSED_DIR / "sales_invoices.csv",
    "sales_exceptions": PROCESSED_DIR / "clean_sales_exceptions.csv",
}


# ---------------------------------------------------------
# Table definitions
# ---------------------------------------------------------

TABLES = {

    "product_sales": """
        CREATE TABLE IF NOT EXISTS product_sales (
            id SERIAL PRIMARY KEY,
            sale_datetime TIMESTAMP NOT NULL,
            department TEXT NOT NULL,
            product_code TEXT NOT NULL,
            product_name TEXT NOT NULL,
            sold_qty INTEGER NOT NULL,
            total_sales NUMERIC(12,2) NOT NULL
        );
    """,

    "daily_turnover": """
        CREATE TABLE IF NOT EXISTS daily_turnover (
            sale_date DATE PRIMARY KEY,
            cash NUMERIC(12,2),
            credit_card NUMERIC(12,2),
            accounts NUMERIC(12,2),
            cheque NUMERIC(12,2),
            non_turnover NUMERIC(12,2),
            tips NUMERIC(12,2),
            total_sales NUMERIC(12,2),
            sales_rounding NUMERIC(12,2),
            turnover_incl NUMERIC(12,2),
            tax NUMERIC(12,2),
            turnover_excl NUMERIC(12,2),
            invoice_count INTEGER
        );
    """,

    "sales_invoices": """
        CREATE TABLE IF NOT EXISTS sales_invoices (
            id SERIAL PRIMARY KEY,
            sale_datetime TIMESTAMP NOT NULL,
            invoice_number TEXT NOT NULL UNIQUE,
            exclusive NUMERIC(12,2),
            inclusive NUMERIC(12,2),
            employee TEXT,
            tax NUMERIC(12,2),
            recorded_datetime TIMESTAMP,
            cash NUMERIC(12,2),
            credit_card NUMERIC(12,2),
            accounts NUMERIC(12,2),
            cheque NUMERIC(12,2),
            non_turnover NUMERIC(12,2)
        );
    """,

    "sales_exceptions": """
        CREATE TABLE IF NOT EXISTS sales_exceptions (
            id SERIAL PRIMARY KEY,
            exception_type TEXT NOT NULL,
            name TEXT,
            qty NUMERIC(12,2),
            table_number TEXT,
            invoice_number TEXT NOT NULL,
            exception_datetime TIMESTAMP NOT NULL,
            date DATE NOT NULL,
            value NUMERIC(12,2),
            invoice_value_before NUMERIC(12,2),
            invoice_value_after NUMERIC(12,2),
            employee TEXT,
            authorized_by TEXT
        );
    """
}


# ---------------------------------------------------------
# View definitions
# ---------------------------------------------------------

VIEWS = {

    "vw_sales_summary": """
        CREATE OR REPLACE VIEW public.vw_sales_summary AS
        SELECT
            count(*) AS trading_days,
            round(sum(turnover_incl), 2) AS total_turnover,
            round(avg(turnover_incl), 2) AS average_daily_turnover,
            round(max(turnover_incl), 2) AS best_day_turnover,
            round(min(turnover_incl), 2) AS worst_day_turnover,
            sum(invoice_count) AS total_invoices,
            round(
                sum(turnover_incl)
                / NULLIF(sum(invoice_count), 0)::numeric,
                2
            ) AS average_invoice_value
        FROM daily_turnover;
    """,

    "vw_daily_sales": """
        CREATE OR REPLACE VIEW public.vw_daily_sales AS
        SELECT
            sale_date,
            round(total_sales::numeric, 2) AS total_sales,
            invoice_count,
            round(
                total_sales
                / NULLIF(invoice_count, 0)::numeric,
                2
            ) AS average_invoice_value,
            TRIM(
                BOTH FROM to_char(
                    sale_date::timestamp with time zone,
                    'Day'::text
                )
            ) AS day_of_week,
            EXTRACT(isodow FROM sale_date) AS day_number
        FROM daily_turnover
        ORDER BY sale_date;
    """,

    "vw_department_performance": """
        CREATE OR REPLACE VIEW public.vw_department_performance AS
        SELECT
            department,
            sum(sold_qty) AS units_sold,
            round(sum(total_sales), 2) AS total_sales,
            count(DISTINCT product_name) AS unique_products,
            round(
                sum(total_sales)
                / NULLIF(sum(sold_qty), 0)::numeric,
                2
            ) AS average_revenue_per_unit,
            round(
                sum(total_sales)
                / NULLIF(
                    sum(sum(total_sales)) OVER (),
                    0::numeric
                ) * 100::numeric,
                2
            ) AS revenue_percentage
        FROM product_sales
        WHERE department <> 'PREPSCREENS'::text
        GROUP BY department
        HAVING sum(total_sales) > 0::numeric
        ORDER BY round(sum(total_sales), 2) DESC;
    """,

    "vw_product_performance": """
        CREATE OR REPLACE VIEW public.vw_product_performance AS
        SELECT
            product_name,
            department,
            sum(sold_qty) AS units_sold,
            round(sum(total_sales), 2) AS total_sales,
            round(
                sum(total_sales)
                / NULLIF(sum(sold_qty), 0)::numeric,
                2
            ) AS average_revenue_per_unit,
            round(
                sum(total_sales)
                / NULLIF(
                    sum(sum(total_sales)) OVER (),
                    0::numeric
                ) * 100::numeric,
                2
            ) AS revenue_percentage
        FROM product_sales
        WHERE department <> 'PREPSCREENS'::text
        GROUP BY product_name, department
        HAVING sum(total_sales) > 0::numeric
        ORDER BY round(sum(total_sales), 2) DESC;
    """,

    "vw_payment_methods": """
        CREATE OR REPLACE VIEW public.vw_payment_methods AS
        SELECT
            round(sum(cash), 2) AS total_cash,
            round(sum(credit_card), 2) AS total_credit_card,
            round(sum(accounts), 2) AS total_accounts,
            round(sum(cheque), 2) AS total_cheque,
            round(sum(non_turnover), 2) AS total_non_turnover,
            round(
                sum(cash)
                / NULLIF(sum(inclusive), 0::numeric)
                * 100::numeric,
                2
            ) AS cash_percentage,
            round(
                sum(credit_card)
                / NULLIF(sum(inclusive), 0::numeric)
                * 100::numeric,
                2
            ) AS credit_card_percentage,
            round(
                sum(accounts)
                / NULLIF(sum(inclusive), 0::numeric)
                * 100::numeric,
                2
            ) AS accounts_percentage,
            round(
                sum(cheque)
                / NULLIF(sum(inclusive), 0::numeric)
                * 100::numeric,
                2
            ) AS cheque_percentage,
            round(
                sum(non_turnover)
                / NULLIF(sum(inclusive), 0::numeric)
                * 100::numeric,
                2
            ) AS non_turnover_percentage
        FROM sales_invoices;
    """,

    "vw_product_sales_analysis": """
        CREATE OR REPLACE VIEW public.vw_product_sales_analysis AS
        SELECT
            sale_datetime,
            sale_datetime::date AS sale_date,
            sale_datetime::time without time zone AS sale_time,
            EXTRACT(hour FROM sale_datetime)::integer AS sale_hour,
            EXTRACT(dow FROM sale_datetime)::integer AS day_of_week_number,
            TRIM(
                BOTH FROM to_char(sale_datetime, 'Day'::text)
            ) AS day_of_week,
            EXTRACT(month FROM sale_datetime)::integer AS month_number,
            TRIM(
                BOTH FROM to_char(sale_datetime, 'Month'::text)
            ) AS month_name,
            EXTRACT(year FROM sale_datetime)::integer AS year,
            CASE
                WHEN EXTRACT(month FROM sale_datetime)
                    = ANY (ARRAY[12::numeric, 1::numeric, 2::numeric])
                    THEN 'Summer'::text

                WHEN EXTRACT(month FROM sale_datetime)
                    = ANY (ARRAY[3::numeric, 4::numeric, 5::numeric])
                    THEN 'Autumn'::text

                WHEN EXTRACT(month FROM sale_datetime)
                    = ANY (ARRAY[6::numeric, 7::numeric, 8::numeric])
                    THEN 'Winter'::text

                WHEN EXTRACT(month FROM sale_datetime)
                    = ANY (ARRAY[9::numeric, 10::numeric, 11::numeric])
                    THEN 'Spring'::text

                ELSE NULL::text
            END AS season,
            department,
            product_code,
            product_name,
            sold_qty,
            total_sales,
            round(
                sum(total_sales) OVER (
                    PARTITION BY product_code
                )
                / NULLIF(
                    sum(total_sales) OVER (),
                    0::numeric
                )
                * 100::numeric,
                2
            ) AS revenue_percentage
        FROM product_sales
        WHERE department <> ALL (
            ARRAY[
                'INGREDIENTS / EXTRAS'::text,
                'PREP SCREEN'::text
            ]
        );
    """
}


# ---------------------------------------------------------
# Create tables
# ---------------------------------------------------------

def create_tables(conn):
    print("\nCreating database tables...")

    with conn.cursor() as cur:
        for table_name, create_statement in TABLES.items():
            cur.execute(create_statement)
            print(f"  ✓ {table_name}")

    conn.commit()


# ---------------------------------------------------------
# Load Product Sales
# ---------------------------------------------------------

def load_product_sales(conn):
    file = FILES["product_sales"]

    print(f"\nLoading {file.name}...")

    df = pd.read_csv(file)

    with conn.cursor() as cur:

        cur.execute("TRUNCATE TABLE product_sales RESTART IDENTITY;")

        records = [
            (
                row.sale_datetime,
                row.department,
                row.product_code,
                row.product_name,
                int(row.sold_qty),
                float(row.total_sales)
            )
            for row in df.itertuples(index=False)
        ]

        cur.executemany(
            """
            INSERT INTO product_sales
            (
                sale_datetime,
                department,
                product_code,
                product_name,
                sold_qty,
                total_sales
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            records
        )

    conn.commit()

    print(f"  ✓ Loaded {len(df):,} rows")


# ---------------------------------------------------------
# Load Daily Turnover
# ---------------------------------------------------------

def load_daily_turnover(conn):
    file = FILES["daily_turnover"]

    print(f"\nLoading {file.name}...")

    df = pd.read_csv(file)

    with conn.cursor() as cur:

        cur.execute("TRUNCATE TABLE daily_turnover;")

        records = []

        for row in df.itertuples(index=False):

            records.append(
                (
                    row.sale_date,
                    row.cash,
                    row.credit_card,
                    row.accounts,
                    row.cheque,
                    row.non_turnover,
                    row.tips,
                    row.total_sales,
                    row.sales_rounding,
                    row.turnover_incl,
                    row.tax,
                    row.turnover_excl,
                    int(row.invoice_count)
                )
            )

        cur.executemany(
            """
            INSERT INTO daily_turnover
            (
                sale_date,
                cash,
                credit_card,
                accounts,
                cheque,
                non_turnover,
                tips,
                total_sales,
                sales_rounding,
                turnover_incl,
                tax,
                turnover_excl,
                invoice_count
            )
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            records
        )

    conn.commit()

    print(f"  ✓ Loaded {len(df):,} rows")


# ---------------------------------------------------------
# Load Sales Invoices
# ---------------------------------------------------------

def load_sales_invoices(conn):
    file = FILES["sales_invoices"]

    print(f"\nLoading {file.name}...")

    df = pd.read_csv(file)

    with conn.cursor() as cur:

        cur.execute("TRUNCATE TABLE sales_invoices RESTART IDENTITY;")

        records = []

        for row in df.itertuples(index=False):

            records.append(
                (
                    row.sale_datetime,
                    row.invoice_number,
                    row.exclusive,
                    row.inclusive,
                    row.employee,
                    row.tax,
                    row.recorded_datetime,
                    row.cash,
                    row.credit_card,
                    row.accounts,
                    row.cheque,
                    row.non_turnover
                )
            )

        cur.executemany(
            """
            INSERT INTO sales_invoices
            (
                sale_datetime,
                invoice_number,
                exclusive,
                inclusive,
                employee,
                tax,
                recorded_datetime,
                cash,
                credit_card,
                accounts,
                cheque,
                non_turnover
            )
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            records
        )

    conn.commit()

    print(f"  ✓ Loaded {len(df):,} rows")


# ---------------------------------------------------------
# Load Sales Exceptions
# ---------------------------------------------------------

def load_sales_exceptions(conn):
    file = FILES["sales_exceptions"]

    print(f"\nLoading {file.name}...")

    df = pd.read_csv(file)

    with conn.cursor() as cur:

        cur.execute("TRUNCATE TABLE sales_exceptions RESTART IDENTITY;")

        records = []

        for row in df.itertuples(index=False):

            records.append(
                (
                    row.exception_type,
                    row.name,
                    row.qty,
                    row.table_number,
                    row.invoice_number,
                    row.exception_datetime,
                    row.date,
                    row.value,
                    row.invoice_value_before,
                    row.invoice_value_after,
                    row.employee,
                    row.authorized_by
                )
            )

        cur.executemany(
            """
            INSERT INTO sales_exceptions
            (
                exception_type,
                name,
                qty,
                table_number,
                invoice_number,
                exception_datetime,
                date,
                value,
                invoice_value_before,
                invoice_value_after,
                employee,
                authorized_by
            )
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            records
        )

    conn.commit()

    print(f"  ✓ Loaded {len(df):,} rows")


# ---------------------------------------------------------
# Create PostgreSQL Views
# ---------------------------------------------------------

def create_views(conn):
    print("\nCreating PostgreSQL views...")

    with conn.cursor() as cur:

        for view_name, create_statement in VIEWS.items():

            cur.execute(create_statement)

            print(f"  ✓ {view_name}")

    conn.commit()


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------

def validate_database(conn):

    print("\nDatabase validation:")

    tables = [
        "product_sales",
        "daily_turnover",
        "sales_invoices",
        "sales_exceptions"
    ]

    with conn.cursor() as cur:

        for table in tables:

            cur.execute(
                sql.SQL("SELECT COUNT(*) FROM {}").format(
                    sql.Identifier(table)
                )
            )

            count = cur.fetchone()[0]

            print(f"  {table}: {count:,} rows")


# ---------------------------------------------------------
# Validate Views
# ---------------------------------------------------------

def validate_views(conn):

    print("\nView validation:")

    views = [
        "vw_sales_summary",
        "vw_daily_sales",
        "vw_department_performance",
        "vw_product_performance",
        "vw_payment_methods",
        "vw_product_sales_analysis"
    ]

    with conn.cursor() as cur:

        for view in views:

            cur.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.views
                    WHERE table_schema = 'public'
                    AND table_name = %s
                );
                """,
                (view,)
            )

            exists = cur.fetchone()[0]

            if not exists:
                raise RuntimeError(
                    f"Required view was not created: {view}"
                )

            print(f"  ✓ {view}")


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------


def main():

    print("Connecting to PostgreSQL...")

    conn = get_connection()

    try:

        # Safety check: never load into the original database.
        with conn.cursor() as cur:
            cur.execute("SELECT current_database();")
            target_database = cur.fetchone()[0]

        if target_database != "basic_bistro_synthetic":
            raise RuntimeError(
                f"Unsafe database target: {target_database}. "
                "Expected basic_bistro_synthetic. No data was loaded."
            )

        print(f"✓ Connected to {target_database}")

        create_tables(conn)

        load_product_sales(conn)
        load_daily_turnover(conn)
        load_sales_invoices(conn)
        load_sales_exceptions(conn)

        create_views(conn)

        validate_database(conn)
        validate_views(conn)

        print("\n===================================")
        print("Synthetic database loading completed!")
        print("===================================")

    except Exception as error:

        conn.rollback()

        print("\nERROR:")
        print(error)

        raise

    finally:

        conn.close()

        print("\nDatabase connection closed.")


if __name__ == "__main__":
    main()
