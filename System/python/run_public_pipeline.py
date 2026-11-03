"""Public portfolio pipeline: synthetic generation -> PostgreSQL synthetic DB.

Never imports or runs the original private data ingestion pipeline.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
import generate_synthetic_data
import load_synthetic_database

ROOT = Path(__file__).resolve().parents[2]

def main() -> None:
    parser = argparse.ArgumentParser(description="Run the public synthetic analytics pipeline")
    parser.add_argument("--skip-generate", action="store_true", help="Load the committed synthetic CSVs without regenerating")
    parser.add_argument("--start", default="2026-10-01")
    parser.add_argument("--end", default="2026-12-31")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if not args.skip_generate:
        print("[1/2] Generating synthetic CSVs using public reference data", flush=True)
        generate_synthetic_data.generate(args.start, args.end, args.seed, source="synthetic")
    print("[2/2] Loading only basic_bistro_synthetic", flush=True)
    load_synthetic_database.main()
    print("Public pipeline completed. Refresh Power BI Desktop to see updated data.")

if __name__ == "__main__":
    main()
