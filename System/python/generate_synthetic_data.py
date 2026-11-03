"""
Generate coordinated synthetic data for the Basic Bistro Analytics portfolio.

Reads only the bundled synthetic reference CSVs to learn broad patterns.
It does not read private processed files or connect to PostgreSQL.
The output contains newly generated transactions and fictional identifiers.

Default output:
    System/data/synthetic/
Default synthetic period:
    2026-10-01 through 2026-12-31

Run from the project root:
    python System/python/generate_synthetic_data.py
Optional:
    python System/python/generate_synthetic_data.py --start 2026-10-01 --end 2026-12-31 --seed 42
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import numpy as np
import pandas as pd


# Project root works both when run as a normal Python script and when frozen.
if getattr(sys, "frozen", False):
    PROJECT_ROOT = Path(sys.executable).resolve().parent.parent
else:
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

OUTPUT_DIR = PROJECT_ROOT / "System" / "data" / "synthetic"

def source_files(directory: Path) -> dict[str, Path]:
    return {
        "product_sales": directory / "product_sales.csv",
        "daily_turnover": directory / "daily_turnover.csv",
        "sales_invoices": directory / "sales_invoices.csv",
        "sales_exceptions": directory / "clean_sales_exceptions.csv",
    }


PRODUCT_NAMES = [
    "Harbour Chicken Bowl", "Garden Pesto Pasta", "Smoky Beef Burger",
    "Roasted Veg Wrap", "Lemon Herb Chicken", "Golden Halloumi Salad",
    "Creamy Mushroom Penne", "Crispy Fish Plate", "Classic Brunch Stack",
    "Caramel Apple Tart", "Dark Cocoa Slice", "Vanilla Berry Cheesecake",
    "Spiced Pumpkin Soup", "Mediterranean Grain Bowl", "Grilled Steak Plate",
    "Buttermilk Pancake Stack", "Citrus Iced Tea", "House Lemonade",
    "Flat White Coffee", "Seasonal Fruit Cup", "Crispy Chicken Sandwich",
    "Tomato Basil Toast", "Roasted Pepper Quiche", "Chocolate Brownie"
]
SYNTHETIC_STAFF = [f"Staff {i:02d}" for i in range(1, 13)]
SYNTHETIC_MANAGERS = [f"Manager {i:02d}" for i in range(1, 4)]


def require_columns(df: pd.DataFrame, columns: set[str], filename: str) -> None:
    missing = columns - set(df.columns)
    if missing:
        raise ValueError(
            f"{filename} is missing required columns: {', '.join(sorted(missing))}"
        )


def numeric_series(df: pd.DataFrame, column: str) -> pd.Series:
    return pd.to_numeric(df[column], errors="coerce")


def robust_median(values: pd.Series | np.ndarray, fallback: float) -> float:
    values = pd.to_numeric(pd.Series(values), errors="coerce")
    values = values[np.isfinite(values) & (values > 0)]
    return float(values.median()) if not values.empty else fallback


def weekday_baseline(
    df: pd.DataFrame,
    date_col: str,
    value_col: str,
    fallback: float,
) -> dict[int, float]:
    dates = pd.to_datetime(df[date_col], errors="coerce")
    values = pd.to_numeric(df[value_col], errors="coerce")
    valid = dates.notna() & values.notna() & (values > 0)
    temp = pd.DataFrame({"weekday": dates[valid].dt.dayofweek, "value": values[valid]})
    overall = robust_median(temp["value"], fallback)
    result = {}
    for day in range(7):
        subset = temp.loc[temp["weekday"] == day, "value"]
        result[day] = robust_median(subset, overall)
    return result


def rounded_money(value: float) -> float:
    return round(max(0.0, float(value)) + 1e-9, 2)


def split_exact(total: float, weights: np.ndarray) -> np.ndarray:
    """Split a money total into cents; the returned values sum to total."""
    total_cents = int(round(max(0.0, total) * 100))
    if len(weights) == 0:
        return np.array([], dtype=float)
    weights = np.asarray(weights, dtype=float)
    if not np.isfinite(weights).all() or weights.sum() <= 0:
        weights = np.ones(len(weights), dtype=float)
    raw = weights / weights.sum() * total_cents
    cents = np.floor(raw).astype(int)
    remainder = total_cents - int(cents.sum())
    if remainder:
        order = np.argsort(-(raw - cents))
        cents[order[:remainder]] += 1
    return cents.astype(float) / 100


def fictional_catalog(
    product_sales: pd.DataFrame,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Create fictional products, using only broad department/price patterns."""
    dept = product_sales["department"].fillna("General").astype(str).str.strip()
    dept = dept.replace("", "General")
    qty = numeric_series(product_sales, "sold_qty")
    sales = numeric_series(product_sales, "total_sales")
    unit_price = sales / qty.replace(0, np.nan)

    source = pd.DataFrame({
        "department": dept,
        "qty": qty,
        "unit_price": unit_price,
    })
    source = source[
        source["department"].notna()
        & np.isfinite(source["unit_price"])
        & (source["unit_price"] > 0)
    ]

    if source.empty:
        source = pd.DataFrame({
            "department": ["Food", "Beverages", "Desserts"],
            "qty": [1, 1, 1],
            "unit_price": [100.0, 35.0, 55.0],
        })

    dept_weights = source["department"].value_counts(normalize=True).to_dict()
    departments = list(dept_weights)
    products = []
    name_index = 0

    for dept_index, department in enumerate(departments, start=1):
        prices = source.loc[source["department"] == department, "unit_price"]
        center = robust_median(prices, 80.0)
        # Prices are deliberately perturbed and rounded; source prices are not copied.
        n_products = int(rng.integers(3, 6))
        for local_index in range(n_products):
            raw_price = center * float(rng.uniform(0.72, 1.32))
            # Round to a plausible price point without retaining the source value.
            price = max(5.0, round(raw_price / 5.0) * 5.0 - 0.01)
            # A product name must identify one catalog item across all departments.
            # Once the base names are exhausted, give each additional item a
            # distinct fictional variant instead of silently recycling a name.
            base_name = PRODUCT_NAMES[name_index % len(PRODUCT_NAMES)]
            variant = name_index // len(PRODUCT_NAMES)
            name = base_name if variant == 0 else f"{base_name} - Variant {variant + 1}"
            name_index += 1
            products.append({
                "department": department,
                "product_code": f"SYN-{dept_index:02d}-{local_index + 1:03d}",
                "product_name": name,
                "reference_price": price,
                "department_weight": float(dept_weights[department]),
            })

    catalog = pd.DataFrame(products)
    if catalog["product_name"].duplicated().any():
        duplicates = catalog.loc[catalog["product_name"].duplicated(), "product_name"].tolist()
        raise RuntimeError(f"Synthetic catalog has duplicate product names: {duplicates}")
    if catalog["product_code"].duplicated().any():
        raise RuntimeError("Synthetic catalog has duplicate product codes.")
    weights = catalog["department_weight"].to_numpy(dtype=float)
    catalog["selection_weight"] = weights / weights.sum()
    return catalog


def payment_method_weights(invoices: pd.DataFrame) -> dict[str, float]:
    methods = ["cash", "credit_card", "accounts", "cheque"]
    totals = {}
    for method in methods:
        if method in invoices.columns:
            totals[method] = float(
                numeric_series(invoices, method).clip(lower=0).fillna(0).sum()
            )
        else:
            totals[method] = 0.0

    total = sum(totals.values())
    if total <= 0:
        return {"cash": 0.35, "credit_card": 0.55, "accounts": 0.09, "cheque": 0.01}
    # Smooth the distribution slightly so a rare method is still possible.
    smoothed = {key: value + total * 0.005 for key, value in totals.items()}
    denominator = sum(smoothed.values())
    return {key: value / denominator for key, value in smoothed.items()}


def infer_tax_rate(invoices: pd.DataFrame) -> float:
    inclusive = numeric_series(invoices, "inclusive")
    tax = numeric_series(invoices, "tax")
    valid = (inclusive > 0) & tax.notna() & (tax >= 0) & (tax < inclusive)
    if not valid.any():
        return 0.15
    rate = float((tax[valid] / inclusive[valid]).median())
    return float(np.clip(rate, 0.10, 0.20))


def generate(
    start_date: str,
    end_date: str,
    seed: int,
) -> None:
    inputs = source_files(OUTPUT_DIR)
    missing_files = [path for path in inputs.values() if not path.exists()]
    if missing_files:
        missing = "\n".join(f"  - {path}" for path in missing_files)
        raise FileNotFoundError(
            "Required reference CSV files were not found:\n"
            f"{missing}\nThe public workflow requires the bundled synthetic reference CSVs."
        )

    product_source = pd.read_csv(inputs["product_sales"])
    daily_source = pd.read_csv(inputs["daily_turnover"])
    invoice_source = pd.read_csv(inputs["sales_invoices"])
    exception_source = pd.read_csv(inputs["sales_exceptions"])

    require_columns(
        product_source,
        {"sale_datetime", "department", "product_code", "product_name", "sold_qty", "total_sales"},
        "product_sales.csv",
    )
    require_columns(
        daily_source,
        {"sale_date", "total_sales", "turnover_incl", "tax", "turnover_excl", "invoice_count",
         "cash", "credit_card", "accounts", "cheque", "non_turnover", "tips", "sales_rounding"},
        "daily_turnover.csv",
    )
    require_columns(
        invoice_source,
        {"sale_datetime", "invoice_number", "exclusive", "inclusive", "tax", "cash",
         "credit_card", "accounts", "cheque", "non_turnover"},
        "sales_invoices.csv",
    )
    require_columns(
        exception_source,
        {"exception_type", "invoice_number", "value"},
        "clean_sales_exceptions.csv",
    )

    start = pd.Timestamp(start_date).normalize()
    end = pd.Timestamp(end_date).normalize()
    if end < start:
        raise ValueError("The end date must be on or after the start date.")
    dates = pd.date_range(start, end, freq="D")
    if len(dates) > 370:
        raise ValueError("For safety, generate no more than 370 days at a time.")

    rng = np.random.default_rng(seed)
    catalog = fictional_catalog(product_source, rng)
    payment_weights = payment_method_weights(invoice_source)
    tax_rate = infer_tax_rate(invoice_source)

    # Learn broad weekday patterns, not individual transaction values.
    daily_baselines = weekday_baseline(
        daily_source, "sale_date", "turnover_incl", fallback=12000.0
    )
    invoice_baselines = weekday_baseline(
        daily_source, "sale_date", "invoice_count", fallback=60.0
    )
    exception_types = (
        exception_source["exception_type"]
        .dropna()
        .astype(str)
        .str.strip()
    )
    exception_types = exception_types[exception_types != ""]
    if exception_types.empty:
        exception_types = pd.Series(["Discount", "Void", "Correction"])
    exception_type_values = exception_types.value_counts().index.to_list()
    exception_type_probs = (
        exception_types.value_counts(normalize=True).reindex(exception_type_values).to_numpy()
    )

    source_invoice_count = max(1, len(invoice_source))
    exception_rate = len(exception_source) / source_invoice_count
    exception_rate = float(np.clip(exception_rate, 0.002, 0.025))

    invoice_rows = []
    product_rows = []
    exception_rows = []
    daily_rows = []

    for day_index, day in enumerate(dates):
        weekday = day.dayofweek
        # Broad weekday/weekend patterns, with fresh daily variation and a gentle trend.
        baseline = daily_baselines.get(weekday, 12000.0)
        trend = 1.0 + 0.0015 * day_index
        weekend_factor = 1.10 if weekday in (4, 5) else (0.82 if weekday == 6 else 1.0)
        daily_target = rounded_money(
            baseline * trend * weekend_factor * float(rng.uniform(0.72, 1.30))
        )
        daily_target = max(daily_target, 500.0)

        count_baseline = invoice_baselines.get(weekday, 60.0)
        invoice_count = max(
            12,
            int(round(count_baseline * float(rng.uniform(0.78, 1.24)))),
        )

        # Split each day's turnover across synthetic invoices, exactly to the cent.
        invoice_weights = rng.gamma(shape=2.0, scale=1.0, size=invoice_count)
        invoice_values = split_exact(daily_target, invoice_weights)
        day_invoice_rows = []

        payment_methods = list(payment_weights)
        payment_probs = np.array([payment_weights[m] for m in payment_methods])
        payment_probs = payment_probs / payment_probs.sum()

        for inv_idx, inclusive in enumerate(invoice_values, start=1):
            invoice_number = f"SYN-{day.strftime('%Y%m%d')}-{inv_idx:04d}"
            sale_hour = int(rng.choice([8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                                       p=np.array([2, 3, 5, 9, 12, 12, 11, 10, 10, 9, 8, 6, 3]) /
                                       np.array([2, 3, 5, 9, 12, 12, 11, 10, 10, 9, 8, 6, 3]).sum()))
            sale_minute = int(rng.integers(0, 60))
            sale_second = int(rng.integers(0, 60))
            sale_datetime = day + pd.Timedelta(
                hours=sale_hour, minutes=sale_minute, seconds=sale_second
            )
            tax = rounded_money(inclusive * tax_rate)
            exclusive = rounded_money(inclusive - tax)
            method = str(rng.choice(payment_methods, p=payment_probs))
            payment = {m: 0.0 for m in payment_methods}
            payment[method] = rounded_money(inclusive)

            row = {
                "sale_datetime": sale_datetime,
                "invoice_number": invoice_number,
                "exclusive": exclusive,
                "inclusive": rounded_money(inclusive),
                "employee": str(rng.choice(SYNTHETIC_STAFF)),
                "tax": tax,
                "recorded_datetime": sale_datetime + pd.Timedelta(minutes=int(rng.integers(0, 8))),
                "cash": payment["cash"],
                "credit_card": payment["credit_card"],
                "accounts": payment["accounts"],
                "cheque": payment["cheque"],
                "non_turnover": 0.0,
            }
            invoice_rows.append(row)
            day_invoice_rows.append(row)

        # Create fictional product lines for the day; their revenue sums to daily_target.
        line_count = int(rng.integers(8, 20))
        selected_indices = rng.choice(
            catalog.index.to_numpy(),
            size=line_count,
            replace=True,
            p=catalog["selection_weight"].to_numpy(),
        )
        line_weights = []
        line_meta = []
        for product_idx in selected_indices:
            product = catalog.loc[product_idx]
            qty = int(rng.choice([1, 1, 1, 2, 2, 3, 4]))
            raw_line = float(product["reference_price"]) * qty * float(rng.uniform(0.8, 1.25))
            line_weights.append(raw_line)
            line_meta.append((product, qty))
        line_values = split_exact(daily_target, np.array(line_weights))
        for (product, qty), line_total in zip(line_meta, line_values):
            product_rows.append({
                "sale_datetime": day + pd.Timedelta(
                    hours=int(rng.integers(8, 21)),
                    minutes=int(rng.integers(0, 60)),
                ),
                "department": product["department"],
                "product_code": product["product_code"],
                "product_name": product["product_name"],
                "sold_qty": qty,
                "total_sales": rounded_money(line_total),
            })

        # Daily summary is aggregated from synthetic invoice rows.
        invoice_df_day = pd.DataFrame(day_invoice_rows)
        daily_cash = rounded_money(invoice_df_day["cash"].sum())
        daily_card = rounded_money(invoice_df_day["credit_card"].sum())
        daily_accounts = rounded_money(invoice_df_day["accounts"].sum())
        daily_cheque = rounded_money(invoice_df_day["cheque"].sum())
        daily_inclusive = rounded_money(invoice_df_day["inclusive"].sum())
        daily_tax = rounded_money(invoice_df_day["tax"].sum())
        daily_exclusive = rounded_money(invoice_df_day["exclusive"].sum())
        daily_rows.append({
            "sale_date": day.date().isoformat(),
            "cash": daily_cash,
            "credit_card": daily_card,
            "accounts": daily_accounts,
            "cheque": daily_cheque,
            "non_turnover": 0.0,
            "tips": rounded_money(daily_inclusive * float(rng.uniform(0.015, 0.055))),
            "total_sales": daily_target,
            "sales_rounding": rounded_money(float(rng.choice([-0.02, -0.01, 0.0, 0.0, 0.01, 0.02]))),
            "turnover_incl": daily_inclusive,
            "tax": daily_tax,
            "turnover_excl": daily_exclusive,
            "invoice_count": invoice_count,
        })

        # A small proportion of synthetic invoices have a fictional exception.
        n_exceptions = int(rng.binomial(invoice_count, exception_rate))
        if n_exceptions:
            chosen_indices = rng.choice(len(day_invoice_rows), size=n_exceptions, replace=False)
            for chosen_index in chosen_indices:
                inv = day_invoice_rows[int(chosen_index)]
                before = float(inv["inclusive"])
                value = rounded_money(before * float(rng.uniform(0.02, 0.25)))
                exception_rows.append({
                    "exception_type": str(rng.choice(exception_type_values, p=exception_type_probs)),
                    "name": str(rng.choice(catalog["product_name"].to_numpy())),
                    "qty": int(rng.choice([1, 1, 1, 2])),
                    "table_number": str(int(rng.integers(1, 31))),
                    "invoice_number": inv["invoice_number"],
                    "exception_datetime": inv["sale_datetime"] + pd.Timedelta(
                        minutes=int(rng.integers(0, 20))
                    ),
                    "date": day.date().isoformat(),
                    "value": value,
                    "invoice_value_before": rounded_money(before),
                    "invoice_value_after": rounded_money(max(0.0, before - value)),
                    "employee": str(rng.choice(SYNTHETIC_STAFF)),
                    "authorized_by": str(rng.choice(SYNTHETIC_MANAGERS)),
                })

    product_out = pd.DataFrame(product_rows, columns=[
        "sale_datetime", "department", "product_code", "product_name", "sold_qty", "total_sales"
    ])
    daily_out = pd.DataFrame(daily_rows, columns=[
        "sale_date", "cash", "credit_card", "accounts", "cheque", "non_turnover", "tips",
        "total_sales", "sales_rounding", "turnover_incl", "tax", "turnover_excl", "invoice_count"
    ])
    invoice_out = pd.DataFrame(invoice_rows, columns=[
        "sale_datetime", "invoice_number", "exclusive", "inclusive", "employee", "tax",
        "recorded_datetime", "cash", "credit_card", "accounts", "cheque", "non_turnover"
    ])
    exception_out = pd.DataFrame(exception_rows, columns=[
        "exception_type", "name", "qty", "table_number", "invoice_number", "exception_datetime",
        "date", "value", "invoice_value_before", "invoice_value_after", "employee", "authorized_by"
    ])

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    product_path = OUTPUT_DIR / "product_sales.csv"
    daily_path = OUTPUT_DIR / "daily_turnover.csv"
    invoice_path = OUTPUT_DIR / "sales_invoices.csv"
    exception_path = OUTPUT_DIR / "clean_sales_exceptions.csv"

    product_out.to_csv(product_path, index=False, date_format="%Y-%m-%d %H:%M:%S")
    daily_out.to_csv(daily_path, index=False)
    invoice_out.to_csv(invoice_path, index=False, date_format="%Y-%m-%d %H:%M:%S")
    exception_out.to_csv(exception_path, index=False, date_format="%Y-%m-%d %H:%M:%S")

    validate_outputs(product_out, daily_out, invoice_out, exception_out)

    print("\nSynthetic data generation completed.")
    print(f"Period: {start.date()} to {end.date()} ({len(dates)} days)")
    print(f"Output folder: {OUTPUT_DIR}")
    print(f"product_sales.csv: {len(product_out):,} rows")
    print(f"daily_turnover.csv: {len(daily_out):,} rows")
    print(f"sales_invoices.csv: {len(invoice_out):,} rows")
    print(f"clean_sales_exceptions.csv: {len(exception_out):,} rows")
    print("Validation: passed")
    print("Reference CSVs were read; PostgreSQL was not accessed.")


def validate_outputs(
    product_sales: pd.DataFrame,
    daily_turnover: pd.DataFrame,
    invoices: pd.DataFrame,
    exceptions: pd.DataFrame,
) -> None:
    """Fail loudly if the generated data does not reconcile."""
    if daily_turnover["sale_date"].duplicated().any():
        raise RuntimeError("Validation failed: duplicate sale_date in daily_turnover.")

    daily_product_totals = (
        product_sales.assign(sale_date=pd.to_datetime(product_sales["sale_datetime"]).dt.date)
        .groupby("sale_date")["total_sales"].sum()
    )
    daily_target = daily_turnover.assign(
        sale_date=pd.to_datetime(daily_turnover["sale_date"]).dt.date
    ).set_index("sale_date")["total_sales"]

    diff = (daily_product_totals.reindex(daily_target.index, fill_value=0) - daily_target).abs()
    if (diff > 0.01).any():
        raise RuntimeError("Validation failed: product sales do not match daily total_sales.")

    invoice_daily = invoices.assign(
        sale_date=pd.to_datetime(invoices["sale_datetime"]).dt.date
    ).groupby("sale_date")["inclusive"].sum()
    daily_inclusive = daily_turnover.assign(
        sale_date=pd.to_datetime(daily_turnover["sale_date"]).dt.date
    ).set_index("sale_date")["turnover_incl"]
    diff = (invoice_daily.reindex(daily_inclusive.index, fill_value=0) - daily_inclusive).abs()
    if (diff > 0.01).any():
        raise RuntimeError("Validation failed: invoice inclusive does not match turnover_incl.")

    payment_sum = invoices[["cash", "credit_card", "accounts", "cheque"]].sum(axis=1)
    if ((payment_sum - invoices["inclusive"]).abs() > 0.01).any():
        raise RuntimeError("Validation failed: invoice payment methods do not match inclusive.")

    invoice_numbers = set(invoices["invoice_number"].astype(str))
    if not set(exceptions["invoice_number"].astype(str)).issubset(invoice_numbers):
        raise RuntimeError("Validation failed: an exception references an unknown invoice.")

    if not exceptions.empty:
        if exceptions["invoice_number"].isna().any():
            raise RuntimeError("Validation failed: an exception has no invoice number.")
        if (exceptions["value"] < 0).any():
            raise RuntimeError("Validation failed: exception values must not be negative.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate coordinated synthetic Bistro CSVs.")
    parser.add_argument("--start", default="2026-10-01", help="First synthetic date (YYYY-MM-DD).")
    parser.add_argument("--end", default="2026-12-31", help="Last synthetic date (YYYY-MM-DD).")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for repeatable output.")
    args = parser.parse_args()
    generate(args.start, args.end, args.seed)


if __name__ == "__main__":
    main()
