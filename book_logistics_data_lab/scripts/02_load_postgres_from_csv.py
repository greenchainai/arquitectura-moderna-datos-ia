#!/usr/bin/env python3
"""
Load generated CSV files into PostgreSQL using COPY.

Environment variables:
  PGHOST=localhost
  PGPORT=5432
  PGDATABASE=logistics_ai_lab
  PGUSER=postgres
  PGPASSWORD=postgres

Example:
  python scripts/02_load_postgres_from_csv.py --input-dir data/output/csv --truncate
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

try:
    import psycopg2
except ImportError as exc:
    raise SystemExit("Missing dependency psycopg2. Install with: pip install -r requirements.txt") from exc

from common_synthetic_generator import TABLE_ORDER

SCHEMA = "logistics"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load synthetic logistics CSV files into PostgreSQL.")
    parser.add_argument("--input-dir", default="data/output/csv", help="Directory containing CSV files.")
    parser.add_argument("--schema", default=SCHEMA, help="Target PostgreSQL schema.")
    parser.add_argument("--truncate", action="store_true", help="Truncate target tables before loading.")
    return parser.parse_args()


def get_connection():
    return psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=int(os.getenv("PGPORT", "5432")),
        dbname=os.getenv("PGDATABASE", "logistics_ai_lab"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", "postgres"),
    )


def table_columns(csv_path: Path) -> str:
    with csv_path.open("r", encoding="utf-8") as f:
        header = f.readline().strip()
    cols = [f'"{c}"' for c in header.split(",")]
    return ", ".join(cols)


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        raise SystemExit(f"Input directory not found: {input_dir}")

    conn = get_connection()
    conn.autocommit = False
    try:
        with conn.cursor() as cur:
            if args.truncate:
                truncate_tables = ", ".join([f'{args.schema}.{t}' for t in reversed(TABLE_ORDER)])
                cur.execute(f"TRUNCATE TABLE {truncate_tables} RESTART IDENTITY CASCADE;")
                print("Target tables truncated.")

            for table in TABLE_ORDER:
                csv_path = input_dir / f"{table}.csv"
                if not csv_path.exists():
                    raise FileNotFoundError(f"Missing CSV file: {csv_path}")
                cols = table_columns(csv_path)
                copy_sql = f"COPY {args.schema}.{table} ({cols}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE, NULL '');"
                with csv_path.open("r", encoding="utf-8") as f:
                    cur.copy_expert(copy_sql, f)
                print(f"Loaded {table}")

            conn.commit()
        print("\nLoad completed successfully.")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    main()
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)
