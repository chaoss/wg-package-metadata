#!/usr/bin/env python3
"""
License Coverage Analysis Tool

This script analyzes license metadata from ecosyste.ms data to determine
the percentage of packages with valid SPDX license expressions per ecosystem.

Copyright 2025
Licensed under the Apache License, Version 2.0
"""

import argparse
import sys
import pandas as pd
from pathlib import Path
from license_expression import get_spdx_licensing, ExpressionError


# SPDX escape hatches that indicate no valid license was declared
# These are excluded from the "valid SPDX" count as they represent
# the use of escape hatches rather than actual license declarations
ESCAPE_HATCHES = {
    'NONE',           # No license declared
    'NOASSERTION',    # License not determined/asserted
    'UNKNOWN',        # Unknown license
    'SEE LICENSE IN', # Reference to external license file (not an SPDX ID)
}


def is_valid_spdx_expression(license_value):
    """
    Check if a license value is a valid SPDX expression.
    
    Excludes escape hatches like NONE, NOASSERTION which technically parse
    as valid SPDX but don't represent actual license declarations.
    
    Args:
        license_value: The license string to validate
        
    Returns:
        bool: True if valid SPDX expression (excluding escape hatches), False otherwise
    """
    # Handle null, empty, or whitespace-only values
    if pd.isna(license_value):
        return False
    
    license_str = str(license_value).strip()
    if not license_str:
        return False
    
    # Check for escape hatches (case-insensitive)
    license_upper = license_str.upper()
    for escape in ESCAPE_HATCHES:
        if escape in license_upper:
            return False
    
    # Try to parse as SPDX expression
    licensing = get_spdx_licensing()
    try:
        parsed = licensing.parse(license_str)
        # Additional check: ensure it's not just an escape hatch that parsed
        if not parsed:
            return False
        return True
    except (ExpressionError, Exception):
        return False


def analyze_csv_file(csv_path, output_dir):
    """
    Analyze a single CSV file for license coverage per ecosystem.
    
    Args:
        csv_path: Path to the CSV file
        output_dir: Directory to save the processed CSV output
        
    Returns:
        tuple: (results_dict, output_csv_path)
    """
    print(f"\n{'='*80}")
    print(f"Analyzing: {csv_path.name}")
    print(f"{'='*80}\n")
    
    # Read CSV file (skip first line if it's a log line)
    df = pd.read_csv(csv_path, skiprows=0)
    
    # Overall statistics
    total_packages = len(df)
    print(f"Total packages: {total_packages:,}")
    print(f"Total ecosystems: {df['ecosystem'].nunique()}\n")
    
    # Analyze by ecosystem
    results = []
    
    for ecosystem in sorted(df['ecosystem'].unique()):
        ecosystem_df = df[df['ecosystem'] == ecosystem]
        total = len(ecosystem_df)
        
        # Count valid SPDX expressions
        valid_count = sum(
            is_valid_spdx_expression(license_val) 
            for license_val in ecosystem_df['licenses']
        )
        
        coverage_pct = (valid_count / total * 100) if total > 0 else 0
        
        results.append({
            'ecosystem': ecosystem,
            'total_packages': total,
            'valid_spdx': valid_count,
            'invalid_or_missing': total - valid_count,
            'coverage_percent': round(coverage_pct, 2)
        })
        
        print(f"{ecosystem:20s} | Total: {total:6,} | Valid SPDX: {valid_count:6,} | Coverage: {coverage_pct:6.2f}%")
    
    # Overall coverage across all ecosystems
    total_valid = sum(r['valid_spdx'] for r in results)
    overall_coverage = (total_valid / total_packages * 100) if total_packages > 0 else 0
    
    print(f"\n{'─'*80}")
    print(f"{'OVERALL':20s} | Total: {total_packages:6,} | Valid SPDX: {total_valid:6,} | Coverage: {overall_coverage:6.2f}%")
    print(f"{'─'*80}")
    
    # Create output dataframe and save as CSV
    results_df = pd.DataFrame(results)
    
    # Create output filename with 'processed' suffix
    output_filename = csv_path.stem + '_processed.csv'
    output_path = output_dir / output_filename
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save to CSV
    results_df.to_csv(output_path, index=False)
    print(f"\nProcessed results saved to: {output_path}")
    
    return results, output_path


def main():
    """Main analysis function."""
    parser = argparse.ArgumentParser(
        description='Analyze license metadata coverage in package ecosystem data.',
        epilog="""
Examples:
  %(prog)s data/licenses-1.csv
  %(prog)s data/licenses-0.1.csv data/licenses-1.csv

The script processes CSV files containing ecosystem, name, and licenses columns.
It validates license declarations as SPDX expressions and outputs coverage
statistics per ecosystem. Results are saved as CSV files with '_processed' suffix
in the docs/attribute_analysis/drafts/ directory.

Escape hatches (NONE, NOASSERTION, etc.) are excluded from valid SPDX counts
as they represent the use of fallback mechanisms rather than actual license
declarations.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'csv_files',
        nargs='+',
        type=Path,
        help='One or more CSV files to analyze'
    )
    
    parser.add_argument(
        '-o', '--output-dir',
        type=Path,
        default=None,
        help='Output directory for processed CSV files (default: ../docs/attribute_analysis/drafts/)'
    )
    
    args = parser.parse_args()
    
    # Determine output directory
    if args.output_dir:
        output_dir = args.output_dir
    else:
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        output_dir = project_root / "docs" / "attribute_analysis" / "drafts"
    
    print("\n" + "="*80)
    print(" LICENSE COVERAGE ANALYSIS ".center(80, "="))
    print("="*80)
    print("\nThis analysis measures the percentage of packages with valid SPDX")
    print("license expressions across different package ecosystems.")
    print(f"\nOutput directory: {output_dir}")
    print("\nExcluding escape hatches: NONE, NOASSERTION, UNKNOWN, SEE LICENSE IN")
    print("These indicate no license was declared or use of fallback mechanisms.")
    
    # Analyze all provided CSV files
    all_results = {}
    
    for csv_file in args.csv_files:
        if not csv_file.exists():
            print(f"\nError: File not found: {csv_file}", file=sys.stderr)
            continue
        
        results, output_path = analyze_csv_file(csv_file, output_dir)
        all_results[csv_file.stem] = {
            'results': results,
            'output_path': output_path
        }
    
    # If multiple files were analyzed, show comparison
    if len(all_results) >= 2:
        print(f"\n{'='*80}")
        print(" COMPARISON SUMMARY ".center(80, "="))
        print(f"{'='*80}\n")
        
        # Get all unique ecosystems across all files
        all_ecosystems = set()
        for data in all_results.values():
            for result in data['results']:
                all_ecosystems.add(result['ecosystem'])
        
        # Print header
        header = f"{'Ecosystem':20s}"
        for file_name in sorted(all_results.keys()):
            header += f" | {file_name:>20s}"
        print(header)
        print("─" * len(header))
        
        # Print each ecosystem's coverage across all files
        for ecosystem in sorted(all_ecosystems):
            row = f"{ecosystem:20s}"
            for file_name in sorted(all_results.keys()):
                data = all_results[file_name]
                ecosystem_data = next(
                    (r for r in data['results'] if r['ecosystem'] == ecosystem),
                    None
                )
                if ecosystem_data:
                    coverage = ecosystem_data['coverage_percent']
                    row += f" | {coverage:19.2f}%"
                else:
                    row += f" | {'-':>20s}"
            print(row)
    
    print(f"\n{'='*80}")
    print(" ANALYSIS COMPLETE ".center(80, "="))
    print(f"{'='*80}\n")
    
    # Print output file locations
    print("Processed CSV files:")
    for file_name, data in all_results.items():
        print(f"  - {data['output_path']}")
    print()


if __name__ == "__main__":
    main()
