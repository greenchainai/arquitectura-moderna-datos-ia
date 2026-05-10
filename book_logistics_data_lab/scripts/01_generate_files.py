#!/usr/bin/env python3
"""
Generate synthetic logistics data as CSV and/or Parquet files.

Examples:
  python scripts/01_generate_files.py --output-dir data/output --format csv --n-orders 5000
  python scripts/01_generate_files.py --output-dir data/output --format both --n-orders 5000

Parquet requires pyarrow or fastparquet. Install requirements first:
  pip install -r requirements.txt
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from common_synthetic_generator import GenerationConfig, TABLE_ORDER, generate_all, write_tables


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate synthetic logistics data files.")
    parser.add_argument("--output-dir", default="data/output", help="Base output directory.")
    parser.add_argument("--format", choices=["csv", "parquet", "both"], default="csv", help="Output format.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for deterministic generation.")
    parser.add_argument("--n-customers", type=int, default=500)
    parser.add_argument("--n-partners", type=int, default=30)
    parser.add_argument("--n-warehouses", type=int, default=12)
    parser.add_argument("--n-carriers", type=int, default=15)
    parser.add_argument("--n-routes", type=int, default=80)
    parser.add_argument("--n-orders", type=int, default=5000)
    parser.add_argument("--start-date", default="2025-01-01")
    parser.add_argument("--end-date", default="2026-04-30")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = GenerationConfig(
        seed=args.seed,
        n_customers=args.n_customers,
        n_partners=args.n_partners,
        n_warehouses=args.n_warehouses,
        n_carriers=args.n_carriers,
        n_routes=args.n_routes,
        n_orders=args.n_orders,
        start_date=args.start_date,
        end_date=args.end_date,
    )

    tables = generate_all(config)
    base_dir = Path(args.output_dir)

    if args.format in ["csv", "both"]:
        csv_dir = base_dir / "csv"
        write_tables(tables, csv_dir, "csv")
        print(f"CSV files written to: {csv_dir.resolve()}")

    if args.format in ["parquet", "both"]:
        parquet_dir = base_dir / "parquet"
        try:
            write_tables(tables, parquet_dir, "parquet")
            print(f"Parquet files written to: {parquet_dir.resolve()}")
        except ImportError as exc:
            print("Parquet generation requires pyarrow or fastparquet.")
            print("Install dependencies with: pip install -r requirements.txt")
            raise exc

    print("\nGenerated row counts:")
    for table in TABLE_ORDER:
        print(f"  {table:<24} {len(tables[table]):>8}")

if __name__ == "__main__":
    main()
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)
