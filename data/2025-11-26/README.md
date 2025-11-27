# License Data from Ecosyste.ms

## Attribution

This data is sourced from [Ecosyste.ms](https://ecosyste.ms/) and is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

**Data Source**: Ecosyste.ms  
**License**: CC BY-SA 4.0 (Creative Commons Attribution-ShareAlike 4.0 International)  
**Collection Date**: November 26, 2025

## Data Files

This directory contains three CSV files with license metadata for popular packages across different ecosystems:

### licenses-0.1.csv
Contains license information for the **top 0.1% of packages** per package manager/ecosystem, ranked by popularity metrics (downloads, usage, etc.).

### licenses-1.csv
Contains license information for the **top 1% of packages** per package manager/ecosystem, ranked by popularity metrics (downloads, usage, etc.).

## Data Structure

Each CSV file contains the following columns:
- **ecosystem**: The package manager/ecosystem (e.g., npm, cargo, pypi, go)
- **name**: The package name
- **licenses**: The license information as declared in the package metadata

## Purpose

This data is used to analyze license metadata coverage and quality across different package managers, specifically to:
- Measure the percentage of packages with valid SPDX license expressions
- Compare license metadata practices across ecosystems
- Assess the machine-readability of license declarations

## Methodology

The data represents the most popular packages in each ecosystem, providing a representative sample of license metadata practices for packages that are widely used and maintained.

