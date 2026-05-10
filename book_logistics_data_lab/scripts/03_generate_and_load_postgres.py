#!/usr/bin/env python3
"""
Convenience wrapper: generate CSV files and load them into PostgreSQL.

Example:
  python scripts/03_generate_and_load_postgres.py --output-dir data/output --n-orders 5000 --truncate
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate synthetic files and load PostgreSQL.")
    parser.add_argument("--output-dir", default="data/output")
    parser.add_argument("--n-orders", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--truncate", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    script_dir = Path(__file__).parent
    generate_cmd = [
        sys.executable,
        str(script_dir / "01_generate_files.py"),
        "--output-dir",
        args.output_dir,
        "--format",
        "csv",
        "--n-orders",
        str(args.n_orders),
        "--seed",
        str(args.seed),
    ]
    load_cmd = [
        sys.executable,
        str(script_dir / "02_load_postgres_from_csv.py"),
        "--input-dir",
        str(Path(args.output_dir) / "csv"),
    ]
    if args.truncate:
        load_cmd.append("--truncate")

    subprocess.run(generate_cmd, check=True)
    subprocess.run(load_cmd, check=True)

if __name__ == "__main__":
    main()
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)
