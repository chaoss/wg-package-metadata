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

### Go Ecosystem — Go Modules
**License Information Available**: No dedicated `license` field in `go.mod`. License information is inferred from license files (e.g., `LICENSE`) present in the module’s source and redistributed module ZIP; `pkg.go.dev` detects licenses heuristically. There is no official module proxy or `go` CLI endpoint that returns structured license metadata. However, the [`go-licenses`](https://github.com/google/go-licenses) tool can be used to extract and map license data from module sources, though its coverage and accuracy depend on file placement and text heuristics.

**References**:
- [Go Modules Reference](https://go.dev/ref/mod) — Module format and proxy behavior.
- [pkg.go.dev License Policy](https://pkg.go.dev/license-policy) — Heuristic detection and redistributable behavior, which mentions the internal catalog is build using [licensecheck](https://pkg.go.dev/github.com/google/licensecheck).
- [Go module proxy protocol](https://golang.org/ref/mod#protocol) — Lists `.mod`, `.info`, and `.zip` endpoints, confirming absence of a license field.
- Common tooling used in practice: [`licensecheck`](https://pkg.go.dev/golang.org/x/license) library and [`go-licenses`](https://github.com/google/go-licenses) CLI for detection and normalization.

### JavaScript Ecosystem — npm
**License Information Available**: The npm ecosystem provides a structured `license` field in `package.json`, which can contain an SPDX identifier or expression, with an escape hatch to reference a license file using the value `SEE LICENSE IN <filename>`. When a license file is present, it is typically named `LICENSE` or `LICENSE.md` and included in the published package tarball. The npm registry surfaces this metadata through both its web interface and JSON API. The publication process does not enforce SPDX or `SEE LICENSE IN` formats; it emits a warning from the [`validate-npm-package-license`](https://github.com/kemitchell/validate-npm-package-license) library but still accepts the package.

**References**:
- [npm package.json specification – license field](https://docs.npmjs.com/cli/v10/configuring-npm/package-json#license)
- [npm registry API reference](https://github.com/npm/registry/blob/main/docs/REGISTRY-API.md)

### PHP Ecosystem — Composer (Packagist)
**License Information Available**: Composer provides a structured `license` field in `composer.json`. It accepts an SPDX identifier, an SPDX expression using `and` or `or`, or an array of SPDX identifiers. The array form has a defined semantics of representing a sequence of `OR` alternatives, not an ambiguous list. For closed-source packages, an escape hatch is available via the value `proprietary`. Packagist surfaces this metadata on package pages and through its JSON API.
Composer validates license values against the SPDX list using the [`composer/spdx-licenses`](https://github.com/composer/spdx-licenses) library, but publication is not blocked for invalid values.

**References**:
- [Composer schema — license field](https://getcomposer.org/doc/04-schema.md#license)
- [composer/spdx-licenses validation library](https://github.com/composer/spdx-licenses)
- [Packagist API reference](https://packagist.org/apidoc)

## 3. Field Analysis

This section groups ecosystems according to how license information can be specified in their package metadata. The focus here is on whether the declaration is unambiguous, ambiguous, or not supported at all, along with the types of definitions that are accepted in practice.

### Unambiguously specified

#### Rust Ecosystem — Cargo
- **Accepted definitions**:
  - SPDX license identifiers
  - SPDX license expressions (e.g., `MIT OR Apache-2.0`)
  - Escape hatch: reference to a license file in the package repository
- Cargo enforces SPDX validation, which ensures unambiguous interpretation of declared licenses.

#### JavaScript Ecosystem — npm
- **Accepted definitions**:
  - SPDX license identifiers.
  - SPDX license expressions.
  - Escape hatch: reference to a license file using the value `SEE LICENSE IN <filename>`.
- npm validates license values during publication but does not enforce them. Non-SPDX strings trigger warnings from the [`validate-npm-package-license`](https://github.com/kemitchell/validate-npm-package-license) library, yet packages are still accepted.
- Ambiguity occurs when legacy packages use free-form text, custom license strings, or omit the `license` field entirely.
- The `package.json` metadata and any `LICENSE` files included in the package tarball together define the licensing information. Registry entries reflect whatever was provided at publish time.

#### PHP Ecosystem — Composer (Packagist)
- **Accepted definitions**:
  - SPDX license identifiers.
  - SPDX license expressions.
  - Escape hatch: `proprietary`, used for closed-source packages.
  - Array of SPDX identifiers, with a documented `OR` semantics.
- Composer validates declared licenses using the [`composer/spdx-licenses`](https://github.com/composer/spdx-licenses) library. Invalid identifiers or expressions trigger warnings but do not prevent publication.
- Ambiguity mainly arises from legacy packages that predate SPDX adoption or that omit the `license` field entirely.
- The `license` field in `composer.json` is the canonical source of license information, reflected consistently in Packagist and registry metadata.

### Ambiguously specified

#### Python Ecosystem — PyPI (pip)
- **Accepted definitions**:
  - SPDX identifiers and expressions (supported in Python > 3.17)
  - Free-form strings (e.g., “MIT License”, “BSD-style”)
  - Copy-paste of license text blocks
  - Historical community conventions where classifiers in `setup.py` or metadata loosely indicated license type
- The presence of multiple valid formats and lack of strict validation means license information can be ambiguous.

#### Go Ecosystem — Go Modules
- **Accepted definitions**:
  - License files such as `LICENSE` located in the module root or subdirectories.
  - License text recognized heuristically by tools such as [`licensecheck`](https://pkg.go.dev/golang.org/x/license) or [`go-licenses`](https://github.com/google/go-licenses), which identify known license patterns in source files.
- Go’s module tooling (`go` CLI, proxies, and `go.mod`) does not provide a structured field for declaring licenses.
- The `.mod` and `.info` files available via the [module proxy protocol](https://go.dev/ref/mod#goproxy-protocol) contain only module and version metadata, not license information.
- The [`pkg.go.dev`](https://pkg.go.dev/license-policy) service detects license information heuristically using [`licensecheck`](https://pkg.go.dev/golang.org/x/license).
- Because license detection depends on the presence and content of files rather than explicit declarations, license metadata in Go modules is ambiguous and not consistently machine-readable.

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

### Go Ecosystem — Go Modules
- **Data type**: Text files containing license text, typically named `LICENSE`, or similar.
- **License expression support**: Not supported. Go modules do not provide a field for SPDX identifiers or expressions in `go.mod` or related metadata.
- **Location**: License files are distributed as part of the module source and included in the module zip file available through proxies (for example, `https://proxy.golang.org/<module>/@v/<version>.zip`).
- The `.mod` file defines module dependencies but does not include licensing information. The `.info` file served by proxies contains version and timestamp metadata only, as defined in the [Go module proxy protocol](https://go.dev/ref/mod#goproxy-protocol).
- **Notes**: License information must be derived from file scanning. Detection accuracy depends on file placement and adherence to standard license naming and text conventions.

### JavaScript Ecosystem — npm
- **Data type**: String containing an SPDX identifier, SPDX expression, or a `SEE LICENSE IN` file reference.
- **License expression support**: SPDX identifiers and expressions are fully supported and documented in the npm specification.
- **Location**: Declared in `package.json` under the `license` field. If `SEE LICENSE IN` is used, the referenced license file (typically `LICENSE` or `LICENSE.md`) is included in the published package tarball. Both the manifest and the license file are available from the npm registry and the downloaded package.
- **Notes**: npm validates the license field format and issues warnings for invalid or non-SPDX values but does not block publication. The registry retains the license information as provided at publish time.

### PHP Ecosystem — Composer (Packagist)
- **Data type**: String containing an SPDX identifier or expression, an array of SPDX identifiers interpreted as an `OR` sequence, or the `proprietary` value used as an escape hatch for closed-source packages.
- **License expression support**: Full support for SPDX identifiers and expressions using `and` and `or` operators, as defined in the Composer schema.
- **Location**: Declared in `composer.json` under the `license` field. The manifest file is included in the distributed package and available through the Packagist registry and API.
- **Notes**: Composer validates license values during package installation and publication using the `composer/spdx-licenses` library. Invalid or unrecognized values produce warnings but do not block distribution.

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

### Go Ecosystem — Go Modules
- **Direct access**: License information is available in the source repository or within the module zip file downloaded from a module proxy. The license files can be read directly from these sources.
- **CLI access**: The `go` command does not provide a subcommand or flag to print license metadata.
- **Registry access**: The [`pkg.go.dev`](https://pkg.go.dev) website displays heuristically detected license information and marks modules as redistributable or non-redistributable based on recognized licenses.
- **API access**: The [module proxy protocol](https://go.dev/ref/mod#goproxy-protocol) serves `.mod`, `.zip`, and `.info` files but does not include license data. Programmatic license retrieval requires downloading the module source and scanning for license files.

### JavaScript Ecosystem — npm
- **Direct access**: License information is available in the `package.json` file within the source code and in the published tarball retrieved from the registry.
- **CLI access**: The `npm view <package> license` command displays the license field as published. Other npm commands, such as `npm info`, also expose this metadata locally.
- **Registry access**: The npm website displays license information on each package page. The license value shown corresponds to the data in the published `package.json`.
- **API access**: The npm registry JSON API provides the license field under each package version’s metadata. Both the manifest and license files can be retrieved programmatically (`curl https://registry.npmjs.org/<package-name>`).

### PHP Ecosystem — Composer (Packagist)
- **Direct access**: License information is available in the `composer.json` file within the package source. This file is included in distributed archives and mirrors.
- **CLI access**: The `composer show <package>` command displays the license field for installed packages. It retrieves this information from the local `composer.lock` file or the package’s manifest.
- **Registry access**: Packagist displays license information on package pages. The values shown correspond directly to the `license` field declared in the source manifest.
- **API access**: The Packagist API exposes license information for each package version through its JSON endpoint, for example `https://repo.packagist.org/p/<vendor>/<package>.json`.

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

### Go Ecosystem — Go Modules
- **Coverage**: TBD
- **Reliability**: Weak. When conventional license files are used and remain unmodified, detection tools produce consistent results. Variations in file naming or content reduce accuracy.
- **Limitations**:
  - No structured license field in `go.mod` or module metadata.
  - License discovery depends entirely on file scanning and heuristic matching.
  - The [`pkg.go.dev`](https://pkg.go.dev/license-policy) classification can differ from results produced by local scanners, as it is based on an internal allowlist and redistributability policy.
  - No official `go` CLI command provides license information (see [cmd/go reference](https://pkg.go.dev/cmd/go)).

### JavaScript Ecosystem — npm
- **Coverage**: TBD
- **Reliability**: Good. SPDX identifiers and expressions are widely adopted and validated during publication. Minor inconsistencies remain due to legacy packages using custom text or missing declarations. A secondary concern is that authors may bypass validation warnings and publish packages with nonstandard license values.
- **Limitations**:
  - The `license` field is not strictly enforced; non-SPDX values generate warnings but are still accepted.
  - Some older packages may contain ambiguous or incomplete license data.
  - License references using `SEE LICENSE IN` depend on the correctness and inclusion of the referenced file in the published package.

  ### PHP Ecosystem — Composer (Packagist)
- **Coverage**: TBD
- **Reliability**: Good. SPDX identifiers/expressions are first-class in `composer.json`, arrays have clear `OR` semantics, and `proprietary` is an explicit escape hatch. Validation via `composer/spdx-licenses` helps, but publication is not blocked for invalid values.
- **Limitations**:
  - Non-SPDX expressions can be published despite warnings.
  - Some older packages may omit the `license` field or use nonstandard strings.

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

### Go Ecosystem — Go Modules
1. Retrieve the module source or download the zip file from the module proxy.
2. Identify license files at the module root or common subdirectories.
3. Use a license scanner such as [`licensecheck`](https://pkg.go.dev/golang.org/x/license) or [`go-licenses`](https://github.com/google/go-licenses) to detect known license texts.
4. Map detected results to SPDX identifiers where possible.
5. Normalize multiple findings into an SPDX expression and validate with an SPDX parser.

### JavaScript Ecosystem — npm
1. Read the `license` field from `package.json`.
   - If it contains a valid SPDX identifier or expression, parse and validate it directly. No further steps are required.
   - If it uses the `SEE LICENSE IN` form, continue with the steps below.
2. Extract the referenced license file from the published package tarball.
3. Scan the file content with a license detection tool to map it to an SPDX identifier.
4. Normalize the detected value into a validated SPDX expression.

### PHP Ecosystem — Composer (Packagist)
1. Read the `license` field from `composer.json`.
   - If it contains a valid SPDX identifier or expression, parse and validate it directly. No further steps are required.
   - If it contains the `proprietary` value, treat it as a closed-source package. The license terms must be obtained manually from the package’s website or vendor documentation, as no license file or metadata is expected in the code.
2. If multiple identifiers are declared in an array, interpret them as an `OR` expression and normalize to a valid SPDX format.
3. Validate the resulting SPDX expression using an SPDX parser.
