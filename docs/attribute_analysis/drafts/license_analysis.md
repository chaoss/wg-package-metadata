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

### Java Ecosystem — Maven Central
**License Information Available**: Maven provides a structured `<licenses>` section in the `pom.xml` file. Each `<license>` element can contain: `<name>` (full legal name of the license), `<url>` (official URL for the license text), `<distribution>` (how the project may be distributed: `repo` or `manual`), and `<comments>` (additional information about the license). The Maven POM reference documentation recommends setting the `<name>` field to an SPDX identifier, though this is not enforced. Multiple `<license>` elements can be defined within the `<licenses>` section, and by convention they are interpreted as an OR relationship (i.e., the software may be used under any of the listed licenses).

While the POM.xml specification itself does not mandate license fields, Maven Central enforces additional publication requirements. To publish to Maven Central, the `<licenses>` section is required, and each `<license>` element must include both `<name>` and `<url>` fields. Maven Central does not validate whether the provided license information conforms to SPDX standards or any specific format beyond the presence of these required fields.

**References**:
- [Maven POM Reference — licenses section](https://maven.apache.org/pom.html)
- [Maven Central publication requirements](https://central.sonatype.org/publish/requirements/#required-pom-metadata)

### .NET Ecosystem — NuGet
**License Information Available**: NuGet provides structured license metadata in the `.nuspec` file through the `<license>` element, which supports SPDX license expressions or references to license files included within the package. The older `<licenseUrl>` element, which provided external URLs to license text, has been deprecated in favor of embedding license information directly in the package. When using an SPDX identifier, the `type="expression"` attribute is specified; when referencing a file, `type="file"` is used along with the file path within the package. NuGet.org (the primary NuGet registry) displays license information on package pages and encourages the use of SPDX identifiers for clarity and standardization.

**References**:
- [NuGet .nuspec file reference — license element](https://learn.microsoft.com/en-us/nuget/reference/nuspec#license)
- [NuGet license metadata deprecation announcement (2018)](https://github.com/NuGet/Announcements/issues/32)

### Ruby Ecosystem — RubyGems
**License Information Available**: RubyGems provides license metadata through the `license` and `licenses` attributes in the `.gemspec` file. The `license` attribute accepts a single license identifier (string), while the `licenses` attribute accepts an array of license identifiers for gems distributed under multiple licenses. RubyGems documentation recommends using SPDX identifiers (maximum 64 characters) for these fields to ensure standardization and clarity. However, these fields are optional, and RubyGems.org does not enforce SPDX format or validate the content of license declarations. The full license text is expected to be included as a file within the gem package.

**References**:
- [RubyGems Specification Reference — license/licenses attributes](https://guides.rubygems.org/specification-reference/#license=)

### macOS Ecosystem — Homebrew
**License Information Available**: Homebrew provides a `license` method in Formula files (Ruby DSL) to declare package licensing information. The method accepts SPDX identifiers as strings (e.g., `"MIT"`, `"Apache-2.0"`), with support for version operators (e.g., `"EPL-1.0+"` for "or later" versions). Special symbols include `:public_domain` for public domain software and `:cannot_represent` for licenses that cannot be expressed using SPDX.

Complex SPDX license expressions are represented using Ruby hash structures based on the SPDX License Expression Guidelines: `any_of:` for OR relationships, `all_of:` for AND relationships, and the hash syntax `"License" => { with: "Exception" }` for SPDX WITH operators (license exceptions). These structures can be arbitrarily nested to express complex licensing scenarios.

Homebrew/homebrew-core (the main tap) does not accept new formulae without a license. All licenses must use identifiers from the SPDX License List or be marked as `:public_domain` or `:cannot_represent`. Only formulae using Debian Free Software Guidelines (DFSG) licenses or released into the public domain are accepted into homebrew-core.

**References**:
- [Homebrew Formula Cookbook](https://docs.brew.sh/Formula-Cookbook)
- [Homebrew License Guidelines](https://docs.brew.sh/License-Guidelines)

### Perl Ecosystem — CPAN
**License Information Available**: CPAN (Comprehensive Perl Archive Network) provides a `license` field in the distribution metadata, defined in `META.json` or `META.yml` files following the CPAN::Meta::Spec specification. The `license` field is **mandatory** and must be an array containing at least one element.

License identifiers must be selected from a fixed list of predefined short names for common open source licenses (e.g., `perl_5`, `apache_2_0`, `mit`, `gpl_3`, `artistic_2`). The specification defines four special values for edge cases: `open_source` (for OSI-approved licenses not in the predefined list), `restricted` (for non-free/proprietary licenses), `unrestricted` (for public domain or similar), and `unknown` (when the license cannot be determined). Multiple licenses in the array indicate the distribution may be used under any of those licenses (OR relationship).

**Reference**:
- [CPAN::Meta::Spec — License field specification](https://metacpan.org/pod/CPAN::Meta::Spec)

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
- The `license` field in `composer.json` is the canonical source of license information, reflected consistently in Packagist and registry metadata.
- Ambiguity mainly arises from legacy packages that predate SPDX adoption or that omit the `license` field entirely.

#### .NET Ecosystem — NuGet
- **Accepted definitions**:
  - SPDX license identifiers and expressions (specified with `type="expression"` attribute in the `<license>` element).
  - Escape hatch: Reference to a license file within the package (specified with `type="file"` attribute and a file path).
  - Deprecated: The `<licenseUrl>` element that provided external URLs to license text, though this has been deprecated since 2018 in favor of embedding license information directly in packages using either `type="expression"` or `type="file"`.
- The `<license>` element is optional, meaning some packages may omit license information entirely.
- Ambiguity primarily arises from legacy packages that still use the deprecated `<licenseUrl>` element or packages that omit the `<license>` element altogether.
- When SPDX expressions are used with `type="expression"`, the license declaration is unambiguous and machine-readable.

#### macOS Ecosystem — Homebrew
- **Accepted definitions**:
  - SPDX identifiers as Ruby symbols (e.g., `:MIT`, `:Apache_2_0`, `:GPL_3_0_only`).
  - SPDX identifiers as strings (e.g., `"MIT"`, `"Apache-2.0"`).
  - Array of SPDX identifiers for multiple licenses.
  - Structured hash with `:any_of` key for OR relationships (e.g., `{ any_of: [:MIT, :Apache_2_0] }`).
  - Structured hash with `:all_of` key for AND relationships (e.g., `{ all_of: [:MIT, :Apache_2_0] }`).
- The `license` field is recommended but not strictly enforced, meaning some formulae may omit license information.
- The use of Ruby symbol notation and structured hashes provides clear, machine-readable representations of licensing including complex scenarios.
- Homebrew's approach explicitly supports SPDX identifiers and provides native structures for expressing AND/OR relationships without relying on SPDX expression syntax strings.

### Ambiguously specified

#### Perl Ecosystem — CPAN
- **Accepted definitions**:
  - License identifiers from a fixed predefined list of common open source licenses (e.g., `perl_5`, `apache_2_0`, `mit`, `gpl_3`, `artistic_2`, `bsd`, `lgpl_3_0`, etc.).
  - Four special values that introduce ambiguity:
    - `open_source`: Indicates an OSI-approved license not in the predefined list, but doesn't specify which one.
    - `restricted`: Indicates a non-free or proprietary license, without specifying the actual terms.
    - `unrestricted`: Indicates public domain or similar, without precise legal characterization.
    - `unknown`: Explicitly indicates the license cannot be determined.
  - The `license` field is mandatory and must be an array with at least one element.
  - Multiple licenses in the array represent an OR relationship (the distribution may be used under any of the listed licenses).
  - While the predefined list provides clear identifiers for common licenses, the four special values introduce significant ambiguity. Distributions using `open_source`, `restricted`, `unrestricted`, or `unknown` do not provide machine-readable or legally precise license information.
  - The fixed list does not correspond to SPDX identifiers, requiring translation for cross-ecosystem compatibility.

#### Ruby Ecosystem — RubyGems
- **Accepted definitions**:
  - Single SPDX identifier in the `license` field (recommended but not enforced).
  - Array of SPDX identifiers in the `licenses` field.
  - Free-form text strings (any string up to 64 characters is accepted).
  - Custom or non-standard license identifiers.
- The `license` and `licenses` fields are optional, meaning gems can be published without any license information.
- RubyGems.org does not validate whether the provided values are valid SPDX identifiers, allowing arbitrary strings to be used.
- When multiple licenses are specified in the `licenses` array, there is no formal specification of whether they represent an OR relationship, AND relationship, or alternatives. This is left to convention and package documentation.
- The lack of validation and optional nature of these fields means license information can be highly ambiguous, inconsistent, or completely absent.

#### Java Ecosystem — Maven Central
- **Accepted definitions**:
  - Free-form text for license names in the `<name>` field (SPDX identifiers are recommended but not enforced)
  - URL to license text in the `<url>` field
  - Multiple `<license>` elements, interpreted as an OR relationship by convention
- Maven Central requires the presence of `<licenses>` section with `<name>` and `<url>` fields for publication, but does not validate the content or format of these fields.
- The lack of SPDX enforcement and acceptance of arbitrary text for license names means license information can be ambiguous and inconsistent across packages.
- The lack of support for SPDX expressions and only supporting OR relationships by convention (rather than formal specification) encourages some corner cases to be wrongly specified. For example, dual-licensing with AND conditions, exceptions (e.g., `Apache-2.0 WITH LLVM-exception`), or more complex license relationships cannot be properly expressed and may be incorrectly represented as simple OR alternatives or conflated into ambiguous text descriptions.

#### Python Ecosystem — PyPI (pip)
- **Accepted definitions**:
  - SPDX identifiers and expressions (supported in Python > 3.17)
  - Free-form strings (e.g., "MIT License", "BSD-style")
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

### Java Ecosystem — Maven Central
- **Data type**: XML structure with a `<licenses>` container element that can hold multiple `<license>` elements. Each `<license>` element contains child elements for `<name>` (free-form text), `<url>` (URL string), `<distribution>` (enumerated value: `repo` or `manual`), and `<comments>` (free-form text).
- **License expression support**: No support for SPDX expressions. The format only allows free-form text in the `<name>` field, with SPDX identifiers recommended but not enforced. Multiple licenses are supported through multiple `<license>` elements, which by convention represent an OR relationship, but this is not formally specified and cannot express AND, WITH, or other SPDX operators.
- **Location**: Declared in `pom.xml` under the `<licenses>` section. The POM file is included in published artifacts (JAR, WAR, etc.) and is available from Maven Central and other Maven repositories. The POM is also distributed separately as a standalone artifact (`<artifactId>-<version>.pom`).
- **Notes**: Maven Central enforces the presence of the `<licenses>` section with `<name>` and `<url>` fields but does not validate the content, format, or accuracy of the license information. The lack of structured validation means license data quality depends entirely on maintainer diligence.

### .NET Ecosystem — NuGet
- **Data type**: XML structure with a `<license>` element that contains a `type` attribute (either `expression` or `file`) and text content. When `type="expression"`, the text content is an SPDX license identifier or expression. When `type="file"`, the text content is a path to a license file within the package. The deprecated `<licenseUrl>` element contained a URL string pointing to external license text.
- **License expression support**: Full support for SPDX identifiers and expressions when using `type="expression"`.
- **Location**: Declared in the `.nuspec` file under the `<metadata>` section. The `.nuspec` file is included at the root of the `.nupkg` package (which is a ZIP archive). When `type="file"` is used, the referenced license file must also be included in the package. Both the `.nuspec` metadata and any included license files are available when the package is downloaded from NuGet.org or other NuGet feeds.
- **Notes**: The `<license>` element is optional in the specification. NuGet.org validates SPDX expressions when `type="expression"` is used but does not enforce their presence. The transition from `<licenseUrl>` to `<license>` has improved the reliability of license metadata by embedding it within packages rather than relying on external URLs.

### Ruby Ecosystem — RubyGems
- **Data type**: The `.gemspec` file is a Ruby script (DSL - Domain Specific Language) that defines gem specifications. The `license` attribute accepts a single string value, while the `licenses` attribute accepts an array of strings. Each string can be an SPDX identifier (recommended), free-form text, or any custom string up to 64 characters.
- **License expression support**: No native support for SPDX expressions. Only individual SPDX identifiers can be specified, either as a single value in `license` or as multiple values in the `licenses` array. Complex licensing scenarios (AND, WITH, exceptions) cannot be expressed using the built-in metadata fields.
- **Location**: Declared in the `.gemspec` file, which is written in Ruby and located at the gem's root directory. When a gem is packaged and distributed, the `.gemspec` metadata is embedded within the `.gem` file (which is a tar archive). License files (typically named `LICENSE`, `LICENSE.txt`, or similar) are expected to be included in the gem package but this is not enforced. The metadata is extractable from the `.gem` file and is also served by RubyGems.org through its web interface and API.
- **Notes**: The `license` and `licenses` fields are optional, and no validation is performed on their content. Because the `.gemspec` is a Ruby script, it must be executed to extract metadata, which can pose security considerations. The lack of enforced standards means license data quality varies significantly across gems.

### macOS Ecosystem — Homebrew
- **Data type**: Formula files are Ruby scripts (DSL) that define package specifications. The `license` method accepts: SPDX identifier strings (e.g., `"MIT"`, `"Apache-2.0"`), special symbols (`:public_domain`, `:cannot_represent`), arrays for multiple licenses, hashes with `any_of:` or `all_of:` keys for complex expressions, and hash syntax for license exceptions (`"License" => { with: "Exception" }`).
- **License expression support**: Full native support for SPDX license expressions through structured Ruby data types based on the SPDX License Expression Guidelines. The `any_of:` hash key represents OR relationships, `all_of:` represents AND relationships, and the hash syntax `"License" => { with: "Exception" }` represents SPDX WITH operators for license exceptions (e.g., `"Apache-2.0" => { with: "LLVM-exception" }`). These structures can be arbitrarily nested to express any valid SPDX license expression. Version operators (`+`, `-only`, `-or-later`) are supported directly in license identifier strings.
- **Location**: Declared in Formula files (`.rb` Ruby scripts) located in Homebrew's formula repositories (homebrew-core, homebrew-cask, and third-party taps). The formula metadata is not embedded in installed packages but is maintained in Git repositories. Homebrew's API and web interface (formulae.brew.sh) serve this metadata. License information is stored in Homebrew's formula repositories and synced to the local system when formulae are updated.
- **Notes**: The `license` field is required for new formulae in homebrew-core. Formula files must be executed as Ruby code to extract metadata. Homebrew uses standard SPDX identifiers in string format, not Ruby symbol notation.

### Perl Ecosystem — CPAN
- **Data type**: JSON or YAML format in `META.json` or `META.yml` files following the CPAN::Meta::Spec. The `license` field is a mandatory array of strings, where each string must be a license identifier from the predefined list or one of the four special values (`open_source`, `restricted`, `unrestricted`, `unknown`).
- **License expression support**: No support for SPDX expressions or complex licensing scenarios. The array format only supports listing multiple licenses that represent an OR relationship. There is no way to express AND relationships, WITH operators for license exceptions, or other SPDX expression constructs. The predefined license identifiers use underscore notation (e.g., `apache_2_0`, `gpl_3`) rather than SPDX standard identifiers.
- **Location**: Declared in `META.json` (preferred) or `META.yml` files located at the distribution root. These metadata files are generated during the build process (by `ExtUtils::MakeMaker`, `Module::Build`, or other build tools) and included in the distribution tarball uploaded to CPAN. The metadata is extracted by CPAN indexers and made available through MetaCPAN and other CPAN search interfaces. Individual distribution tarballs can be downloaded and the META files extracted directly.
- **Notes**: The `license` field is mandatory in the CPAN::Meta::Spec version 2. The use of a fixed predefined list rather than SPDX identifiers means translation is required for cross-ecosystem compatibility. The four special values (`open_source`, `restricted`, `unrestricted`, `unknown`) provide escape hatches but sacrifice specificity and machine-readability.

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
- **CLI access**: The `composer show <package>` command displays the license field for installed packages. It retrieves this information from the local `composer.lock` file or the package's manifest.
- **Registry access**: Packagist displays license information on package pages. The values shown correspond directly to the `license` field declared in the source manifest.
- **API access**: The Packagist API exposes license information for each package version through its JSON endpoint, for example `https://repo.packagist.org/p/<vendor>/<package>.json`.

### Java Ecosystem — Maven Central
- **Direct access**: License information is available in the `pom.xml` file within the project source code. The POM file is also embedded within published artifacts (JAR, WAR, etc.) at `META-INF/maven/<groupId>/<artifactId>/pom.xml`, and is distributed as a separate `.pom` artifact alongside the main artifact.
- **CLI access**: The `mvn dependency:tree -Dverbose` can be used to list resolved dependencies and combined with POM inspection, though Maven does not provide a dedicated command to display only license information.
- **Registry access**: Maven Central's web interface at `https://central.sonatype.com` and legacy search at `https://search.maven.org` display license information on package pages, parsed from the POM metadata.
- **API access**: POM files can be retrieved directly from Maven Central using the repository URL pattern `https://repo1.maven.org/maven2/<groupId-as-path>/<artifactId>/<version>/<artifactId>-<version>.pom`. Maven Central also provides a REST API for searching artifacts, though license-specific queries are limited. Third-party services like MVNRepository (`https://mvnrepository.com`) provide additional search and API capabilities for license information.

### .NET Ecosystem — NuGet
- **Direct access**: License information is available in the `.nuspec` file within the package source code and at the root of the downloaded `.nupkg` package file. When `type="file"` is used, the license file is also included in the package at the specified path.
- **CLI access**: The `dotnet list package` command does not display license information. The `nuget.exe` tool does not provide a dedicated command for querying license metadata. However, the `.nuspec` file can be extracted from `.nupkg` files (which are ZIP archives) and parsed manually or with third-party tools.
- **Registry access**: NuGet.org displays license information prominently on package pages. The displayed information is parsed from the `<license>` element in the package's `.nuspec` file. For packages using `type="expression"`, the SPDX expression is shown directly. For packages using `type="file"`, a link to view the license file is provided.
- **API access**: The NuGet V3 API provides license metadata through the package metadata endpoint. License information can be accessed programmatically via `https://api.nuget.org/v3-flatcontainer/<package-id>/<version>/<package-id>.nuspec`. Additionally, the Search API returns license information in search results. The `.nupkg` package file can be downloaded and the `.nuspec` extracted for full license details.

### Ruby Ecosystem — RubyGems
- **Direct access**: License information is available in the `.gemspec` file within the gem's source code. The `.gemspec` metadata is also embedded within the `.gem` package file (tar archive) when distributed. License files are typically included in the gem package root directory but this is not enforced.
- **CLI access**: The `gem specification <gem-name> license` command displays the license field value for installed gems. 
- **Registry access**: RubyGems.org displays license information on each gem's page. The information shown is extracted from the `license` or `licenses` fields in the gem's metadata.
- **API access**: The RubyGems API provides license metadata through multiple endpoints. The Gems API (`https://rubygems.org/api/v2/runygems/<gem-name>/versions/<version>.json`) returns gem metadata including the `licenses` field as an array. Individual gem version data can also be retrieved. The `.gem` file can be downloaded and the `.gemspec` extracted programmatically to access full metadata including license information.

### macOS Ecosystem — Homebrew
- **Direct access**: License information is available in Formula files (`.rb` Ruby scripts) stored in Homebrew's formula repositories on GitHub (e.g., homebrew-core, homebrew-cask). These repositories can be cloned or browsed directly. The formula files are also synced locally when running `brew update`.
- **CLI access**: The `brew info <formula>` command displays license information along with other formula metadata. The output shows the license value as declared in the formula file. Additionally, `brew info --json=v2 <formula>` provides JSON output including license information for programmatic access.
- **Registry access**: The formulae.brew.sh website displays license information for each formula. The license is parsed from the formula's `license` attribute and displayed on the formula's page along with other metadata.
- **API access**: Homebrew provides a JSON API at `https://formulae.brew.sh/api/formula/<formula>.json` that includes license metadata. The API returns structured data including the license field. Formula files can also be accessed directly from GitHub repositories for detailed inspection.

### Perl Ecosystem — CPAN
- **Direct access**: License information is available in `META.json` or `META.yml` files within the distribution source or the distributed tarball. These files are located at the root of the distribution and can be read directly from the downloaded tarball or from the source repository.
- **CLI access**: CPAN clients such as `cpan` and `cpanm` can access license metadata, though they do not provide dedicated commands to display only license information. Tools like `cpan-outdated` or custom scripts using `CPAN::Meta` can programmatically extract license data from installed or available distributions.
- **Registry access**: MetaCPAN (https://metacpan.org) displays license information prominently on each distribution's page. The license data is extracted from the `META.json` or `META.yml` files and presented in a human-readable format. The interface shows both the license identifiers and provides links to license details.
- **API access**: MetaCPAN provides a comprehensive REST API (https://fastapi.metacpan.org) that exposes license metadata. Distribution information can be retrieved programmatically, including the license array. For example, `https://fastapi.metacpan.org/v1/release/<distribution>` returns JSON including the license field. The `META.json` or `META.yml` files can also be downloaded directly from CPAN mirrors.

## 6. Quality Assessment

The quality of license metadata across ecosystems varies widely, not only in terms of completeness but also in clarity and machine-readability. Below we evaluate coverage, reliability, and key limitations.

### Methodology

To assess the practical quality and machine-readability of license metadata, we analyzed real-world data from [Ecosyste.ms](https://ecosyste.ms/) (licensed under CC BY-SA 4.0). The analysis examined two sample sizes: the top 0.1% and top 1% most popular packages per ecosystem, ranked by download counts and usage metrics. For each package, we validated whether the declared license value could be successfully parsed as a valid SPDX expression using the `license-expression` library.

**Coverage Definition**: The percentage represents the proportion of packages that declare a valid SPDX license expression. Empty values, null entries, whitespace-only strings, and SPDX escape hatches are excluded from the "valid" count. Escape hatches such as `NONE`, `NOASSERTION`, `UNKNOWN`, and `SEE LICENSE IN` technically parse as valid SPDX but indicate that no license was declared or that a fallback mechanism was used rather than an actual machine-readable license declaration. This metric measures how effectively each ecosystem supports machine-readable license declarations in practice, not just in specification.

**Data Samples**: 
- Top 0.1% of packages per ecosystem: 2,132 packages across 27 ecosystems
- Top 1% of packages per ecosystem: 36,224 packages across 36 ecosystems
- Analysis date: November 26, 2025
- Full analysis results available in [`license_coverage_results.txt`](license_coverage_results.txt)
- Processed data available in [`licenses-0.1_processed.csv`](licenses-0.1_processed.csv) and [`licenses-1_processed.csv`](licenses-1_processed.csv)

**Sample Size Impact**: Comparing the two sample sizes reveals how license metadata quality varies with package popularity. In most ecosystems, the top 0.1% packages (the most popular) show comparable or slightly different coverage compared to the broader top 1% sample. Significant differences between samples can indicate that less popular packages have different metadata practices, either better (when maintainers are more careful) or worse (when packages are less actively maintained). Notable findings include ecosystems like Docker, Deno, and Pub which show 0% coverage due to lack of structured license metadata fields. Detailed per-ecosystem comparisons are provided in the coverage results.

### Rust Ecosystem — Cargo
- **Coverage**: 45.53% of packages in the top 1% have valid SPDX expressions (top 0.1%: insufficient sample size).
- **Reliability**: Mixed. While SPDX validation is enforced, many packages use the license file escape hatch rather than declaring SPDX expressions directly, resulting in lower machine-readable coverage than expected.
- **Limitations**:
  - When a license file is used instead of an SPDX expression, automated tooling must parse external text, which introduces variability.
  - The high use of escape hatches (54.47% of top 1% packages) indicates that while the specification supports SPDX, many maintainers opt for the license file mechanism.

### Python Ecosystem — PyPI (pip)
- **Coverage**: 60.29% of packages in the top 1% have valid SPDX expressions (top 0.1%: 58.06%).
- **Reliability**: Weak to mixed.
  - Newer projects (Python > 3.17, setuptools ≥ 66.0) can use SPDX identifiers and expressions, making license data machine-readable.
  - Older projects often use free-form text or inconsistent naming ("BSD-style", "GPLv2 or later"), which complicates parsing.
  - The relatively consistent coverage across both samples (~58-60%) indicates that license metadata practices are uniform across popularity levels.
- **Limitations**:
  - Backward compatibility means ambiguous license strings will remain in circulation for the foreseeable future.
  - Some projects include a `LICENSE` file in their source but leave the metadata blank, forcing consumers to rely on heuristics.

### Container Ecosystem — Docker
- **Coverage**: 0% (both top 0.1% and 1%). Docker does not provide structured license metadata fields.
- **Reliability**: Absent. Crawling image descriptions in registries is only a heuristic approach, and most descriptions do not include licensing information. The analysis confirms that 828 packages in the top 0.1% and 10,766 packages in the top 1% have no machine-readable license metadata.
- **Limitations**:
  - Registries like Docker Hub sometimes display licensing information in free-text descriptions, but this is inconsistent and not machine-readable.
  - Without structured metadata, automated compliance tooling cannot reliably determine licensing status.

### Go Ecosystem — Go Modules
- **Coverage**: 94.83% of packages in the top 1% have valid SPDX expressions (top 0.1%: 95.0%), as detected and normalized by ecosyste.ms from license files.
- **Reliability**: Good in practice despite weak specification. When conventional license files are used and remain unmodified, detection tools produce consistent results. Variations in file naming or content reduce accuracy. The consistently high coverage (~95%) across both samples indicates that the Go ecosystem has strong conventions around license file placement and content, enabling reliable heuristic detection.
- **Limitations**:
  - No structured license field in `go.mod` or module metadata.
  - License discovery depends entirely on file scanning and heuristic matching.
  - The [`pkg.go.dev`](https://pkg.go.dev/license-policy) classification can differ from results produced by local scanners, as it is based on an internal allowlist and redistributability policy.
  - No official `go` CLI command provides license information (see [cmd/go reference](https://pkg.go.dev/cmd/go)).

### JavaScript Ecosystem — npm
- **Coverage**: 95.98% of packages in the top 1% have valid SPDX expressions (top 0.1%: 96.94%).
- **Reliability**: Excellent. SPDX identifiers and expressions are widely adopted and validated during publication. The high and consistent coverage (~96-97%) across both samples demonstrates that npm's validation warnings effectively encourage proper SPDX usage. Minor inconsistencies remain due to legacy packages using custom text or missing declarations.
- **Limitations**:
  - The `license` field is not strictly enforced; non-SPDX values generate warnings but are still accepted.
  - Some older packages may contain ambiguous or incomplete license data.
  - License references using `SEE LICENSE IN` are excluded from our coverage metric as they represent an escape hatch, though they may point to valid license files in the package.

### PHP Ecosystem — Composer (Packagist)
- **Coverage**: 97.21% of packages in the top 1% have valid SPDX expressions (top 0.1%: 100%).
- **Reliability**: Excellent. SPDX identifiers/expressions are first-class in `composer.json`, arrays have clear `OR` semantics, and `proprietary` is an explicit escape hatch. Validation via `composer/spdx-licenses` effectively encourages proper SPDX usage. The very high coverage (97-100%) demonstrates strong community adoption of SPDX standards, with the most popular packages achieving perfect compliance.
- **Limitations**:
  - Non-SPDX expressions can be published despite warnings.
  - Some older packages may omit the `license` field or use nonstandard strings, though this is rare in practice.

### Java Ecosystem — Maven Central
- **Coverage**: TBD
- **Reliability**: Weak to mixed. While Maven Central requires the `<licenses>` section for publication, the lack of content validation results in highly inconsistent license data. Free-form text in the `<name>` field leads to variations like "Apache License 2.0", "Apache 2.0", "Apache-2.0", "ASL 2.0", and other permutations for the same license. Although SPDX identifiers are recommended, many packages use descriptive names, URLs, or informal abbreviations instead.
- **Limitations**:
  - No validation of license content or format—Maven Central only checks for the presence of required fields.
  - No support for SPDX expressions; complex licensing scenarios (AND, WITH, exceptions) cannot be properly expressed.
  - Multiple licenses are interpreted as OR by convention only, with no formal specification or machine-readable indication of the relationship.
  - License data quality is entirely dependent on individual maintainer diligence and awareness of best practices.
  - Historical packages may contain outdated license URLs, broken links, or references to deprecated license versions.
  - The `<url>` field is required but not validated, leading to inconsistent or non-existent URLs that cannot be reliably used for automated license text retrieval.

### .NET Ecosystem — NuGet
- **Coverage**: TBD
- **Reliability**: Good. Packages using the modern `<license>` element with `type="expression"` provide reliable, machine-readable SPDX license data. NuGet.org validates SPDX expressions when they are used, ensuring correctness. However, the optional nature of the `<license>` element means some packages omit license information entirely. Legacy packages may still use the deprecated `<licenseUrl>` element, which points to external URLs that may become stale or inaccessible over time.
- **Limitations**:
  - The `<license>` element is optional, allowing packages to be published without license information.
  - Legacy packages using the deprecated `<licenseUrl>` element rely on external URLs that may break, change, or become unavailable, making license information unreliable over time.
  - When `type="file"` is used, license information requires extracting and parsing the referenced file from the package, adding complexity to automated processing.
  - No enforcement mechanism to migrate legacy packages from `<licenseUrl>` to the modern `<license>` element, meaning both formats will coexist indefinitely.
  - Some older packages may have neither `<license>` nor `<licenseUrl>`, leaving license information completely unspecified.

### Ruby Ecosystem — RubyGems
- **Coverage**: TBD
- **Reliability**: Weak to mixed. While SPDX identifiers are recommended for the `license` and `licenses` fields, there is no validation or enforcement. Gems can specify arbitrary strings, use non-standard license names, or omit license information entirely. The quality of license metadata depends entirely on individual gem maintainer diligence and awareness of best practices.
- **Limitations**:
  - The `license` and `licenses` fields are optional, allowing gems to be published without any license information.
  - No validation of field content—any string up to 64 characters is accepted, including misspellings, custom abbreviations, or non-existent identifiers.
  - No support for SPDX expressions; complex licensing scenarios (AND, WITH, exceptions) cannot be properly expressed.
  - When multiple licenses are specified in the `licenses` array, there is no formal indication of their relationship (OR vs. AND), relying on convention and documentation.
  - The `.gemspec` file must be executed as Ruby code to extract metadata, which can pose security concerns and complicates automated parsing.
  - License files are expected but not enforced, meaning some gems may declare a license in metadata but not include the actual license text.
  - Historical gems may have outdated, inconsistent, or completely missing license information with no migration path.

### macOS Ecosystem — Homebrew
- **Coverage**: TBD
- **Reliability**: Strong. Homebrew formulae maintained in official taps (homebrew-core, homebrew-cask) generally have consistent and accurate license information. The use of Ruby symbols for SPDX identifiers provides compile-time checking and reduces typos. The structured hash format with `:any_of` and `:all_of` keys makes complex licensing relationships explicit and machine-readable.
- **Limitations**:
  - The `license` field is recommended but optional, meaning some formulae may omit license information, particularly in third-party taps.
  - Homebrew uses its own Ruby symbol notation for SPDX identifiers (`:Apache_2_0` instead of `Apache-2.0`), requiring translation to standard SPDX format for cross-ecosystem compatibility.
  - Formula files must be executed as Ruby code to extract metadata, which requires a Ruby interpreter and poses potential security considerations.
  - License information is maintained separately from installed packages in formula repositories, meaning it can become out of sync if formulae are updated without updating installed software.
  - Third-party taps may have inconsistent or missing license information compared to official Homebrew repositories.
  - Historical formulae may lack license information or use deprecated license identifier formats.

### Perl Ecosystem — CPAN
- **Coverage**: TBD
- **Reliability**: Mixed. The mandatory nature of the `license` field in CPAN::Meta::Spec version 2 ensures that all modern distributions include license metadata. However, the four special values (`open_source`, `restricted`, `unrestricted`, `unknown`) significantly reduce reliability. Distributions using these special values provide little to no actionable license information. The predefined list covers common open source licenses, but the lack of SPDX identifiers means the data requires translation for cross-ecosystem use.
- **Limitations**:
  - The four special values reduce data quality: `open_source` doesn't specify which license, `restricted` doesn't provide actual terms, `unrestricted` lacks precise legal characterization, and `unknown` explicitly indicates missing information.
  - The predefined list uses non-SPDX identifier notation (underscore-separated like `apache_2_0` instead of hyphen-separated SPDX like `Apache-2.0`), requiring translation.
  - No support for SPDX expressions means complex licensing scenarios (AND, WITH, exceptions) cannot be properly expressed.
  - Multiple licenses in the array are interpreted as OR by convention, but this is not formally specified in the metadata itself.
  - Older distributions using CPAN::Meta::Spec version 1 may have inconsistent or missing license information.
  - The predefined list may not include newer licenses or license versions, forcing use of the ambiguous `open_source` special value.
  - Build tools must correctly generate META files from distribution metadata; errors in this process can result in incorrect license information.

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
   - If it contains the `proprietary` value, treat it as a closed-source package. The license terms must be obtained manually from the package's website or vendor documentation, as no license file or metadata is expected in the code.
2. If multiple identifiers are declared in an array, interpret them as an `OR` expression and normalize to a valid SPDX format.
3. Validate the resulting SPDX expression using an SPDX parser.

### Java Ecosystem — Maven Central
1. Retrieve the POM file from the artifact, either from the source repository, from within the published artifact at `META-INF/maven/<groupId>/<artifactId>/pom.xml`, or directly from Maven Central using the repository URL pattern.
2. Parse the XML and extract all `<license>` elements within the `<licenses>` section.
3. For each `<license>` element, extract the `<name>` field content.
   - Attempt to match the license name to a known SPDX identifier using fuzzy matching or a lookup table of common variations (e.g., "Apache License 2.0" → `Apache-2.0`, "MIT License" → `MIT`).
   - If the `<name>` field is already an SPDX identifier, use it directly.
   - If fuzzy matching fails, use the `<url>` field (if present and valid) to retrieve the license text and apply a license text scanner (e.g., *scancode-toolkit*) to identify the SPDX identifier.
   - If both approaches fail, flag the license as unresolvable and retain the original free-form text for manual review.
4. If multiple `<license>` elements are present, combine them into an SPDX expression with `OR` operators, reflecting the conventional interpretation that the software may be used under any of the listed licenses.
5. Validate the resulting SPDX expression using an SPDX parser.

### .NET Ecosystem — NuGet
1. Retrieve the `.nuspec` file from the package, either from the source repository, by downloading the `.nupkg` file from NuGet.org and extracting it (it's a ZIP archive), or via the NuGet API.
2. Parse the XML and locate the `<license>` element within the `<metadata>` section.
3. Check the `type` attribute of the `<license>` element:
   - If `type="expression"`, extract the text content which contains an SPDX identifier or expression. Parse and validate it directly using an SPDX expression parser. No further steps are required.
   - If `type="file"`, continue with the steps below.
4. If `type="file"` is used:
   - Extract the file path from the text content of the `<license>` element.
   - Retrieve the license file from the package at the specified path.
   - Apply a license text scanner (e.g., *scancode-toolkit*) to identify the most likely SPDX identifier(s).
   - Convert the result into a valid SPDX expression.
5. If the deprecated `<licenseUrl>` element is present instead of `<license>`:
   - Attempt to retrieve the license text from the URL (if still accessible).
   - Scan the retrieved text with a license detection tool to map it to an SPDX identifier.
   - If the URL is inaccessible, flag the license as unresolvable and retain the URL for manual review.
6. Validate the resulting SPDX expression using an SPDX parser.

### Ruby Ecosystem — RubyGems
1. Retrieve the `.gemspec` file from the gem, either from the source repository, by downloading and extracting the `.gem` file (tar archive), or via the RubyGems API.
2. Parse the `.gemspec` file to extract the `license` and/or `licenses` fields. Note that this may require executing Ruby code or using a Ruby parser, as `.gemspec` files are Ruby scripts.
3. Check which field(s) are populated:
   - If the `license` field (singular) is present, extract its string value.
   - If the `licenses` field (plural array) is present, extract all string values from the array.
   - If both are present, prefer the `licenses` array as it can represent multiple licenses.
4. For each extracted license string:
   - Attempt to match it to a known SPDX identifier using exact matching (case-insensitive).
   - If exact matching fails, use fuzzy matching or a lookup table for common variations and misspellings (e.g., "apache 2.0" → `Apache-2.0`, "mit" → `MIT`).
   - If the license string is already a valid SPDX identifier, use it directly.
   - If matching fails, search for license files in the gem package (e.g., `LICENSE`, `LICENSE.txt`, `COPYING`) and scan them with a license text scanner (e.g., *scancode-toolkit*) to identify SPDX identifiers.
   - If all approaches fail, flag the license as unresolvable and retain the original string for manual review.
5. If multiple licenses are found (from the `licenses` array), combine them into an SPDX expression with `OR` operators, reflecting the common implicit convention that gems with multiple licenses allow use under any of them.
6. If no license information is present in the `.gemspec`, flag the gem as having no declared license.
7. Validate the resulting SPDX expression using an SPDX parser.

### macOS Ecosystem — Homebrew
1. Retrieve the Formula file from Homebrew's repositories, either by accessing the local formula repository (synced via `brew update`), from GitHub (e.g., `https://github.com/Homebrew/homebrew-core`), or via Homebrew's JSON API.
2. Parse the Formula file (Ruby script) to extract the `license` value. This requires either executing Ruby code or using a Ruby parser to extract the value.
3. Determine the format of the `license` value:
   - If it's a special symbol (`:public_domain` or `:cannot_represent`), handle accordingly.
   - If it's a string, check if it's a valid SPDX identifier (potentially with version operators like `+`, `-only`, or `-or-later`). Convert to standard SPDX format if needed.
   - If it's a hash with a string key and a `with:` value (e.g., `"Apache-2.0" => { with: "LLVM-exception" }`), convert to SPDX WITH syntax: `Apache-2.0 WITH LLVM-exception`.
   - If it's an array, continue to step 4.
   - If it's a hash with `any_of:` or `all_of:` keys, continue to step 5.
4. If the license is an array:
   - Process each element recursively using step 3 (handling strings, symbols, nested hashes with `with:`, etc.).
   - Combine the resulting SPDX expressions with `OR` operators.
5. If the license is a structured hash with `any_of:` or `all_of:`:
   - If the hash contains an `any_of:` key, extract the array value and process each element recursively using step 3.
   - Combine the results with `OR` operators.
   - If the hash contains an `all_of:` key, extract the array value and process each element recursively using step 3.
   - Combine the results with `AND` operators.
   - Handle arbitrarily nested structures (arrays within hashes, hashes within arrays, license exceptions within complex expressions) by applying these rules recursively.
6. If no license information is present in the Formula, flag the package as having no declared license.
7. Validate the resulting SPDX expression using an SPDX parser.

### Perl Ecosystem — CPAN
1. Retrieve the `META.json` or `META.yml` file from the distribution, either from the source repository, by downloading and extracting the distribution tarball from CPAN, or via the MetaCPAN API.
2. Parse the JSON or YAML file and extract the `license` field value. This field is mandatory and contains an array of license identifiers.
3. For each license identifier in the array:
   - Check if it's one of the four special values:
     - If `open_source`: Flag as an OSI-approved license that requires manual identification. Check for LICENSE files in the distribution and use a license text scanner to identify the actual license.
     - If `restricted`: Flag as proprietary/restricted. The actual license terms must be obtained from the distribution documentation or vendor.
     - If `unrestricted`: Flag as public domain or similar. Check for documentation clarifying the exact status.
     - If `unknown`: Flag as undetermined. Check for LICENSE files and documentation to manually identify the license.
   - If it's from the predefined list (e.g., `perl_5`, `apache_2_0`, `mit`, `gpl_3`), translate to the corresponding SPDX identifier using a mapping table (e.g., `apache_2_0` → `Apache-2.0`, `gpl_3` → `GPL-3.0`, `perl_5` → `Artistic-1.0-Perl OR GPL-1.0-or-later`).
4. If multiple licenses are present in the array (and none are special values), combine them into an SPDX expression with `OR` operators, reflecting CPAN's convention that multiple licenses represent alternatives.
5. If any special values were encountered, document the ambiguity and include the need for manual review or additional license file scanning.
6. Validate the resulting SPDX expression using an SPDX parser.
7. Note that CPAN distributions may also include LICENSE or COPYING files that should be checked to confirm or supplement the metadata, especially when special values are used.
