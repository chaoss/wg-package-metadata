#!/usr/bin/env python3
"""
Filter a license coverage CSV to a balanced sample: at most N packages per ecosystem.

The top 0.1%, 1%, and 10% samples from Ecosyste.ms are popularity-based across all
packages, so ecosystem sample sizes are unequal (e.g. Go and npm dominate the 10% file).
This script keeps the first N rows per ecosystem (in file order), producing a CSV
with a more balanced sample across package managers for comparison.

Copyright 2026
Licensed under the Apache License, Version 2.0
"""

import argparse
import csv
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Filter a license CSV to at most N packages per ecosystem (balanced sample).",
        epilog="""
Examples:
  %(prog)s ../data/2025-11-26/licenses-10.csv -o ../data/2025-11-26/licenses-10-balanced.csv
  %(prog)s ../data/2025-11-26/licenses-10.csv --max 500 --analyze

Output CSV has the same columns: ecosystem,name,licenses.
Use --analyze to run the license coverage analysis on the filtered CSV and write
the processed results to the drafts directory.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "input_csv",
        type=Path,
        help="Input CSV (ecosystem,name,licenses) e.g. licenses-10.csv",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Output filtered CSV path (default: <input_stem>-balanced.csv in same dir)",
    )
    parser.add_argument(
        "-n", "--max",
        type=int,
        default=500,
        metavar="N",
        help="Max packages per ecosystem (default: 500)",
    )
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Run analyze_license_coverage.py on the filtered CSV after writing it",
    )
    parser.add_argument(
        "--analysis-output-dir",
        type=Path,
        default=None,
        help="Directory for analysis output (default: ../docs/attribute_analysis/drafts/)",
    )
    args = parser.parse_args()

    if not args.input_csv.exists():
        print(f"Error: File not found: {args.input_csv}", file=sys.stderr)
        sys.exit(1)

    if args.output is None:
        args.output = args.input_csv.parent / "licenses-500top-balanced.csv"

    # Read and detect header / skip log line
    with open(args.input_csv, encoding="utf-8") as f:
        first_line = f.readline()
    skip_first = not first_line.strip().startswith("ecosystem")

    # Collect first N rows per ecosystem (file order)
    counts = {}
    rows_by_ecosystem = []
    fieldnames = ["ecosystem", "name", "licenses"]

    with open(args.input_csv, encoding="utf-8") as f:
        if skip_first:
            next(f)
        reader = csv.DictReader(f, fieldnames=fieldnames)
        for row in reader:
            eco = row.get("ecosystem", "").strip()
            if eco not in counts:
                counts[eco] = 0
            if counts[eco] < args.max:
                counts[eco] += 1
                rows_by_ecosystem.append(row)

    total = sum(counts.values())
    num_ecosystems = len(counts)
    print(f"Balanced sample: {total:,} packages across {num_ecosystems} ecosystems (max {args.max} per ecosystem)")
    print(f"Writing: {args.output}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_by_ecosystem)

    if args.analyze:
        script_dir = Path(__file__).resolve().parent
        analyzer = script_dir / "analyze_license_coverage.py"
        cmd = [sys.executable, str(analyzer), str(args.output)]
        if args.analysis_output_dir is not None:
            cmd.extend(["-o", str(args.analysis_output_dir)])
        print(f"\nRunning: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
