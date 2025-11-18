# License Metadata Analysis

This document analyzes how different package managers handle license metadata across ecosystems.

## 1. Key findings summary

_TBD after sections 2–7 are finalized._

## 2. Data Collection Overview

This section provides an overview of the ecosystems and package managers reviewed to determine whether they make license information available as part of their metadata. For each package manager, we indicate the level of support for license data and point to the relevant specification or documentation. This establishes the foundation for deeper analysis in subsequent sections.

### C++ Ecosystem — Conan
**License Information Available**: Conan provides a `license` attribute in the `conanfile.py` (or `conanfile.txt` for simpler configurations). The `license` attribute accepts a string value that identifies the software license. While there is no strict format enforcement, the documentation recommends using SPDX identifiers for standardization and clarity. The `license` attribute is optional but strongly recommended for packages published to ConanCenter (the central public repository).

**Reference**:
- [Conan Reference: Conanfile Attributes](https://docs.conan.io/2/reference/conanfile/attributes.html)

### C++ Ecosystem — Vcpkg
**License Information Available**: Vcpkg provides a `license` field in the `vcpkg.json` manifest file. According to the vcpkg documentation, the `license` field should be either an SPDX 3.19 license expression or `null` as an escape hatch for licenses that cannot be expressed as SPDX (indicating users must read the deployed `/share/<port>/copyright` file). DocumentRefs are not supported. While this specification is not technically enforced through validation, it defines the expected format for the field. The license field is optional in `vcpkg.json`.

**Reference**:
- [vcpkg Reference: vcpkg.json manifest](https://learn.microsoft.com/en-us/vcpkg/reference/vcpkg-json)

### Clojure Ecosystem — Clojars (Leiningen)
**License Information Available**: Leiningen provides a `:license` key in the `project.clj` file that accepts a map with `:name` and `:url` keys to specify license information. When deploying to Clojars, Leiningen generates a `pom.xml` file that includes the license information in Maven POM format. Clojars uses this POM metadata to display license information. The `:license` field is optional in `project.clj`, and there is no validation of license format or content. The field accepts free-form text for both the name and URL.

**Reference**:
- [Leiningen Tutorial](https://github.com/technomancy/leiningen/blob/master/doc/TUTORIAL.md)

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

### JavaScript Ecosystem — npm / yarn
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

### Python Ecosystem — Conda
**License Information Available**: Conda provides multiple fields for license information within the `about` section of the `meta.yaml` file used to build conda packages:

- `license`: A free-form text string that specifies the license name. Accepts any string value without format enforcement or validation.
- `license_family`: Categorizes the license type. While there is no official exhaustive list, common values used by convention include `Apache`, `BSD`, `GPL`, `LGPL`, `MIT`, `Proprietary`, `Public Domain`, and `Other`.
- `license_file`: Specifies the path to a license text file to be included in the package.
- `license_url`: Provides a URL pointing to the license text.

All of these fields are optional in the specification. The combination of free-form text in `license`, optional categorization via `license_family`, and the ability to reference license content through either `license_file` or `license_url` provides flexibility but does not ensure consistency or machine-readability across packages.

**Reference**:
- [Conda Build — Define Metadata (meta.yaml)](https://docs.conda.io/projects/conda-build/en/latest/resources/define-metadata.html)

### Linux Ecosystem — dpkg (Debian/Ubuntu)
**License Information Available**: Debian packages include license information in the `debian/copyright` file within the source package, using a machine-readable format based on DEP-5 (Debian Enhancement Proposal 5). This file contains `License` fields that specify the license for each set of files in the package.

The machine-readable copyright format includes:
- `License` field with a short name (e.g., `GPL-2`, `MIT`, `Apache-2.0`, `BSD-3-clause`)
- Full license text in a separate paragraph below the `License` field
- Multiple `Files` stanzas for different licensing of different parts of the package
- Support for combining licenses using operators like `and`, `or`, with parentheses for complex expressions

While Debian encourages the use of common license short names (including SPDX-like identifiers), there is no strict enforcement of SPDX format. The format prioritizes human readability while maintaining machine parseability. The `debian/copyright` file is included in the source package but is also installed at `/usr/share/doc/<package>/copyright` in binary packages.

**Reference**:
- [Debian Policy Manual — Control files](https://www.debian.org/doc/debian-policy/ch-controlfields.html)
- [Debian Copyright Format 1.0 (DEP-5)](https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/)

### Linux Ecosystem — rpm (Red Hat/Fedora/SUSE)
**License Information Available**: RPM packages include a mandatory `License:` tag in the spec file that defines the package license. The spec file is used to build the RPM package and the license metadata is embedded in the resulting binary package.

As of July 2022, Fedora (a major RPM-based distribution) requires the `License:` field to contain an SPDX license expression that includes only Fedora-acceptable licenses. The expression must list all licenses that apply to the package's source code using SPDX operators:
- `AND` for packages containing code under multiple licenses
- `OR` for packages offering alternative licensing options
- `WITH` for license exceptions

Example: `License: MIT AND GPL-2.0-or-later` or `License: Apache-2.0 WITH LLVM-exception`

The actual license text files should be included in the package and marked with the `%license` directive in the `%files` section of the spec file. This ensures license texts are installed at `/usr/share/licenses/<package-name>/`. Other RPM-based distributions (Red Hat Enterprise Linux, CentOS, openSUSE) have varying degrees of SPDX adoption, with some still accepting free-form license strings.

**Reference**:
- [RPM Packaging Guide — Spec File Format](https://rpm.org/docs/4.20.x/manual/spec.html)
- [Fedora Licensing Guidelines](https://docs.fedoraproject.org/en-US/legal/license-field/)

### Linux Ecosystem — apk (Alpine Linux)
**License Information Available**: Alpine Linux packages specify license information in the `license` variable within the `APKBUILD` file (a shell script used to build Alpine packages).

The `license` variable contains a space-separated list of license identifiers. Alpine's conventions include:
- Use of SPDX license identifiers where possible (e.g., `MIT`, `GPL-2.0-or-later`, `Apache-2.0`)
- Custom licenses can be specified with the prefix `custom:` followed by a descriptive name (e.g., `custom:Proprietary`)
- For packages with multiple licenses, all applicable licenses are listed separated by spaces

Alpine policy requires the `license` field to be set for all packages. License files are typically included in the package at `/usr/share/licenses/<pkgname>/`. The APKBUILD metadata is not included in the binary package, but the license information is extracted and stored in the package index.

**Reference**:
- [Alpine Linux APKBUILD Reference](https://wiki.alpinelinux.org/wiki/APKBUILD_Reference)
- [Alpine Linux Package Policies](https://wiki.alpinelinux.org/wiki/Creating_an_Alpine_package)

### FreeBSD Ecosystem — Ports
**License Information Available**: FreeBSD Ports specify license information in the port's `Makefile` using structured variables:

- `LICENSE`: Specifies one or more short identifiers for the license(s) under which the port is distributed. FreeBSD maintains a predefined list of license identifiers in `Mk/bsd.licenses.db.mk`. Common identifiers include `MIT`, `GPLv2`, `GPLv3`, `APACHE20`, `BSD2CLAUSE`, `BSD3CLAUSE`, among others.
- `LICENSE_COMB`: Indicates how multiple licenses apply. Values include:
  - `single` (default): Only one license applies (used with a single license identifier)
  - `multi`: All licenses apply simultaneously (AND relationship)
  - `dual`: Any of the licenses may be chosen (OR relationship)
- `LICENSE_FILE`: Points to the file containing the full license text within the port's source tree
- `LICENSE_TEXT`: Contains the full license text directly within the `Makefile` (used when no separate file exists)
- `LICENSE_PERMS`: Defines permissions associated with the license (e.g., `dist-mirror`, `dist-sell`, `pkg-mirror`, `pkg-sell`, `auto-accept`)
- `LICENSE_NAME`: Provides the full name of a custom license (used when defining non-standard licenses)

The `LICENSE` variable is mandatory for ports. FreeBSD uses its own set of license identifiers rather than strict SPDX identifiers, though many align with SPDX conventions. For predefined licenses in the database, the framework automatically provides the license name, permissions, and often the license file location. Custom licenses not in the predefined list can be defined by setting `LICENSE_NAME`, `LICENSE_TEXT` or `LICENSE_FILE`, and `LICENSE_PERMS`.

**Reference**:
- [FreeBSD Porter's Handbook — Licenses](https://docs.freebsd.org/en/books/porters-handbook/)

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

#### Linux Ecosystem — rpm (Fedora)
- **Accepted definitions**:
  - SPDX license identifiers and expressions (mandatory in Fedora since July 2022)
  - SPDX operators: `AND`, `OR`, `WITH` for expressing complex licensing scenarios
  - Example: `MIT AND GPL-2.0-or-later`, `Apache-2.0 WITH LLVM-exception`
- Fedora strictly requires SPDX expressions in the `License:` field and validates that only Fedora-acceptable licenses are used.
- The license text files must be included in the package and marked with the `%license` directive.
- When SPDX expressions are used, the license declaration is unambiguous and machine-readable.
- **Note**: Other RPM-based distributions (Red Hat Enterprise Linux, CentOS, openSUSE) have varying degrees of SPDX adoption. Some still accept free-form license strings, making the ecosystem as a whole less consistent. However, Fedora's approach represents the strongest and most unambiguous license metadata specification among RPM distributions.

#### C++ Ecosystem — Vcpkg
- **Accepted definitions**:
  - SPDX 3.19 license expressions (specified format)
  - Escape hatch: `null` value for licenses that cannot be expressed as SPDX (indicating users must read the deployed `/share/<port>/copyright` file)
- When the specification is followed (SPDX expressions or `null`), the license declaration is unambiguous and machine-readable. The challenge is that non-conforming values can be introduced due to lack of enforcement.
- The `license` field is optional in `vcpkg.json`, meaning packages can be created without license information.

### Ambiguously specified

#### C++ Ecosystem — Conan
- **Accepted definitions**:
  - SPDX license identifiers (recommended but not enforced)
  - Free-form text strings (any string value accepted)
  - No support for SPDX license expressions with operators (AND, OR, WITH)
- The `license` attribute is optional, allowing packages to be published without license information.
- While Conan's documentation recommends using SPDX identifiers for standardization, there is no validation mechanism to enforce SPDX format or check identifier validity.
- ConanCenter (the central public repository) has submission guidelines that strongly recommend including license information, but this is a policy requirement rather than technical enforcement.
- When multiple licenses apply, there is no structured way to express the relationship (AND vs. OR)—multiple licenses would typically be listed as comma-separated or otherwise delimited text within the string, making the semantics ambiguous.
- The lack of validation and optional nature mean license information quality varies significantly across packages, depending on maintainer awareness and diligence.

#### Clojure Ecosystem — Clojars (Leiningen)
- **Accepted definitions**:
  - Free-form text in the `:license` map with `:name` and `:url` keys
  - Multiple licenses can be specified as a vector of maps, but the relationship between them (AND vs. OR) is not formally specified
- The `:license` field is optional in `project.clj`, allowing projects to be deployed without license information.
- There is no validation of license format or content—any string can be used for `:name` and `:url`.
- While the structure (`:name` and `:url`) provides some organization, the lack of standardization means license names can be arbitrary text, descriptive phrases, abbreviations, or SPDX identifiers depending on maintainer preference.
- Since Leiningen generates Maven POM files for Clojars deployment, the license information follows Maven's structure and inherits similar ambiguity issues (free-form `:name` field, optional `:url`).
- When multiple licenses are specified, there is no formal indication of their relationship (OR vs. AND), similar to Maven's convention-based interpretation.
- The lack of validation and optional nature mean license information quality varies significantly across packages, depending on maintainer awareness and adherence to common conventions.

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

#### Python Ecosystem — Conda
- **Accepted definitions**:
  - Free-form text string in the `license` field (any string value accepted without validation)
  - Conventional categorization via `license_family` field (e.g., `MIT`, `BSD`, `GPL`, `Apache`, `Proprietary`, `Public Domain`, `Other`)
  - Reference to license file via `license_file` field
  - URL to license text via `license_url` field
- All license-related fields are optional in the `meta.yaml` specification, meaning packages can be published without any license information.
- The `license` field accepts arbitrary text without format enforcement or validation against SPDX identifiers.
- The `license_family` field has no official exhaustive list, it accepts any text, with common values used only by convention.
- There is no support for expressing complex license relationships (AND, OR, WITH) through structured syntax or SPDX expressions.
- The combination of optional fields, free-form text, and lack of validation means license information can be highly ambiguous, inconsistent, or completely absent across conda packages.

#### Linux Ecosystem — dpkg (Debian/Ubuntu)
- **Accepted definitions**:
  - License short names in the `License` field of `debian/copyright` file (e.g., `GPL-2`, `MIT`, `Apache-2.0`, `BSD-3-clause`)
  - Operators: `and`, `or`, with parentheses for grouping (e.g., `GPL-2 or GPL-3`, `(MIT or BSD-2-Clause) and GPL-2`)
  - Full license text included in the copyright file below the License field
  - Multiple Files stanzas with different licenses for different parts of the package
- While Debian encourages the use of common license short names similar to SPDX identifiers, there is no strict enforcement or validation of SPDX format.
- The DEP-5 machine-readable format prioritizes human readability while maintaining machine parseability, but allows for variations and free-form text in license names.
- License names do not have to exactly match SPDX identifiers (e.g., `GPL-2+` is often used instead of `GPL-2.0-or-later`).
- The format is semi-structured, providing better clarity than pure free-form text but lacking the strict validation that would make it fully unambiguous.
- The `debian/copyright` file is mandatory for Debian packages, but the quality and accuracy of license declarations depend on maintainer diligence.

#### Linux Ecosystem — apk (Alpine Linux)
- **Accepted definitions**:
  - SPDX license identifiers (recommended, e.g., `MIT`, `GPL-2.0-or-later`, `Apache-2.0`)
  - Space-separated list for packages with multiple licenses
  - Custom licenses with `custom:` prefix (e.g., `custom:Proprietary`, `custom:CompanyName`)
- Alpine policy requires the `license` field to be set for all packages, making it mandatory.
- While SPDX identifiers are encouraged, there is no strict validation or enforcement of SPDX format.
- The `custom:` prefix provides an escape hatch for non-SPDX licenses but introduces ambiguity since the text after the prefix is free-form.
- When multiple licenses are listed (space-separated), the relationship between them (AND vs. OR) is not explicitly specified in the format, relying on convention or package documentation.
- The APKBUILD format does not support SPDX expression operators (AND, OR, WITH), limiting the ability to express complex licensing scenarios unambiguously.

#### FreeBSD Ecosystem — Ports
- **Accepted definitions**:
  - FreeBSD-specific license identifiers from the predefined list in `Mk/bsd.licenses.db.mk` (e.g., `MIT`, `GPLv2`, `GPLv3`, `APACHE20`, `BSD2CLAUSE`, `BSD3CLAUSE`)
  - Multiple licenses with explicit combination semantics via `LICENSE_COMB`:
    - `single` (default): Single license applies
    - `multi`: All licenses apply (AND relationship)
    - `dual`: Any license may be chosen (OR relationship)
  - Custom licenses defined via `LICENSE_NAME`, `LICENSE_TEXT` or `LICENSE_FILE`, and `LICENSE_PERMS`
- The `LICENSE` variable is mandatory for all ports.
- FreeBSD uses its own set of license identifiers rather than strict SPDX identifiers, though many identifiers align with SPDX conventions (e.g., `MIT`, `BSD2CLAUSE`), while others use different naming (e.g., `GPLv2` instead of `GPL-2.0-only`, `APACHE20` instead of `Apache-2.0`).
- The `LICENSE_COMB` variable provides explicit support for expressing AND/OR relationships between multiple licenses, making the semantics unambiguous. However, the non-SPDX identifier naming introduces ambiguity for cross-ecosystem use.
- FreeBSD's predefined license database provides consistency within the FreeBSD ecosystem, but requires translation to SPDX identifiers for broader interoperability.
- No support for SPDX WITH operators (license exceptions) through the structured variables, though exceptions could be defined as custom licenses.

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

### C++ Ecosystem — Conan
- **Data type**: String in the `license` attribute of `conanfile.py` (or `conanfile.txt`). Accepts free-form text without validation.
- **License expression support**: No support for structured SPDX expressions with operators (AND, OR, WITH). The `license` attribute is a simple string field. Multiple licenses must be represented as delimited text within the single string (e.g., "MIT, Apache-2.0"), with no formal specification of the delimiter or semantics (AND vs. OR).
- **Location**: Declared in `conanfile.py` or `conanfile.txt` in the package source. The conanfile is included in the package recipe uploaded to Conan repositories (local or ConanCenter). When a package is installed, the license information from the conanfile is stored in the package metadata in the local Conan cache. Conan's package metadata JSON files (stored in `~/.conan2/p/` or similar paths) include the license information. License text files (e.g., `LICENSE`, `COPYING`) are typically included in the package source but are not part of the conanfile metadata structure.
- **Notes**: The optional nature of the `license` attribute and lack of validation means packages may have no license information, SPDX identifiers, free-form text, or any combination. The lack of structured expression support makes complex licensing scenarios (AND, OR, exceptions) ambiguous. ConanCenter has stricter guidelines requiring license information, but technical enforcement is limited.

### C++ Ecosystem — Vcpkg
- **Data type**: String or `null` in the `license` field of `vcpkg.json`. The specification states it should be an SPDX 3.19 license expression or `null` as an escape hatch, but any string value is technically accepted due to lack of validation.
- **License expression support**: The specification requires SPDX 3.19 license expressions (supporting operators like `OR`, `AND`, `WITH`), with `null` as an escape hatch for licenses that cannot be expressed as SPDX. However, there is no validation to enforce correct SPDX expression format. In practice, the field can contain SPDX expressions, SPDX identifiers, free-form text, or `null`.
- **Location**: Declared in `vcpkg.json` manifest file at the root of the port directory in the centralized vcpkg ports repository on GitHub (e.g., `ports/<package>/vcpkg.json` in https://github.com/microsoft/vcpkg). When vcpkg installs a package, the manifest metadata is stored locally in the vcpkg installation directory. When `license` is `null` (the escape hatch), the copyright file is expected at `/share/<port>/copyright` in the installed package, providing license information for cases where SPDX expressions are insufficient. License text files are typically in the package source and are installed to the package's installation directory. The vcpkg binary cache (when used) includes the package's license files. Unlike package managers with registry services (e.g., ConanCenter, npm registry), vcpkg uses a file-based approach in a GitHub repository rather than a database-backed registry service with web UI and API.
- **Notes**: The optional `license` field means packages can be created without license information. The gap between the specification (SPDX 3.19 expressions with `null` escape hatch) and reality (no validation, any string accepted) means license data quality varies widely. The `null` escape hatch provides a standardized way to indicate that license information must be obtained from the copyright file, but doesn't provide structured, machine-readable metadata in the manifest itself. The lack of validation means SPDX expressions may be malformed, free-form text may be used, or the field may not conform to the documented specification.

### Clojure Ecosystem — Clojars (Leiningen)
- **Data type**: Clojure map (hash-map) in the `:license` key of `project.clj`. The map contains `:name` and `:url` keys with string values. Multiple licenses are specified as a vector of maps.
- **License expression support**: No support for SPDX expressions with operators (AND, OR, WITH). Multiple licenses are listed as separate map entries in a vector, but the relationship between them (AND vs. OR) is not formally specified in the format. By convention, multiple licenses typically represent OR relationships (similar to Maven), but this is not enforced or documented in the format itself.
- **Location**: Declared in `project.clj` at the project root. When deploying to Clojars, Leiningen generates a `pom.xml` file that includes license information in Maven's `<licenses>` format. The POM file is stored in Clojars' Maven-compatible repository structure. License metadata is displayed on Clojars.org web pages. License text files (e.g., `LICENSE`, `COPYING`) are typically included in the project source and distributed in JARs but are not part of the `project.clj` metadata structure.
- **Notes**: The optional `:license` field means projects can be deployed without license information. The free-form nature of the `:name` and `:url` fields means license declarations can range from SPDX identifiers to descriptive phrases to arbitrary text. Since Clojars is built on Maven infrastructure, license metadata quality shares similar issues with Maven Central—lack of validation, inconsistent naming, and ambiguous semantics for multiple licenses.

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

### Python Ecosystem — Conda
- **Data type**: YAML format in `meta.yaml` files used to build conda packages. The `about` section contains four optional license-related fields: `license` (free-form text string), `license_family` (free-form text string for categorization), `license_file` (string specifying path to a license file), and `license_url` (string specifying a URL to license text).
- **License expression support**: No support for SPDX expressions or structured complex licensing scenarios. The `license` field accepts arbitrary text without validation. There is no way to express AND, OR, or WITH relationships through structured syntax.
- **Location**: Declared in `meta.yaml` files located at the root of conda recipe directories. These recipe files are used during the build process to create conda packages (`.tar.bz2` or `.conda` archives). The resulting package metadata is indexed and made available through Anaconda.org, conda-forge, and other conda channels. When a package is installed, metadata is stored locally but the original `meta.yaml` is not typically included in the installed package itself—it remains in the recipe repository.
- **Notes**: All license-related fields are optional in the conda-build specification, meaning packages can be built and published without any license information. The free-form nature of both `license` and `license_family` fields, combined with lack of validation, means license information varies widely in format and quality across conda packages. The `license_file` and `license_url` fields provide alternative ways to reference license content but do not improve machine-readability of the license terms themselves.

### Linux Ecosystem — dpkg (Debian/Ubuntu)
- **Data type**: Machine-readable text format in the `debian/copyright` file following the DEP-5 (Debian Copyright Format 1.0) specification. The file contains structured paragraphs with `License:` fields containing short names and full license text.
- **License expression support**: Supports expressing multiple licenses using `and`, `or` operators with parentheses for grouping complex expressions (e.g., `GPL-2 or GPL-3`, `(MIT or BSD-2-Clause) and GPL-2`). While similar to SPDX expressions, the format is not identical—Debian uses its own conventions (e.g., `GPL-2+` instead of `GPL-2.0-or-later`).
- **Location**: The `debian/copyright` file is located in the source package under the `debian/` directory. It is also installed in binary packages at `/usr/share/doc/<package>/copyright`. The file can contain multiple `Files:` stanzas, each with its own `License:` and `Copyright:` fields, allowing different licenses for different parts of the package. License text must be included directly in the copyright file or referenced from `/usr/share/common-licenses/` for well-known licenses.
- **Notes**: The DEP-5 format is mandatory for Debian packages but not all packages use the fully machine-readable format—some older packages may use prose-style copyright files. The format prioritizes human readability while maintaining machine parseability. License short names are encouraged to match common conventions but there is no strict validation against SPDX or any other standard list.

### Linux Ecosystem — rpm (Red Hat/Fedora/SUSE)
- **Data type**: String in the `License:` tag of the RPM spec file. In Fedora (since July 2022), this must be a valid SPDX license expression. In other RPM-based distributions, it may be free-form text.
- **License expression support**: Fedora requires full SPDX expression support with `AND`, `OR`, and `WITH` operators (e.g., `MIT AND GPL-2.0-or-later`, `Apache-2.0 WITH LLVM-exception`). Other RPM distributions have varying degrees of SPDX support—some accept SPDX expressions, others accept free-form license names.
- **Location**: Declared in the spec file (`.spec`) under the `License:` tag in the package header. The spec file is used to build the RPM package, and the license metadata is embedded in the binary RPM package header as metadata. License text files should be included in the package and installed at `/usr/share/licenses/<package-name>/` using the `%license` directive in the `%files` section. The license metadata is queryable using `rpm -qi <package>` and is accessible through package manager APIs and repositories.
- **Notes**: The `License:` tag is mandatory in RPM packages. Fedora validates SPDX expressions and requires only Fedora-acceptable licenses. Other RPM-based distributions may have different validation policies or no validation at all. The embedded metadata in the RPM package header ensures license information is always available with the installed package, unlike some other ecosystems where metadata is only in the source.

### Linux Ecosystem — apk (Alpine Linux)
- **Data type**: String variable `license` in the APKBUILD shell script. Contains a space-separated list of license identifiers.
- **License expression support**: No support for SPDX expression operators (AND, OR, WITH). Multiple licenses are listed as space-separated identifiers, but the relationship between them (AND vs. OR) is not formally specified. SPDX identifiers are recommended but not enforced. The `custom:` prefix can be used for non-standard licenses (e.g., `custom:Proprietary`).
- **Location**: Declared in the `APKBUILD` file (a shell script) located in the Alpine package repository. The APKBUILD is not included in the binary package itself. During the build process, license metadata is extracted from the APKBUILD and stored in the package index (APKINDEX). License files are typically included in the package at `/usr/share/licenses/<pkgname>/`. The license metadata is available through the APK package manager (`apk info <package>`), the package index, and Alpine's package search website.
- **Notes**: The `license` field is mandatory in Alpine Linux packages. While SPDX identifiers are encouraged, there is no validation mechanism. The format is simple but limited—complex licensing scenarios cannot be expressed unambiguously due to the lack of structured operators. The space-separated format is compact but requires convention or documentation to clarify whether multiple licenses represent AND or OR relationships.

### FreeBSD Ecosystem — Ports
- **Data type**: Structured variables in the port's `Makefile`. The `LICENSE` variable contains one or more FreeBSD license identifiers (space-separated when multiple). The `LICENSE_COMB` variable indicates the relationship between multiple licenses.
- **License expression support**: Support for expressing license combinations through the `LICENSE_COMB` variable with three explicit values:
  - `single` (default): One license applies
  - `multi`: All licenses apply (AND relationship, e.g., `LICENSE=MIT GPLv2 LICENSE_COMB=multi` means MIT AND GPLv2)
  - `dual`: Choice of licenses (OR relationship, e.g., `LICENSE=MIT GPLv2 LICENSE_COMB=dual` means MIT OR GPLv2)
  - No native support for SPDX WITH operators (license exceptions). Exceptions would need to be defined as custom licenses or included in the license text/file.
- **Location**: Declared in the port's `Makefile` located in the ports tree (e.g., `/usr/ports/category/portname/Makefile`). The Makefile is the source of truth for port metadata during building. License identifiers reference a predefined database (`Mk/bsd.licenses.db.mk`) that provides license names, permissions, and often default license file locations. The `LICENSE_FILE` variable can point to license text files within the port's work directory (extracted from source). The `LICENSE_TEXT` variable can contain license text directly in the Makefile for cases where no separate file exists. License metadata is embedded in the resulting binary package and accessible via `pkg` tools. FreshPorts and other web interfaces display license information parsed from port Makefiles.
- **Notes**: The `LICENSE` variable is mandatory for all ports. FreeBSD uses its own predefined set of license identifiers rather than strict SPDX identifiers, though many align (e.g., `MIT`) while others differ (e.g., `GPLv2`, `APACHE20`). The `LICENSE_COMB` mechanism provides unambiguous AND/OR semantics for multiple licenses through explicit variable values. However, the non-SPDX naming requires translation for cross-ecosystem use. The `LICENSE_PERMS` variable defines distribution and selling permissions, providing additional metadata not commonly found in other ecosystems. Custom licenses can be fully defined within a port using `LICENSE_NAME`, `LICENSE_TEXT`/`LICENSE_FILE`, and `LICENSE_PERMS`, allowing flexibility beyond the predefined list.

## 5. Access Patterns

Access to license metadata varies across ecosystems. Some make it directly available from the project source or distribution, while others rely on registry infrastructure or provide no access at all.

### C++ Ecosystem — Conan
- **Direct access**: License information is available in the `conanfile.py` or `conanfile.txt` file within the package source. When packages are installed, license metadata is stored in Conan's local cache (e.g., `~/.conan2/p/<package>/metadata`) as JSON files that can be read directly. License text files in the package source can also be accessed if included.
- **CLI access**: The `conan inspect <reference>` command displays package metadata including the license field. The `conan list <reference>` command can also show package information. These commands work with both remote repositories and locally installed packages. The output shows the license value as declared in the conanfile.
- **Registry access**: ConanCenter (https://conan.io/center/) provides a web interface for browsing packages with license information displayed on each package page. The license information shown is extracted from the package's conanfile metadata. Third-party Conan repositories may also provide web interfaces, but this varies by repository.
- **API access**: Conan repositories provide REST APIs for querying package metadata. ConanCenter exposes package information through its API, including license data. The Conan client can query remote repositories programmatically using the Conan Python API. Package recipe files (conanfiles) can be downloaded from repositories and parsed to extract license information. The Conan v2 API provides methods to access package metadata from both local cache and remote repositories.

### C++ Ecosystem — Vcpkg
- **Direct access**: License information is available in the `vcpkg.json` manifest file in the vcpkg ports repository (https://github.com/microsoft/vcpkg). The ports repository can be cloned locally, and manifest files are plain JSON that can be read with any text editor or JSON parser. When vcpkg installs a package, the manifest is stored in the vcpkg installation directory. License text files from the package source are installed to the package's installation prefix (e.g., `vcpkg_installed/<triplet>/share/<package>/`).
- **CLI access**: The `vcpkg search <package>` command can display package information, though license information may not be shown in the summary output. The manifest file can be read directly using file system commands (e.g., `cat ports/<package>/vcpkg.json`). The `vcpkg list` command shows installed packages but does not display license information in its output. Accessing license metadata typically requires reading the `vcpkg.json` file directly or checking the installed license files.
- **Registry access**: Vcpkg does not provide a web-based registry service equivalent to ConanCenter, npm registry, or PyPI. Package information is stored in the centralized vcpkg ports repository on GitHub (https://github.com/microsoft/vcpkg). Users can browse the repository online to view `vcpkg.json` files and see license information. Some third-party tools and websites provide searchable interfaces to vcpkg ports, but these are community efforts rather than official Microsoft-provided registry infrastructure.
- **API access**: Vcpkg does not provide a dedicated REST API for querying package metadata. However, the centralized ports repository can be accessed via GitHub's API to retrieve `vcpkg.json` files programmatically. The vcpkg repository structure is file-based, so package metadata must be extracted by parsing JSON files from the repository. Tools can clone the vcpkg repository and programmatically read manifest files to aggregate license information across ports.

### Clojure Ecosystem — Clojars (Leiningen)
- **Direct access**: License information is available in the `project.clj` file within the project source. When projects are packaged as JARs, the license metadata is embedded in the generated `pom.xml` file included in the JAR at `META-INF/maven/<group-id>/<artifact-id>/pom.xml`. License text files (e.g., `LICENSE`) are typically included in the project root and distributed in the JAR.
- **CLI access**: Leiningen itself does not provide a dedicated command to display only license information. The `lein pom` command generates a `pom.xml` file that includes license metadata, which can then be inspected. For installed dependencies, the `pom.xml` files in the local Maven repository (`~/.m2/repository/`) can be read to access license information.
- **Registry access**: Clojars.org provides a web interface for browsing packages with license information displayed on each package page when available. The license information is extracted from the `pom.xml` metadata generated by Leiningen during deployment.
- **API access**: Clojars does not provide a dedicated REST API for querying package metadata. However, since Clojars is Maven-compatible, `pom.xml` files can be retrieved directly from the repository using Maven repository URL patterns (e.g., `https://repo.clojars.org/<group-id>/<artifact-id>/<version>/<artifact-id>-<version>.pom`). The Clojars search interface provides some programmatic access, but license-specific queries are limited.

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

### Python Ecosystem — Conda
- **Direct access**: License information is available in `meta.yaml` files within conda recipe directories (e.g., on GitHub for conda-forge recipes). The original `meta.yaml` files are not included in installed packages, but metadata extracted from them is stored in the installed package's `info` directory as JSON files.
- **CLI access**: The `conda search <package> --info` command displays package metadata including license information for packages available in configured channels. The `conda list --show-channel-urls` command shows installed packages but does not display license information directly. For installed packages, license metadata can be read from JSON files in the conda environment's `conda-meta/` directory (e.g., `<env>/conda-meta/<package>-<version>-<build>.json`).
- **Registry access**: Anaconda.org displays license information on package pages when provided by package maintainers. The conda-forge website and individual package pages also show license information extracted from package metadata. However, the display format and availability depend on whether maintainers populated the license fields in their recipes.
- **API access**: Anaconda.org provides an API for querying package metadata, accessible at endpoints like `https://api.anaconda.org/package/<channel>/<package>`. The API returns JSON including license information when available. The conda channels serve package metadata as JSON through repodata files (e.g., `https://conda.anaconda.org/<channel>/<platform>/repodata.json`), which include license information for packages in that channel. Individual package metadata can also be extracted from downloaded package archives.

### Linux Ecosystem — dpkg (Debian/Ubuntu)
- **Direct access**: License information is available in the `debian/copyright` file located in the source package under the `debian/` directory. For installed packages, the copyright file is available at `/usr/share/doc/<package>/copyright`. The file can be read directly using standard file tools (`cat`, `less`, etc.).
- **CLI access**: The `dpkg -L <package> | grep copyright` command can locate the copyright file for installed packages. `apt show <package>` displays package metadata but does not include license information directly. The `apt-file` tool can search for files across packages. License information must be read from the copyright file manually or with custom scripts that parse the DEP-5 format.
- **Registry access**: The Debian package tracker (https://tracker.debian.org/pkg/<package>) provides links to package information including the copyright file. Ubuntu's Launchpad (https://launchpad.net/ubuntu/+source/<package>) provides similar functionality. The copyright files can be browsed online through package source browsers.
- **API access**: The Debian API (https://sources.debian.org/src/) and Ubuntu's Launchpad API provide programmatic access to package metadata and source files, including copyright files. The copyright file can be retrieved from package sources via these APIs. Additionally, package repositories serve `.deb` files that can be downloaded and extracted (they are `ar` archives containing control and data tarballs) to access the copyright file at `usr/share/doc/<package>/copyright`.

### Linux Ecosystem — rpm (Red Hat/Fedora/SUSE)
- **Direct access**: License information is embedded in the RPM package header metadata and is always available with installed packages. The license text files are installed at `/usr/share/licenses/<package-name>/` when packages use the `%license` directive. The spec file (source of license metadata) is typically not included in binary packages but is available in source RPMs (SRPMs).
- **CLI access**: The `rpm -qi <package>` command displays package information including the `License` field for installed packages. The `dnf info <package>` (Fedora/RHEL) or `yum info <package>` (older systems) or `zypper info <package>` (openSUSE) commands display similar information for both installed and available packages. These commands directly query the RPM database or repository metadata.
- **Registry access**: Package repository web interfaces display license information parsed from RPM metadata. Examples include Fedora Packages (https://packages.fedoraproject.org/), Red Hat Package Browser, and openSUSE Software portal. These sites display the `License:` field value along with other package metadata.
- **API access**: Repository metadata is available through repodata XML/SQLite files served by RPM repositories. Tools like `dnf repoquery --info <package>` provide programmatic access to package metadata including licenses. The `rpm` command can also query remote packages via URLs. Third-party services like Repology (https://repology.org/) aggregate package metadata including licenses across multiple RPM-based distributions.

### Linux Ecosystem — apk (Alpine Linux)
- **Direct access**: License information is stored in the package index (APKINDEX) and embedded in package metadata. For installed packages, the APKBUILD source file (containing the original `license` variable) is not included, but license files are typically installed at `/usr/share/licenses/<pkgname>/`. The package index file can be read from Alpine mirrors.
- **CLI access**: The `apk info <package>` command displays package information but does not include a dedicated license field in its standard output. The `apk info -L <package>` lists installed files, which can be used to locate license files. The `apk info -w <package>` displays the web URL for the package. License information must typically be retrieved from the package index or Alpine's website.
- **Registry access**: Alpine's package website (https://pkgs.alpinelinux.org/packages) displays license information for packages, extracted from the APKBUILD metadata. The website provides search and browsing capabilities with license information visible on package detail pages.
- **API access**: Alpine's package index (APKINDEX) is available as a gzipped text file from Alpine mirrors (e.g., `https://dl-cdn.alpinelinux.org/alpine/<version>/<repository>/<arch>/APKINDEX.tar.gz`). The index can be parsed to extract license metadata for all packages in a repository. The APKINDEX format is a simple key-value text format. Package build files (APKBUILDs) are available in Alpine's aports Git repository (https://gitlab.alpinelinux.org/alpine/aports) where the `license` variable can be read directly.

### FreeBSD Ecosystem — Ports
- **Direct access**: License information is available in the port's `Makefile` located in the ports tree (e.g., `/usr/ports/category/portname/Makefile`). The ports tree can be checked out locally using SVN or Git (the official repository is at `https://git.freebsd.org/ports.git`). Port Makefiles are plain text and can be read directly using standard tools. For installed packages, license metadata is embedded in the binary package database.
- **CLI access**: The `make -C /usr/ports/category/portname -V LICENSE` command displays the license identifier(s) for a port. Similarly, `-V LICENSE_COMB`, `-V LICENSE_FILE`, and other license variables can be queried. For installed packages, the `pkg info <package>` command displays package metadata including licenses. The `pkg query '%L' <package>` command can be used to query specifically the license field. The `pkg` tool queries the local package database for installed packages.
- **Registry access**: FreshPorts (https://www.freshports.org/) provides a comprehensive web interface for browsing FreeBSD ports, including detailed license information parsed from port Makefiles. Each port page displays the license identifiers, license combination type, and other license-related metadata. The site provides search capabilities and tracks port updates, making it the primary web-based resource for FreeBSD ports information.
- **API access**: FreshPorts provides RSS feeds and some structured data access, though not a formal REST API. The FreeBSD ports tree itself is the canonical source and can be accessed via Git for programmatic processing. Port Makefiles can be parsed to extract `LICENSE` and related variables. The `pkg` tool supports JSON output for queries (`pkg query --json`), allowing programmatic access to license metadata for installed packages. Binary packages distributed via FreeBSD package repositories include embedded license metadata that can be extracted from downloaded packages.

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

### C++ Ecosystem — Conan
- **Coverage**: TBD
- **Reliability**: Weak to mixed. The `license` attribute is optional, allowing packages to be published without license information. There is no validation of the license field content—any string value is accepted, including misspellings, non-SPDX identifiers, custom abbreviations, or arbitrary text. ConanCenter (the central public repository) has submission guidelines that strongly recommend including license information and using SPDX identifiers, which improves reliability for packages in ConanCenter compared to private or third-party repositories. However, even ConanCenter relies primarily on code review rather than automated validation, meaning quality depends on reviewer diligence and package maintainer awareness.
- **Limitations**:
  - The `license` field is optional, allowing packages without any license metadata.
  - No validation mechanism—any string is accepted, including invalid, misspelled, or non-standard license identifiers.
  - No support for SPDX expressions with structured operators (AND, OR, WITH), making complex licensing scenarios ambiguous.
  - Multiple licenses must be represented as delimited text within a string (e.g., "MIT, Apache-2.0") with no formal specification of delimiters or semantics (AND vs. OR), requiring interpretation or external documentation.
  - Quality varies dramatically between ConanCenter (with human review) and private/third-party repositories (minimal or no quality control).
  - No centralized enforcement or migration path to improve license metadata quality for existing packages.
  - The `conanfile.py` format requires Python code execution to extract metadata, which can pose security concerns and complicates automated parsing compared to declarative formats like JSON.
  - License text files are expected by convention but not enforced—packages may declare a license in metadata without including the actual license text.

### C++ Ecosystem — Vcpkg
- **Coverage**: TBD
- **Reliability**: Weak to mixed. The `license` field is optional in `vcpkg.json`, allowing packages to be created without license information. The vcpkg documentation specifies that the license field should be either an SPDX 3.19 license expression or `null` as an escape hatch, but there is no validation to enforce this specification. Any string value is accepted. Vcpkg's position as a Microsoft-maintained project means many ports in the official repository follow the specification and use SPDX expressions. However, the lack of automated validation means license data quality depends entirely on port maintainer awareness and the code review process, and non-conforming values can be introduced.
- **Limitations**:
  - The `license` field is optional, allowing ports without any license metadata.
  - No validation mechanism—despite the specification requiring SPDX 3.19 expressions or `null` (escape hatch), any string value is accepted, including malformed SPDX expressions, misspellings, or arbitrary text that violates the specification.
  - The gap between specification (SPDX 3.19 expressions with `null` escape hatch) and enforcement (none) means non-conforming license declarations can exist in the ecosystem.
  - The `null` escape hatch is appropriate for licenses that cannot be expressed as SPDX, but requires users to manually inspect the copyright file at `/share/<port>/copyright`, providing no structured, machine-readable metadata in the manifest.
  - No mechanism to systematically audit or improve license metadata quality across all ports or detect specification violations automatically.
  - The file-based nature of vcpkg (using a GitHub repository rather than a database-backed registry service) makes it difficult to aggregate license information or assess ecosystem-wide compliance with the specification without cloning and parsing the repository.

### Clojure Ecosystem — Clojars (Leiningen)
- **Coverage**: TBD
- **Reliability**: Weak. The `:license` field is optional in `project.clj`, allowing projects to be deployed to Clojars without license information. There is no validation of license content—any string can be used for `:name` and `:url`. Since Clojars is built on Maven infrastructure and Leiningen generates Maven POM files, license metadata inherits similar quality issues as Maven Central—free-form text in license names, lack of SPDX validation, and inconsistent declarations across packages.
- **Limitations**:
  - The `:license` field is optional, allowing projects without any license metadata to be deployed to Clojars.
  - No validation mechanism—any string value is accepted for `:name` and `:url`, including misspellings, non-standard names, custom abbreviations, or arbitrary text.
  - No support for SPDX expressions with structured operators (AND, OR, WITH), making complex licensing scenarios ambiguous.
  - When multiple licenses are specified as a vector of maps, there is no formal specification of their relationship (OR vs. AND), relying on convention similar to Maven (typically OR).
  - License name quality varies widely—packages may use SPDX identifiers, descriptive phrases (e.g., "Eclipse Public License"), abbreviations (e.g., "EPL"), URLs, or arbitrary text depending on maintainer awareness.
  - No centralized validation or quality control mechanism at the Clojars level—license metadata is passed through from `project.clj` to `pom.xml` without validation.
  - Historical packages may have outdated, incorrect, or completely missing license information with no migration path or enforcement of standards.
  - The dependency on Leiningen-generated POM files means license metadata quality is constrained by Maven POM limitations and conventions.
  - No mechanism to systematically audit or improve license metadata quality across the Clojars ecosystem.

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

### Python Ecosystem — Conda
- **Coverage**: TBD
- **Reliability**: Weak. All license-related fields in `meta.yaml` are optional, meaning conda packages can be built and published without any license information. The `license` field accepts arbitrary free-form text without validation, leading to highly inconsistent license declarations across packages. Package maintainers may use SPDX identifiers, descriptive names, abbreviations, URLs, or any other text. The `license_family` field provides broad categorization but follows no official standard and accepts any text value, with common values used only by convention.
- **Limitations**:
  - All license-related fields (`license`, `license_family`, `license_file`, `license_url`) are optional, allowing packages to be published without any license metadata.
  - No validation of the `license` field, any string value is accepted, including misspellings, non-standard names, custom abbreviations, or even arbitrary text.
  - No support for SPDX expressions; complex licensing scenarios (AND, OR, WITH, exceptions) cannot be properly expressed through structured metadata.
  - The `license_family` field has no official specification or predefined list, relying entirely on community convention with no enforcement or consistency checks.
  - No mechanism to ensure that `license_file` references actually exist or contain valid license text in the built package.
  - The `license_url` field points to external URLs that may become stale, change, or become inaccessible over time, similar to deprecated approaches in other ecosystems.
  - License metadata quality varies dramatically between official channels (like defaults, conda-forge) and third-party channels, with no central validation or quality standards.
  - The `meta.yaml` file is not included in distributed packages, only derived metadata, making it difficult to trace the original license declaration or verify its accuracy.
  - Historical packages may have completely missing, inconsistent, or ambiguous license information with no migration path or enforcement of standards.
  - Recipe maintainers may inconsistently populate fields—for example, using only `license` without `license_family`, or vice versa, or using `license_url` instead of including license text directly.

### Linux Ecosystem — dpkg (Debian/Ubuntu)
- **Coverage**: TBD
- **Reliability**: Mixed to good. The DEP-5 (Debian Copyright Format 1.0) specification provides a machine-readable structured format that supports complex licensing scenarios with multiple licenses, operators (`and`, `or`), and file-level granularity. Debian policy mandates the `debian/copyright` file and encourages the use of DEP-5 format for new packages. However, reliability varies across the ecosystem because not all packages use the fully machine-readable format—older packages may still use prose-style copyright files that require human interpretation.
- **Limitations**:
  - The DEP-5 format is mandatory but not universally adopted—many older packages predate the format or haven't been updated to use it.
  - Parsing requires handling both DEP-5 machine-readable format and legacy prose-style copyright files, increasing complexity.
  - License short names used in DEP-5 follow Debian conventions (e.g., `GPL-2+`) rather than strict SPDX identifiers (e.g., `GPL-2.0-or-later`), requiring translation for cross-ecosystem compatibility.
  - No automated validation of license short names against SPDX or any other standard list—packages may use non-standard abbreviations or variations.
  - The file-level granularity in DEP-5 (different licenses for different files) means extracting a single "package license" requires interpretation and aggregation logic.
  - License text can be embedded directly or referenced from `/usr/share/common-licenses/`, requiring tools to handle both cases and potentially access the system filesystem.
  - Binary packages may have simplified or incomplete copyright files compared to their source packages, reducing metadata quality for installed software.
  - Quality depends heavily on package maintainer diligence—errors, omissions, or outdated information may persist through multiple package versions.

### Linux Ecosystem — rpm (Red Hat/Fedora/SUSE)
- **Coverage**: TBD
- **Reliability**: Strong for Fedora, mixed to weak for other RPM distributions. Since July 2022, Fedora requires valid SPDX license expressions in the `License:` tag and validates them at build time using the `python-license-expression` library. This ensures high reliability and consistency for Fedora packages. However, the broader RPM ecosystem is fragmented—different distributions have different requirements. Red Hat Enterprise Linux (RHEL), CentOS, openSUSE, and others may have varying levels of SPDX adoption, validation, or may still accept free-form license text without validation.
- **Limitations**:
  - The `License:` tag is mandatory in all RPM distributions, but content validation varies dramatically by distribution.
  - Only Fedora enforces SPDX expression validation; other RPM-based distributions may accept arbitrary text without validation.
  - Fedora additionally restricts licenses to only Fedora-acceptable licenses based on their licensing guidelines, which is stricter than SPDX or other distributions.
  - Historical packages built before Fedora's 2022 SPDX requirement may contain non-SPDX license strings even in Fedora repositories.
  - Cross-distribution portability is limited—a package built for Fedora with strict SPDX expressions may not be rebuildable on distributions that don't support SPDX syntax.
  - Source RPMs (SRPMs) contain the original spec file with license metadata, but binary RPMs embed only the processed `License:` tag value in the header, potentially losing context or spec file comments.
  - The spec file format allows complex macro expansion and conditionals, making static analysis of license declarations non-trivial without building the package.
  - License files are recommended to use the `%license` directive but this is not strictly enforced, meaning some packages may not include license text files.
  - Quality depends on distribution policy and maintainer practices—packages from less-maintained repositories may have outdated, incorrect, or ambiguous license information.

### Linux Ecosystem — apk (Alpine Linux)
- **Coverage**: TBD
- **Reliability**: Weak to mixed. The `license` field is mandatory in Alpine Linux APKBUILDs, ensuring that all packages have some license declaration. SPDX identifiers are recommended in Alpine's documentation, and many packages do use them. However, there is no validation mechanism to enforce SPDX identifiers or expressions. The space-separated format used for listing multiple licenses creates ambiguity—the format doesn't distinguish between AND and OR relationships, relying on convention, documentation, or contextual understanding of the software's actual licensing terms.
- **Limitations**:
  - The `license` field is mandatory but unvalidated—any text value is accepted, including misspellings, non-standard names, or custom abbreviations.
  - No support for SPDX expression operators (AND, OR, WITH)—complex licensing relationships cannot be expressed unambiguously.
  - Multiple licenses are listed as space-separated identifiers, but their relationship (AND vs. OR) is not formally specified, requiring interpretation or external knowledge.
  - The `custom:` prefix allows arbitrary custom license names, which may not be machine-readable or mappable to known licenses.
  - SPDX identifiers are recommended but not enforced, leading to inconsistent usage across packages and maintainers.
  - The APKBUILD is a shell script that must be executed or carefully parsed to extract the `license` variable, which can contain shell variable expansions or complex logic in rare cases.
  - The APKBUILD is not included in binary packages—license metadata is only in the package index (APKINDEX), which may become unavailable if mirrors are down or repositories are removed.
  - License files are typically included at `/usr/share/licenses/<pkgname>/` but this is by convention, not enforcement—some packages may not include license text files.
  - The space-separated format is compact but limited—expressing licenses with exceptions, nested conditions, or file-level variations is not possible.
  - Quality depends entirely on individual package maintainer knowledge and diligence, with no centralized validation or quality control mechanism.

### FreeBSD Ecosystem — Ports
- **Coverage**: TBD
- **Reliability**: Good to strong. The `LICENSE` variable is mandatory for all FreeBSD ports, ensuring comprehensive coverage across the ports collection. FreeBSD maintains a predefined database of license identifiers (`Mk/bsd.licenses.db.mk`) that provides consistency and reduces ambiguity within the FreeBSD ecosystem. The `LICENSE_COMB` variable provides explicit, unambiguous semantics for expressing AND/OR relationships between multiple licenses through three distinct values (`single`, `multi`, `dual`). The ports framework validates that license identifiers either match entries in the predefined database or are properly defined as custom licenses with all required metadata.
- **Limitations**:
  - FreeBSD uses its own set of license identifiers rather than SPDX identifiers, requiring translation for cross-ecosystem use. While many identifiers align (e.g., `MIT`, `BSD2CLAUSE`, `BSD3CLAUSE`), others differ significantly (e.g., `GPLv2` vs. `GPL-2.0-only`, `APACHE20` vs. `Apache-2.0`).
  - The predefined license list may not include the latest SPDX licenses or rare licenses, forcing use of custom license definitions which adds complexity and potential inconsistency.
  - No native support for SPDX WITH operators (license exceptions)—exceptions must be handled as custom licenses or included in license text, making them less structured and harder to parse automatically.
  - The Makefile format requires `make` to properly expand variables and evaluate conditionals, which can complicate static analysis and automated extraction of license metadata.
  - Custom licenses require manual definition of `LICENSE_NAME`, `LICENSE_TEXT` or `LICENSE_FILE`, and `LICENSE_PERMS`, which relies on port maintainer accuracy and completeness.
  - The `LICENSE_PERMS` variable (defining distribution and selling permissions) uses FreeBSD-specific conventions that don't directly map to SPDX or other ecosystems' permission models.
  - Quality depends on port maintainer diligence in selecting appropriate license identifiers from the predefined list and ensuring `LICENSE_FILE` or `LICENSE_TEXT` accurately reflects the actual license.
  - Historical ports may use outdated license identifiers or definitions that haven't been updated to reflect changes in the upstream software's licensing.
  - The ports framework provides excellent structure and consistency within FreeBSD, but its ecosystem-specific conventions create friction when attempting to aggregate or compare license data across multiple package ecosystems.

## 7. Transformation Requirements

To make license information usable across ecosystems, processes must account for the different formats and locations where licenses are declared. The goal is to produce validated SPDX expressions from heterogeneous sources.

### C++ Ecosystem — Conan
1. Retrieve the `conanfile.py` or `conanfile.txt` from the package source, either by downloading from the repository (e.g., ConanCenter), accessing the local Conan cache (`~/.conan2/p/<package>/`), or checking out the package recipe from a Git repository.
2. Parse the conanfile to extract the `license` attribute value. For `conanfile.py`, this requires executing or parsing Python code to read the `self.license` attribute. For `conanfile.txt`, parse the INI-style format to find the license line.
3. Analyze the extracted license string:
   - If it's a recognizable SPDX identifier (case-insensitive match), normalize it to the correct SPDX format (e.g., "mit" → `MIT`, "apache-2.0" → `Apache-2.0`).
   - If it appears to be multiple licenses (e.g., "MIT, Apache-2.0", "MIT OR Apache-2.0", "MIT/Apache-2.0"):
     - Attempt to parse common delimiter patterns (comma, slash, "OR", "AND", "or", "and").
     - If "OR" or "or" keywords are present, construct an SPDX expression with `OR` operators.
     - If "AND" or "and" keywords are present, construct an SPDX expression with `AND` operators.
     - If only delimiters like comma or slash are present, make a conservative assumption based on common dual-licensing patterns (typically `OR`), but flag for manual review.
   - If the string is free-form text or doesn't match SPDX identifiers, attempt fuzzy matching against the SPDX license list.
   - If fuzzy matching fails, flag the package for manual review.
4. If the license field is empty or not present:
   - Search the package source for common license files (e.g., `LICENSE`, `LICENSE.txt`, `COPYING`, `COPYING.txt`).
   - Apply a license text scanner (e.g., *scancode-toolkit*) to identify SPDX identifier(s) from the license file content.
   - If multiple licenses are detected, construct an appropriate SPDX expression based on the scanning results and package context.
5. Validate the resulting SPDX expression using an SPDX expression parser.

### Clojure Ecosystem — Clojars (Leiningen)
1. Retrieve license information from either the `project.clj` file (source) or the generated `pom.xml` file (from Clojars repository or JAR's `META-INF/maven/` directory).
2. If working with `project.clj`:
   - Parse the Clojure data structure to extract the `:license` key value.
   - This may require a Clojure parser or using Leiningen itself to read the project file.
   - The `:license` value can be a single map or a vector of maps, each with `:name` and `:url` keys.
3. If working with `pom.xml` (more common for deployed artifacts):
   - Parse the XML and extract all `<license>` elements within the `<licenses>` section.
   - For each `<license>` element, extract the `<name>` and `<url>` fields.
4. For each license `:name` (or `<name>` from POM):
   - Attempt to match the license name to a known SPDX identifier using fuzzy matching or a lookup table of common variations.
   - Common Clojure ecosystem licenses include "Eclipse Public License 1.0" → `EPL-1.0`, "EPL" → `EPL-1.0`, "Apache License 2.0" → `Apache-2.0`, "MIT" → `MIT`.
   - If the name is already an SPDX identifier, use it directly.
   - If fuzzy matching fails, use the `<url>` or `:url` field (if present and valid) to retrieve the license text and apply a license text scanner (e.g., *scancode-toolkit*) to identify the SPDX identifier.
   - If both approaches fail, flag the license as unresolvable and retain the original text for manual review.
5. If multiple licenses are present (vector of maps in `project.clj` or multiple `<license>` elements in POM):
   - Combine them into an SPDX expression with `OR` operators, following the Maven convention that multiple licenses represent alternatives.
6. Validate the resulting SPDX expression using an SPDX expression parser.

### C++ Ecosystem — Vcpkg
1. Retrieve the `vcpkg.json` manifest file from the vcpkg ports repository, either by cloning the repository (https://github.com/microsoft/vcpkg), accessing a local vcpkg installation (`<vcpkg-root>/ports/<package>/vcpkg.json`), or fetching it via the GitHub API.
2. Parse the JSON file and extract the `license` field value.
3. Check the type of the license field:
   - If `license` is `null` or missing, proceed to step 5 (license file scanning).
   - If `license` is a string, proceed to step 4.
4. Analyze the license string:
   - The vcpkg specification requires SPDX 3.19 license expressions. Attempt to parse the string as an SPDX 3.19 expression using an SPDX expression parser:
     - If parsing succeeds, validate that the expression uses only operators and identifiers valid in SPDX 3.19. Use the validated expression.
     - If parsing fails (malformed expression or uses non-SPDX format), check if it's a valid SPDX identifier without operators.
   - If the string appears to be a single SPDX identifier (no operators), validate it against the SPDX license list and normalize the case/format if needed.
   - If the string is free-form text or doesn't conform to SPDX format (specification violation):
     - Flag the port as non-conforming to the vcpkg specification.
     - Attempt fuzzy matching against the SPDX license list to map common variations (e.g., "Apache 2.0" → `Apache-2.0`, "BSD 3-Clause" → `BSD-3-Clause`).
     - If fuzzy matching succeeds, use the matched SPDX identifier but document that the original value violated the specification.
     - If fuzzy matching fails, flag the package for manual review and proceed to license file scanning as a fallback.
5. If the license field is `null`, missing, or unresolvable:
   - If `license` is `null`, this conforms to the specification and represents the escape hatch for licenses that cannot be expressed as SPDX. The copyright file is authoritative. Search for the copyright file at `/share/<port>/copyright` in the installed package.
   - If `license` is missing or the string was unresolvable, search the installed package directory or source files for common license file names (e.g., `LICENSE`, `LICENSE.txt`, `COPYING`, `copyright`, `COPYING.txt`).
   - Common locations to search: `<vcpkg-installed>/<triplet>/share/<package>/`, the port's source directory, or within the extracted source tarball.
   - Apply a license text scanner (e.g., *scancode-toolkit*) to identify SPDX identifier(s) from license file content.
   - If multiple distinct licenses are found (not just copyright statements), construct an SPDX expression based on the scanning results. Use AND if licenses apply to different components, OR if they represent alternatives.
6. Validate the resulting SPDX expression using an SPDX 3.19 expression parser.

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

### Python Ecosystem — Conda
1. Retrieve package metadata from the conda channel (e.g., via `conda search <package> --info`, from the channel's `repodata.json`, via the Anaconda.org API, or from the installed package's JSON metadata in `conda-meta/`).
2. Extract the `license` field from the metadata if present. If not present, proceed to step 4.
3. Process the `license` field content:
   - If it contains a recognizable SPDX identifier, validate it directly using an SPDX expression parser.
   - If it contains free-form text (e.g., "MIT License", "Apache 2.0", "BSD-style"), attempt to normalize common variations and map to SPDX identifiers using fuzzy matching or a lookup table.
   - If it contains multiple comma-separated or slash-separated license names (e.g., "MIT/BSD", "Apache-2.0 or MIT"), parse them and create an SPDX expression with `OR` operators.
   - If it contains a URL, proceed to step 6 to fetch and scan the license text.
   - If it contains arbitrary descriptive text that cannot be mapped, flag it for manual review and proceed to alternative extraction methods.
4. Check the `license_file` field if present:
   - Retrieve the conda package archive (`.tar.bz2` or `.conda` file) from the channel.
   - Extract the package contents and locate the file specified by `license_file`.
   - Apply a license text scanner (e.g., *scancode-toolkit*) to identify the most likely SPDX identifier(s).
   - Convert the scanning result into a valid SPDX expression.
5. Check the `license_url` field if present:
   - Attempt to retrieve the license text from the URL (if still accessible).
   - Scan the retrieved text with a license detection tool to map it to an SPDX identifier.
   - If the URL is inaccessible, broken, or returns non-license content, flag for manual review.
6. Use the `license_family` field as a supplementary hint (if present):
   - If no usable license information was extracted from previous steps, use `license_family` as a broad category indicator (e.g., `MIT` family → `MIT`, `Apache` → potentially `Apache-2.0`, `GPL` → requires version information).
   - Note that `license_family` is too imprecise for definitive SPDX mapping and should only be used as a last resort with appropriate caveats.
7. If all extraction attempts fail or no license fields are populated:
   - Search the package contents for common license files (`LICENSE`, `LICENSE.txt`, `COPYING`, `COPYING.txt`, etc.) and scan them with a license text scanner.
   - If no license information can be found, flag the package as having no declared or detectable license information.
8. Validate the resulting SPDX expression using an SPDX parser.

### Linux Ecosystem — dpkg (Debian/Ubuntu)
1. Retrieve the `debian/copyright` file from the package, either from the source package under `debian/`, from the installed package at `/usr/share/doc/<package>/copyright`, via the Debian API (https://sources.debian.org/src/), or by extracting the `.deb` file.
2. Determine if the copyright file uses the DEP-5 (Debian Copyright Format 1.0) machine-readable format or legacy prose format:
   - Check for the `Format:` header field at the beginning of the file. If present with value `https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/` or similar, it's DEP-5 format.
   - If no `Format:` field is present, it's likely a legacy prose format.
3. If the file uses DEP-5 format:
   - Parse the structured format to extract all `Files:` stanzas, each with associated `License:` and `Copyright:` fields.
   - For each `License:` field value, parse the license expression using Debian's expression syntax (e.g., `GPL-2 or GPL-3`, `(MIT or BSD-2-Clause) and GPL-2`).
   - Extract the license short name(s) and translate Debian-style license identifiers to SPDX identifiers using a mapping table (e.g., `GPL-2+` → `GPL-2.0-or-later`, `GPL-2` → `GPL-2.0-only`, `Apache-2` → `Apache-2.0`).
   - If license text is embedded in the copyright file, extract it. If license text is referenced from `/usr/share/common-licenses/`, retrieve the referenced file for validation or scanning if needed.
   - Aggregate file-level license information into a package-level SPDX expression:
     - If all files have the same license, use that license.
     - If files have different licenses, combine them with `AND` to indicate that the package as a whole includes components under multiple licenses.
     - If files offer license alternatives (using `or` in DEP-5), preserve the `OR` relationships in the SPDX expression.
4. If the file uses legacy prose format:
   - Apply natural language processing or pattern matching to extract mentions of license names, URLs, or identifiers.
   - Search for common license name patterns (e.g., "GNU General Public License version 2", "MIT License", "BSD-style").
   - Attempt to map extracted text to SPDX identifiers using fuzzy matching or a lookup table.
   - Flag the package for manual review, as prose format is inherently ambiguous and may require human interpretation.
   - If extraction is unreliable, search the package contents for common license files (`LICENSE`, `COPYING`, etc.) and scan them with a license text scanner (e.g., *scancode-toolkit*).
5. Validate the resulting SPDX expression using an SPDX parser.


### Linux Ecosystem — rpm (Red Hat/Fedora/SUSE)
1. Query the RPM package metadata to retrieve the `License:` tag value, either using `rpm -qi <package>` for installed packages, `dnf info <package>` or similar tools for repository packages, by parsing repository metadata (repodata), or by extracting the spec file from a source RPM (SRPM).
2. Determine the distribution and policy context:
   - If the package is from Fedora (especially packages built after July 2022), the `License:` value should be a valid SPDX license expression.
   - If the package is from other RPM-based distributions (RHEL, CentOS, openSUSE, etc.), the `License:` value may be SPDX-compliant, follow older conventions, or be free-form text.
3. For Fedora packages with SPDX expressions:
   - Parse the `License:` value directly as an SPDX expression with full support for `AND`, `OR`, and `WITH` operators (e.g., `MIT AND GPL-2.0-or-later`, `Apache-2.0 WITH LLVM-exception`).
   - Validate the expression using an SPDX expression parser. Fedora's validation at build time means the expression should already be valid, but verification is recommended.
4. For other RPM-based distributions without guaranteed SPDX compliance:
   - Attempt to parse the `License:` value as an SPDX expression first.
   - If parsing fails, check if it's a recognizable license name or identifier using fuzzy matching or a lookup table (e.g., "GPLv2+" → `GPL-2.0-or-later`, "MIT" → `MIT`, "Apache License Version 2.0" → `Apache-2.0`).
   - If the value contains multiple licenses separated by common patterns (e.g., "GPLv2+ and BSD", "MIT or Apache-2.0"), parse the separators and create an appropriate SPDX expression.
   - If the value is ambiguous or unrecognizable, flag the package for manual review and attempt to retrieve license text files from `/usr/share/licenses/<package-name>/` to scan with a license text scanner (e.g., *scancode-toolkit*).
5. For packages where the `License:` tag value cannot be reliably transformed:
   - Extract the source RPM (SRPM) and inspect the spec file directly for comments or additional context that might clarify the license.
   - Search the package contents for common license files and scan them with a license text scanner.
   - Flag the package as requiring manual review and document the original `License:` value for human interpretation.
6. Validate the resulting SPDX expression using an SPDX parser.


### Linux Ecosystem — apk (Alpine Linux)
1. Retrieve the `license` field value from the package metadata, either by parsing the APKBUILD file from Alpine's aports repository (https://gitlab.alpinelinux.org/alpine/aports), by extracting it from the package index (APKINDEX.tar.gz) available from Alpine mirrors, or via Alpine's package website API.
2. Parse the space-separated list of license identifiers in the `license` field value.
3. For each license identifier in the list:
   - Check if it uses the `custom:` prefix (e.g., `custom:Proprietary`). If so, flag it as a custom license that requires manual review and cannot be directly mapped to SPDX. The license terms must be obtained from the package documentation, vendor website, or included license files.
   - If it's a standard SPDX identifier (case-sensitive), use it directly (e.g., `MIT`, `Apache-2.0`, `GPL-2.0-or-later`).
   - If it appears to be an SPDX identifier with case variations or minor formatting differences, normalize it to the correct SPDX format (e.g., `apache-2.0` → `Apache-2.0`).
   - If it's not a recognized SPDX identifier, attempt fuzzy matching or lookup against common license name variations.
   - If no match is found, flag the identifier as non-standard and requiring manual review.
4. Determine the relationship between multiple licenses (AND vs. OR):
   - Alpine's space-separated format does not specify whether multiple licenses represent AND or OR relationships.
   - As a heuristic, check the software's official documentation or repository to determine the actual licensing relationship.
5. If license identifiers are ambiguous or non-standard:
   - Retrieve license files from the package at `/usr/share/licenses/<pkgname>/` (if available in the installed package) or from the APKBUILD sources.
   - Apply a license text scanner (e.g., *scancode-toolkit*) to identify the most likely SPDX identifier(s) from the license text.
   - Use the scanning results to supplement or replace the declared license identifiers.
6. Construct the SPDX expression using the determined operators (AND or OR) and the mapped SPDX identifiers.
7. Validate the resulting SPDX expression using an SPDX parser.

### FreeBSD Ecosystem — Ports
1. Retrieve the port's `Makefile` from the FreeBSD ports tree, either by accessing the local ports tree (e.g., `/usr/ports/category/portname/Makefile`), cloning the Git repository (https://git.freebsd.org/ports.git), or accessing it via FreshPorts.
2. Parse the Makefile to extract the `LICENSE`, `LICENSE_COMB`, `LICENSE_FILE`, `LICENSE_TEXT`, and `LICENSE_NAME` variables. This requires either executing `make` with the appropriate variable queries or parsing the Makefile statically (which may require handling make conditionals and variable expansions).
3. For each license identifier in the `LICENSE` variable (space-separated if multiple):
   - Check if it's a predefined license identifier from `Mk/bsd.licenses.db.mk`. Maintain a mapping table of FreeBSD license identifiers to SPDX identifiers. Common mappings include:
     - `MIT` → `MIT`
     - `GPLv2` → `GPL-2.0-only`
     - `GPLv3+` → `GPL-3.0-or-later`
     - `APACHE20` → `Apache-2.0`
     - `BSD3CLAUSE` → `BSD-3-Clause`
     - And many others from the predefined database
   - If it's a custom license (not in the predefined list), extract the `LICENSE_NAME` and `LICENSE_TEXT` or `LICENSE_FILE` to attempt identification:
     - If `LICENSE_TEXT` is present, apply a license text scanner (e.g., *scancode-toolkit*) to the text.
     - If `LICENSE_FILE` is present, retrieve the file from the port's work directory or extracted source and scan it.
     - If scanning succeeds, map to an SPDX identifier.
     - If scanning fails, flag the license as requiring manual review and retain the FreeBSD identifier and custom license information.
4. Determine the license combination semantics using the `LICENSE_COMB` variable:
   - If `LICENSE_COMB=single` or not set (default): Use only the first license identifier (or the single license if only one is specified).
   - If `LICENSE_COMB=multi`: Combine all mapped SPDX identifiers with `AND` operators (e.g., `MIT AND GPL-2.0-only`).
   - If `LICENSE_COMB=dual`: Combine all mapped SPDX identifiers with `OR` operators (e.g., `MIT OR GPL-2.0-only`).
5. For cases where the port has license exceptions or special terms not expressible through standard SPDX identifiers:
   - Review the `LICENSE_FILE` or `LICENSE_TEXT` for additional clauses or modifications.
   - If the exception is a recognized SPDX exception, construct an SPDX expression with the `WITH` operator (e.g., `GPL-2.0-or-later WITH Classpath-exception-2.0`).
   - If the exception is not a standard SPDX exception, flag it for manual review and document the custom terms.
6. Validate the resulting SPDX expression using an SPDX parser.
