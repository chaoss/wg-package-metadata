# License Metadata Analysis

This document analyzes how different package managers handle license metadata across ecosystems.

## 1. Key findings summary

_TBD after sections 2–7 are finalized._

## 2. Data Collection Overview

This section provides an overview of the ecosystems and package managers reviewed to determine whether they make license information available as part of their metadata. For each package manager, we indicate the level of support for license data and point to the relevant specification or documentation. This establishes the foundation for deeper analysis in subsequent sections.

### Rust Ecosystem — Cargo
**License Information Available**: SPDX expression (with escape hatch to provide a license file instead)
**Reference**: [Cargo Reference: The Manifest Format](https://doc.rust-lang.org/cargo/reference/manifest.html#the-license-and-license-file-fields)

### Python Ecosystem — PyPI (pip)
**License Information Available**: SPDX expression (in Python > 3.17), with ambiguous alternatives retained for backward compatibility
**References**:
- [Python Packaging User Guide — Dependency Specifiers](https://packaging.python.org/en/latest/specifications/dependency-specifiers/#dependency-specifiers)
- PEP 621 ([Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/))
- PEP 639 ([Improving License Clarity with SPDX](https://peps.python.org/pep-0639/))
- PEP 643 ([Metadata for Python Software Packages](https://peps.python.org/pep-0643/))

### Container Ecosystem — Docker
**License Information Available**: No
**Reference**: [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)

## 3. Field Analysis

This section groups ecosystems according to how license information can be specified in their package metadata. The focus here is on whether the declaration is unambiguous, ambiguous, or not supported at all, along with the types of definitions that are accepted in practice.

### Unambiguously specified

#### Rust Ecosystem — Cargo
- **Accepted definitions**:
  - SPDX license identifiers
  - SPDX license expressions (e.g., `MIT OR Apache-2.0`)
  - Escape hatch: reference to a license file in the package repository
- Cargo enforces SPDX validation, which ensures unambiguous interpretation of declared licenses.

### Ambiguously specified

#### Python Ecosystem — PyPI (pip)
- **Accepted definitions**:
  - SPDX identifiers and expressions (supported in Python > 3.17)
  - Free-form strings (e.g., “MIT License”, “BSD-style”)
  - Copy-paste of license text blocks
  - Historical community conventions where classifiers in `setup.py` or metadata loosely indicated license type
- The presence of multiple valid formats and lack of strict validation means license information can be ambiguous.

### Unspecified

#### Container Ecosystem — Docker
- **Accepted definitions**:
  - No formal mechanism for license metadata in Docker images
  - Licensing information is sometimes provided in external documentation, README files, or image repository descriptions as a community practice
- This absence of structured license declarations makes automated analysis unreliable.

## 4. Data Format Analysis

License metadata is not only expressed in different formats, but also stored in different locations across ecosystems. Some package managers require the license to be declared directly in project source files, others embed it into the distributed package, and some expose it only through registry metadata or websites. These variations affect both the reliability of license declarations and the ease with which automated tools can access them.

### Rust Ecosystem — Cargo
- **Data type**: String containing an SPDX expression.
- **License expression support**: Accepts both single SPDX identifiers (e.g., `MIT`) and full SPDX expressions (e.g., `MIT OR Apache-2.0`).
- **Location**: Declared in `Cargo.toml` under the `[package]` section. The manifest file, along with any referenced license file, is included in the `.crate` package uploaded to crates.io. This ensures license metadata is redistributed and accessible both from the source and from the published artifact.
- **Notes**: Cargo enforces SPDX validation. If a valid SPDX expression is not provided, the alternative is to reference a license file directly.

### Python Ecosystem — PyPI (pip)
- **Data type**: String without enforced structure.
- **License expression support**:
  - Modern metadata (Python > 3.17) supports SPDX identifiers and expressions.
  - Legacy metadata allows arbitrary free-form strings, from license names (“MIT License”) to pasted license text.
- **Location**: Declared in project configuration files (`pyproject.toml`, `setup.cfg`, `setup.py`). These declarations may or may not be preserved in the built distribution (`wheel` or `sdist`). The PyPI registry surface (web and API) is the most consistent place to retrieve license metadata, but ambiguity remains due to mixed formats.
- **Notes**: Because both SPDX and free-style values are still allowed, license information is not uniformly reliable across packages.

### Container Ecosystem — Docker
- **Data type**: None — no structured license attribute is supported.
- **License expression support**: Not applicable.
- **Location**: Docker images do not embed license metadata. Any licensing information is external, typically shown in Docker Hub image descriptions or project documentation. Such information is not redistributed with the image itself, making it inaccessible for automated processing.
- **Notes**: The lack of in-artifact metadata means license discovery depends entirely on community practices or external documentation.

## 5. Access Patterns

Access to license metadata varies across ecosystems. Some make it directly available from the project source or distribution, while others rely on registry infrastructure or provide no access at all.

### Rust Ecosystem — Cargo
- **Direct access**: License information is available in the `Cargo.toml` file within the source code and redistributed in the `.crate` package.
- **CLI access**: The `cargo metadata` command provides license information as part of the structured metadata output.
- **Registry access**: License information is displayed on crates.io package pages.
- **API access**: crates.io provides a JSON API that includes the license field for published packages.

### Python Ecosystem — PyPI (pip)
- **Direct access**: License declarations appear in configuration files (`pyproject.toml`, `setup.cfg`, `setup.py`), though not always preserved in built artifacts.
- **CLI access**: `pip show <package>` displays license information for packages installed in the local environment. It does not query PyPI directly.
- **Registry access**: PyPI package pages display license information in a dedicated field.
- **API access**: The PyPI JSON API exposes the license field, though its reliability depends on whether the package used SPDX or free-form declarations.

### Container Ecosystem — Docker
- **Direct access**: It is possible to include `LICENSE` files within images, but this is optional. Even when present, it is not clear whether such a file represents the license of the image itself, the software installed inside it, or only part of its contents.
- **CLI access**: None. The `docker inspect` command surfaces image metadata, but license information is not among the supported attributes.
- **Registry access**: License details, if provided, appear only in free-text descriptions on Docker Hub or other registries.
- **API access**: Docker Hub APIs can return image descriptions, but they do not include a structured license field.

## 6. Quality Assessment

The quality of license metadata across ecosystems varies widely, not only in terms of completeness but also in clarity and machine-readability. Below we evaluate coverage, reliability, and key limitations.

### Rust Ecosystem — Cargo
- **Coverage**: TBD
- **Reliability**: Strong. SPDX validation ensures that declared identifiers and expressions are unambiguous and machine-readable.
- **Limitations**:
  - When a license file is used instead of an SPDX expression, automated tooling must parse external text, which introduces variability.

### Python Ecosystem — PyPI (pip)
- **Coverage**: TBD
- **Reliability**: Weak to mixed.
  - Newer projects (Python > 3.17, setuptools ≥ 66.0) can use SPDX identifiers and expressions, making license data machine-readable.
  - Older projects often use free-form text or inconsistent naming (“BSD-style”, “GPLv2 or later”), which complicates parsing.
- **Limitations**:
  - Backward compatibility means ambiguous license strings will remain in circulation for the foreseeable future.
  - Some projects include a `LICENSE` file in their source but leave the metadata blank, forcing consumers to rely on heuristics.

### Container Ecosystem — Docker
- **Coverage**: TBD
- **Reliability**: Absent. Crawling image descriptions in registries is only a heuristic approach, and most descriptions do not include licensing information.
- **Limitations**:
  - Registries like Docker Hub sometimes display licensing information in free-text descriptions, but this is inconsistent and not machine-readable.
  - Without structured metadata, automated compliance tooling cannot reliably determine licensing status.

## 7. Transformation Requirements

To make license information usable across ecosystems, processes must account for the different formats and locations where licenses are declared. The goal is to produce validated SPDX expressions from heterogeneous sources.

### Rust Ecosystem — Cargo
1. Read the `license` attribute from `Cargo.toml`.
   - If present, this will contain an SPDX identifier or expression, which can be parsed directly with an SPDX expression parser.
2. If the `license-file` attribute is used instead, extract the referenced file from the source or the redistributed `.crate` package.
   - Apply a license text scanner (e.g., *scancode-toolkit*) to identify the most likely SPDX identifier(s).
   - Convert the result into a valid SPDX expression.

### Python Ecosystem — PyPI (pip)
1. Read the license attribute from `pyproject.toml`, `setup.cfg`, or `setup.py`.
   - If it contains an SPDX identifier or expression (common in newer packages), parse it directly.
   - If it contains a free-form string, normalize common variations (e.g., “BSD-style” → `BSD-2-Clause`).
   - If it contains a pasted license text, use a license text scanner (e.g., *scancode-toolkit*) to identify SPDX identifiers.
2. Check PyPI registry metadata via API to cross-confirm license values when available.
3. Run all extracted values through an SPDX expression parser for final validation.

### Container Ecosystem — Docker
1. Crawl the Docker Hub or other registry description fields for free-text mentions of licenses.
2. Inspect image layers for the presence of `LICENSE` or similarly named files.
   - If found, scan the file with a license text identification tool to map it to SPDX.
   - Results will probably still be unreliable and incomplete, since no standard defines what the license of an image should represent.
3. Normalize any extracted license names or text into SPDX identifiers, and validate using an SPDX expression parser.
