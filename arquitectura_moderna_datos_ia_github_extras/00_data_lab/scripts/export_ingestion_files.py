#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd


def export_files(input_dir: Path, output_dir: Path, fmt: str) -> None:
    (output_dir / "csv").mkdir(parents=True, exist_ok=True)
    (output_dir / "parquet").mkdir(parents=True, exist_ok=True)
    for csv_file in sorted(input_dir.glob("*.csv")):
        df = pd.read_csv(csv_file)
        if fmt in ("csv", "both"):
            df.to_csv(output_dir / "csv" / csv_file.name, index=False)
        if fmt in ("parquet", "both"):
            df.to_parquet(output_dir / "parquet" / f"{csv_file.stem}.parquet", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="data/generated")
    parser.add_argument("--output-dir", default="data/ingestion")
    parser.add_argument("--format", choices=["csv", "parquet", "both"], default="both")
    args = parser.parse_args()
    export_files(Path(args.input_dir), Path(args.output_dir), args.format)
