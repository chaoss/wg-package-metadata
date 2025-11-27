# Package Metadata Processing Tools

A collection of data processing tools for analyzing package metadata across different ecosystems.

## Overview

This toolkit provides utilities for processing and analyzing package metadata collected from various package registries and ecosystems. The primary focus is on assessing the quality and machine-readability of metadata attributes such as license declarations.

## Tools

### `analyze_license_coverage.py`

Analyzes license metadata to determine the percentage of packages with valid SPDX license expressions per ecosystem.

**Features:**
- Validates license declarations as SPDX expressions
- Considers empty, null, and escape hatch values (e.g., `NONE`, `NOASSERTION`) as failure to declare in machine readable way.
- Aggregates coverage statistics by ecosystem
- Outputs results in CSV format for further analysis

**Usage:**
```bash
pipenv run python analyze_license_coverage.py <input.csv> [<input2.csv> ...]
```

**Input Format:**
CSV files with columns: `ecosystem`, `name`, `licenses`

**Output:**
- Processed CSV files with suffix `_processed.csv` containing coverage statistics
- Files are saved in the `docs/attribute_analysis/drafts/` directory

**Example:**
```bash
pipenv run python analyze_license_coverage.py ../data/2025-11-26/licenses-1.csv
```

## Installation

This project uses pipenv for dependency management:

```bash
# Install dependencies
pipenv install

# Run tools
pipenv run python analyze_license_coverage.py <file.csv>
```

### Requirements
- Python 3.13+
- pandas
- license-expression

## Data Sources

The tools process data from various sources including:
- [Ecosyste.ms](https://ecosyste.ms/) - Package ecosystem data (CC BY-SA 4.0)

When using data from external sources, ensure proper attribution is maintained.

## Contributing

When adding new tools:
1. Follow the established patterns for CLI argument parsing
2. Use CSV format for input and output where applicable
3. Include proper documentation in this README
4. Add any new dependencies to `pyproject.toml`

## License

Copyright 2025

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

