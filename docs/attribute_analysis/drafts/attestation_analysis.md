# Attestation Metadata Analysis

This document analyzes how different package managers handle attestation and provenance metadata across ecosystems. Attestations provide cryptographic proof about how a package was built, linking published artifacts to their source code and build processes through verifiable claims.

## 1. Key findings summary

_TBD after sections 2–7 are finalized._

## 2. Data Collection Overview

This section provides an overview of the ecosystems and package managers reviewed to determine whether they make attestation and provenance information available as part of their metadata. Attestations are typically enabled through trusted publishing mechanisms that use OpenID Connect (OIDC) to verify the identity of publishers and generate signed claims about build provenance.

For each package manager, we indicate the level of support for attestation data and point to the relevant specification or documentation.

### JavaScript Ecosystem — npm

**Attestation Information Available**: Yes, via package provenance (shipped April 2023) and attestations

**Trusted Publishing Available**: Yes (shipped July 2025)

**References**:
- [Introducing npm package provenance](https://github.blog/2023-04-19-introducing-npm-package-provenance/)
- [npm provenance documentation](https://docs.npmjs.com/generating-provenance-statements)
- [npm trusted publishing with OIDC](https://github.blog/changelog/2025-07-31-npm-trusted-publishing-with-oidc-is-generally-available/)

### Python Ecosystem — PyPI (pip)

**Attestation Information Available**: Yes, via digital attestations (shipped November 2024)

**Trusted Publishing Available**: Yes (shipped April 2023)

**References**:
- [PyPI now supports digital attestations](https://blog.pypi.org/posts/2024-11-14-pypi-now-supports-digital-attestations/)
- [Trusted Publishers documentation](https://docs.pypi.org/trusted-publishers/)
- [Introducing Trusted Publishers](https://blog.pypi.org/posts/2023-04-20-introducing-trusted-publishers/)
- [PEP 740: Index support for digital attestations](https://peps.python.org/pep-0740/)

**Funding**: Trusted publishing funded by Google Open Source Security Team; PEP 740 partially funded by Sovereign Tech Fund; implementation funded by Google Open Source Security Team

### Java Ecosystem — Maven Central

**Attestation Information Available**: Yes, via Sigstore provenance (shipped August 2024)

**Trusted Publishing Available**: No dedicated OIDC-based trusted publishing

**References**:
- [Announcing Sigstore Java 1.0](https://blog.sigstore.dev/announcing-sigstore-java-1-0/)
- [Sigstore signature validation via portal](https://central.sonatype.org/news/20250128_sigstore_signature_validation_via_portal/)

### .NET Ecosystem — NuGet

**Attestation Information Available**: Proposed (as of June 2024)

**Trusted Publishing Available**: Yes (shipped September 2025)

**References**:
- [NuGet provenance proposal](https://github.com/NuGet/Home/issues/13581)
- [NuGet trusted publishing documentation](https://learn.microsoft.com/en-us/nuget/nugetorg/trusted-publishing)

### PHP Ecosystem — Composer (Packagist)

**Attestation Information Available**: No dedicated attestation support

**Trusted Publishing Available**: No

**References**:
- [Transparency log (in progress)](https://github.com/composer/packagist/pull/1334)

**Note**: While Packagist has a transparency log proposal in progress since September 2022, there is no shipped attestation or trusted publishing mechanism as of this analysis.

### Ruby Ecosystem — RubyGems

**Attestation Information Available**: Yes, via attestations (shipped November 2024)

**Trusted Publishing Available**: Yes (shipped December 2023)

**References**:
- [RubyGems attestations PR](https://github.com/rubygems/rubygems/pull/8239)
- [Trusted publishing announcement](https://blog.rubygems.org/2023/12/14/trusted-publishing.html)

**Funding**: Trusted publishing work done by AWS Security Residency

### Rust Ecosystem — Cargo (crates.io)

**Attestation Information Available**: Proposed (artifact signing proposed December 2023)

**Trusted Publishing Available**: Yes (shipped July 2025)

**References**:
- [Improving supply chain security](https://foundation.rust-lang.org/news/2023-12-21-improving-supply-chain-security/)
- [crates.io development update](https://blog.rust-lang.org/2025/07/11/crates-io-development-update-2025-07/)

### macOS Ecosystem — Homebrew

**Attestation Information Available**: Yes, via build provenance (shipped May 2024)

**Trusted Publishing Available**: No dedicated OIDC-based trusted publishing

**References**:
- [A peek into build provenance for Homebrew](https://blog.trailofbits.com/2024/05/14/a-peek-into-build-provenance-for-homebrew/)

**Funding**: OpenSSF Alpha Omega

### Dart Ecosystem — pub.dev

**Attestation Information Available**: Not explicitly documented

**Trusted Publishing Available**: Yes (shipped February 2024)

**References**:
- [Automated publishing with OIDC](https://dart.dev/tools/pub/automated-publishing)

## 3. Field Analysis

This section groups ecosystems according to how attestation and provenance information can be accessed and verified. The focus is on whether attestations are cryptographically signed, publicly accessible, and integrated into the package metadata or served separately.

### Ecosystems with Shipped Attestation Support

#### JavaScript Ecosystem — npm

- **Attestation mechanism**: npm generates provenance attestations using Sigstore when packages are published from supported CI/CD platforms (GitHub Actions)
- **Format**: Uses in-toto attestation format with SLSA (Supply chain Levels for Software Artifacts) provenance
- **Signing**: Attestations are signed using Sigstore's keyless signing (ephemeral keys with OIDC identity verification)
- **Storage**: Attestations are stored in the npm registry and linked to package versions
- **Verification**: Can be verified using the npm CLI or Sigstore verification tools
- **Trusted publishing integration**: OIDC-based trusted publishing allows direct publishing from GitHub Actions without long-lived tokens

#### Python Ecosystem — PyPI (pip)

- **Attestation mechanism**: Digital attestations following PEP 740, generated during package upload
- **Format**: Uses attestation bundles containing provenance information
- **Signing**: Attestations are signed and verifiable through the PyPI API
- **Storage**: Attestations are stored separately from package files but accessible via the PyPI API
- **Verification**: Verification tools and libraries are available for validating attestations
- **Trusted publishing integration**: OIDC-based trusted publishing from GitHub Actions, GitLab CI, Google Cloud, and other providers eliminates the need for API tokens

#### Java Ecosystem — Maven Central

- **Attestation mechanism**: Sigstore-based provenance for artifacts
- **Format**: Uses Sigstore bundle format
- **Signing**: Cryptographic signatures using Sigstore
- **Storage**: Provenance data stored alongside artifacts in Maven Central
- **Verification**: Verification available through the Maven Central portal and Sigstore tools
- **Trusted publishing integration**: No dedicated OIDC-based publishing mechanism; relies on traditional authentication

#### Ruby Ecosystem — RubyGems

- **Attestation mechanism**: Attestations for gem packages
- **Format**: TBD (requires API investigation)
- **Signing**: Cryptographic signatures
- **Storage**: Attestations stored in RubyGems registry
- **Verification**: Verification mechanisms available
- **Trusted publishing integration**: OIDC-based trusted publishing from GitHub Actions and other CI/CD platforms

#### macOS Ecosystem — Homebrew

- **Attestation mechanism**: Build provenance for formula bottles
- **Format**: Provenance metadata describing the build environment and process
- **Signing**: TBD (requires investigation)
- **Storage**: Provenance information stored with bottle metadata
- **Verification**: Verification mechanisms available
- **Trusted publishing integration**: No dedicated OIDC-based publishing mechanism

### Ecosystems with Proposed Attestation Support

#### .NET Ecosystem — NuGet

- **Status**: Provenance proposed (GitHub issue #13581 from June 2024)
- **Trusted publishing**: Shipped (September 2025)
- **Current state**: While trusted publishing is available, attestation/provenance generation and verification is still in proposal stage
- **Expected mechanism**: Likely to follow similar patterns to npm and PyPI once implemented

#### Rust Ecosystem — Cargo (crates.io)

- **Status**: Artifact signing proposed (December 2023)
- **Trusted publishing**: Shipped (July 2025)
- **Current state**: Trusted publishing available but attestation/signing still being designed
- **Additional security work**: TUF (The Update Framework) for releases and package index proposed (October 2024)

### Ecosystems without Attestation Support

#### PHP Ecosystem — Composer (Packagist)

- **Attestation support**: No
- **Trusted publishing**: No
- **Related work**: Transparency log proposal in progress (since September 2022)
- **Security features**: Popular package takeover prevention, repo jacking protection, vulnerability notifications

#### Dart Ecosystem — pub.dev

- **Attestation support**: Not explicitly documented or announced
- **Trusted publishing**: Yes (shipped February 2024)
- **Current state**: Trusted publishing available but no public attestation mechanism

## 4. Data Format Analysis

This section analyzes the technical formats and standards used for attestations across ecosystems, including how attestations are structured, signed, and stored.

### JavaScript Ecosystem — npm

- **Data type**: JSON attestation bundles
- **Standard**: in-toto attestation format (https://in-toto.io/Statement/v0.1)
- **Provenance level**: SLSA v0.2 provenance predicates
- **Signature format**: Sigstore bundle (includes signature, certificate from Fulcio CA, and transparency log entry in Rekor)
- **Build type**: `https://github.com/npm/cli/gha/v2` for GitHub Actions builds
- **Subject**: Published npm package with SHA512 digest
- **Materials**: Source repository URI and commit SHA
- **Location**: Stored in npm registry and Sigstore's Rekor transparency log
- **API endpoint**: `https://registry.npmjs.org/-/npm/v1/attestations/${name}@${version}`
- **Rekor verification**: `https://rekor.sigstore.dev/api/v1/log/entries?logIndex=${logIndex}`
- **Accessibility**: Available through npm CLI commands and registry API endpoints
- **Verification requirements**: Sigstore verification libraries or npm CLI verification commands

### Python Ecosystem — PyPI (pip)

- **Data type**: Attestation bundles as defined in PEP 740
- **Standard**: in-toto Attestation Framework
- **Supported predicates**:
  - SLSA Provenance (v1.0 specification) - for build provenance claims
  - PyPI Publish attestations (v1) - confirms publishing via Trusted Publisher (predicate type: `https://docs.pypi.org/attestations/publish/v1`)
    - Minimal attestation: predicate body is empty JSON object `{}` or `null`
    - Confirms package was uploaded via Trusted Publisher (not API token)
    - Links to specific publisher identity (GitHub Actions workflow, Google Cloud service account, etc.)
- **Signature format**: Identity-based signing using OpenID Connect (OIDC) identities instead of key pairs
- **Verification material**: Includes certificate and transparency log information
- **Location**: Separate from package files, accessible via PyPI Integrity API
- **API endpoint**: `GET /integrity/<project>/<version>/<filename>/provenance`
- **Example**: `https://pypi.org/integrity/sampleproject/4.0.0/sampleproject-4.0.0.tar.gz/provenance`
- **Simple API integration**: Distributions with attestations include a `provenance` key in the JSON simple API and `data-provenance` attribute in PEP 503 index
- **Limit**: Maximum of two attestations per file (one per predicate type)
- **Accessibility**:
  - Programmatic via Integrity API (JSON format)
  - Web UI on file details pages (e.g., `pypi.org/project/sampleproject/#sampleproject-4.0.0.tar.gz`)
- **Verification requirements**:
  - `pypi-attestations` Python library
  - Only attestations with verifiable signatures are accepted by PyPI
  - Can verify local files, pypi: prefixed filenames, or direct URLs

### Java Ecosystem — Maven Central

- **Data type**: Sigstore bundles (`.sigstore.json` files)
- **Standard**: Sigstore bundle format
- **Provenance level**: Sigstore signatures supplement PGP signatures (both currently supported)
- **Signature format**: Sigstore signatures using Fulcio CA and Rekor transparency log
- **Location**: Stored alongside artifacts in Maven Central repository
  - Pattern: `{group}/{artifact}/{version}/{artifact}-{version}.jar.sigstore.json`
  - Example: `https://repo1.maven.org/maven2/org/leplus/ristretto/2.0.0/ristretto-2.0.0.jar.sigstore.json`
- **Status**: Optional - Sigstore signatures not required for publishing (as of 2024/2025)
- **Validation**: Maven Central Publisher Portal validates Sigstore signatures and provides warnings for invalid signatures
- **Future**: Warnings will eventually become errors; PGP signatures remain required alongside Sigstore
- **Accessibility**:
  - Direct download from Maven repository URLs
  - Validation feedback via Publisher Portal during deployment
- **Verification requirements**:
  - Sigstore Java libraries (`dev.sigstore:sigstore-java`)
  - cosign CLI for verification
  - Maven plugin: `dev.sigstore:sigstore-maven-plugin`
  - Gradle plugin: `dev.sigstore.sign`

### Ruby Ecosystem — RubyGems

- **Data type**: Sigstore attestation bundles
- **Standard**: Sigstore bundle format with DSSE (Dead Simple Signing Envelope) signing
- **Provenance level**: Build attestations linking gems to GitHub Actions workflows
- **Signature format**: Sigstore signatures using GitHub identity via OIDC
- **Location**: RubyGems.org registry with new API endpoints and storage systems
- **Publishing**: `gem push --attestation FILE` command
- **Accessibility**:
  - Uploaded as JSON arrays during gem push
  - Stored in RubyGems.org infrastructure
  - API endpoints available (specific endpoints require further documentation)
- **Verification requirements**:
  - `sigstore-ruby` gem (pure-Ruby implementation of Sigstore client spec)
  - Command: `gem sigstore_cosign_verify_bundle` with certificate identity and OIDC issuer validation
  - Third-party verification: DataDog's `go-attestations-verifier` library
- **Adoption tracking**: "Are We Attested Yet?" tracker at https://segiddins.github.io/are-we-attested-yet/
- **Current adoption**: 20 of the top gems shipping attestations as of 2024
- **Integration**: Works with trusted publishing from GitHub Actions

### macOS Ecosystem — Homebrew

- **Data type**: Build provenance attestations for bottles
- **Standard**: GitHub Artifact Attestations using in-toto statement format
- **Provenance level**: SLSA Build L2 compliant
- **Signature format**: Sigstore signatures via GitHub's attestation system
- **Attestation contents**:
  - GitHub owner and repository
  - Git commit hash
  - GitHub Actions workflow identifier
  - Workflow trigger event
  - GitHub Actions run ID
- **Generation**: Automatic via `generate-build-provenance` action in Homebrew CI pipeline
- **Location**: Stored through GitHub's native attestation system
- **Accessibility**:
  - GitHub API endpoints (requires authentication)
  - `gh attestation` CLI (GitHub's command-line interface)
  - Homebrew's verification layer (wraps `gh` CLI internally)
- **Verification requirements**:
  - Primary: `brew verify` command (from Trail of Bits tap)
  - Installation-time: `HOMEBREW_VERIFY_ATTESTATIONS=1` environment variable during `brew install`
  - Direct verification: cosign v2.4.0+ with `cosign verify-blob-attestation`
  - Certificate validation: `--certificate-oidc-issuer` and `--certificate-identity` flags for official Homebrew workflows
- **Fallback strategy**: Waterfall verification checks upstream provenance from Homebrew/homebrew-core, then backfilled attestations
- **Status**: Public beta, working toward default-enabled verification for all bottles
- **Impact**: Changes integrity guarantee from "matches known digest" to "matches known digest AND produced on Homebrew's CI/CD"

## 5. Access Patterns

This section describes how attestation information can be accessed and retrieved across different ecosystems, including CLI tools, APIs, and verification mechanisms.

### JavaScript Ecosystem — npm

- **CLI access**:
  - Verification: `npm audit signatures` command (npm 9.5.0+)
  - Publishing with provenance: `npm publish --provenance` from GitHub Actions
- **API access**: `https://registry.npmjs.org/-/npm/v1/attestations/${name}@${version}`
- **Web interface**: npm website displays provenance badge and information on package pages for packages with verified provenance
- **Verification process**:
  1. npm registry validates cryptographic signature and signing certificate identity before accepting publication
  2. Rekor transparency log provides tamper-evident record
  3. Consumers verify using `npm audit signatures` or Sigstore tools
- **Programmatic access**:
  - Registry API returns attestation data in JSON format (in-toto Statement)
  - Cross-reference with Rekor using logIndex: `https://rekor.sigstore.dev/api/v1/log/entries?logIndex=${logIndex}`
- **Generation**: Automatic when publishing with `--provenance` flag from GitHub Actions (uses single-use keypair, Fulcio CA certificate, Rekor transparency log)

### Python Ecosystem — PyPI (pip)

- **CLI access**:
  - Verification: `pypi-attestations` Python library/CLI tool
  - Publishing: Automatic generation when using `pypa/gh-action-pypi-publish` from GitHub Actions with Trusted Publishing
- **API access**: `GET /integrity/<project>/<version>/<filename>/provenance`
  - Example: `https://pypi.org/integrity/sampleproject/4.0.0/sampleproject-4.0.0.tar.gz/provenance`
  - Returns JSON with attestation bundles grouped by Trusted Publisher identity
- **Web interface**:
  - File details pages show attestation information (e.g., `pypi.org/project/sampleproject/#sampleproject-4.0.0.tar.gz`)
  - Package pages display attestation status
- **Simple API integration**:
  - Distributions with attestations include `provenance` key in JSON simple API
  - `data-provenance` attribute in PEP 503 index contains provenance object URL
- **Verification process**:
  1. PyPI validates signatures at upload time—only verifiable attestations accepted
  2. Attestations bind package files to source repositories via OIDC identities
  3. Consumers verify using `pypi-attestations` library (supports local files, pypi: URIs, direct URLs)
- **Generation**:
  - Automatic: Publish from GitHub Actions/GitLab CI/Google Cloud with Trusted Publishing enabled
  - Manual generation supported but not recommended
- **Supported identities**: GitHub Actions, GitLab CI/CD, Google Cloud (via OIDC)

### Java Ecosystem — Maven Central

- **CLI access**:
  - Maven and Gradle plugins for signing during build: `dev.sigstore:sigstore-maven-plugin`, `dev.sigstore.sign`
  - cosign CLI for verification: `cosign verify-blob --bundle <file>.sigstore.json --certificate-oidc-issuer <issuer> --certificate-identity-regexp=<pattern> <artifact>`
  - Maven CLI does not directly expose attestation verification
- **API access**: Direct HTTP access to Maven repository URLs
  - Pattern: `https://repo1.maven.org/maven2/{group}/{artifact}/{version}/{artifact}-{version}.{ext}.sigstore.json`
  - Example: `https://repo1.maven.org/maven2/org/leplus/ristretto/2.0.0/ristretto-2.0.0.jar.sigstore.json`
- **Web interface**: Maven Central Publisher Portal provides signature validation interface
  - Validates Sigstore signatures during deployment
  - Provides warnings for invalid signatures (will become errors in future)
- **Verification process**:
  1. Download artifact and corresponding `.sigstore.json` bundle
  2. Verify using Sigstore Java libraries or cosign
  3. Validate certificate OIDC issuer and identity
  4. Confirm signature matches artifact content
- **Programmatic access**:
  - Sigstore Java library APIs
  - Standard HTTP GET requests to Maven repository URLs
  - Integration with build tools via plugins

### Ruby Ecosystem — RubyGems

- **CLI access**:
  - Publishing: `gem push --attestation FILE` (supports multiple attestation files)
  - Verification: `gem sigstore_cosign_verify_bundle` with certificate identity and OIDC issuer validation
  - Sigstore Ruby gem provides pure-Ruby implementation of Sigstore client
- **API access**: RubyGems.org API with new attestation endpoints
  - Attestations uploaded as JSON arrays during gem push
  - Specific API endpoint URLs require further documentation
- **Web interface**:
  - Adoption tracking: "Are We Attested Yet?" at https://segiddins.github.io/are-we-attested-yet/
  - Package pages may display attestation status (requires confirmation)
- **Verification process**:
  1. Retrieve gem and attestation bundle
  2. Verify using `sigstore-ruby` gem or third-party tools
  3. Validate GitHub identity via OIDC certificate
  4. Confirm DSSE signature matches gem content
- **Programmatic access**:
  - `sigstore-ruby` gem for Ruby applications
  - DataDog's `go-attestations-verifier` library for Go applications
  - Command: `go run ./cmd rubygems --name <gem> --version <version>`
- **Generation**: Automatic when using trusted publishing from GitHub Actions
- **Current adoption**: 20 of top gems shipping attestations as of 2024

### macOS Ecosystem — Homebrew

- **CLI access**:
  - Verification: `brew verify` command (from Trail of Bits tap: `brew tap trailofbits/brew-verify`)
  - Installation-time verification: Set `HOMEBREW_VERIFY_ATTESTATIONS=1` environment variable
  - GitHub CLI: `gh attestation` commands for direct attestation access
- **API access**: GitHub API endpoints for artifact attestations
  - Requires authentication for API access
  - Attestations stored in GitHub's native attestation system
- **Web interface**: Not applicable (Homebrew is primarily CLI-based)
  - GitHub Actions run pages show attestation generation
- **Verification process**:
  1. Homebrew wraps `gh` CLI internally for attestation retrieval
  2. Waterfall verification strategy:
     - First checks upstream provenance from Homebrew/homebrew-core workflows
     - Falls back to backfilled attestations if needed
     - Hard failure if neither exists (prevents downgrade attacks)
  3. Validates against official Homebrew workflows using OIDC issuer and identity
  4. Confirms bottle matches attested build metadata
- **Programmatic access**:
  - cosign v2.4.0+ for direct verification: `cosign verify-blob-attestation`
  - GitHub API for programmatic attestation retrieval
  - Homebrew's internal attestation module (Ruby API)
- **Attestation contents**:
  - Links bottle to specific GitHub Actions run
  - Includes commit hash, workflow ID, and trigger event
  - SLSA Build L2 compliant metadata
- **Status**: Public beta, working toward default-enabled verification

## 6. Quality Assessment

This section evaluates the maturity, coverage, and reliability of attestation mechanisms across ecosystems.

### JavaScript Ecosystem — npm

- **Maturity**: Mature (shipped April 2023 for provenance, July 2025 for trusted publishing)
- **Coverage**: Low adoption - among 2,000 most downloaded packages on jsDelivr, only 26 out of 205 eligible packages (12.6%) have enabled provenance as of 2024
- **Adoption requirements**: Requires publishing from supported CI/CD platforms (primarily GitHub Actions) with `--provenance` flag
- **Limitations**:
  - Only packages published from supported CI/CD platforms receive attestations
  - Requires publishers to adopt trusted publishing workflows
  - Legacy packages published before April 2023 lack attestations
  - Low adoption rate despite feature maturity
  - Verification requires understanding of Sigstore and SLSA concepts
  - Provenance only generated when explicitly enabled with `--provenance` flag

### Python Ecosystem — PyPI (pip)

- **Maturity**: Recent (shipped November 2024)
- **Coverage**: TBD (percentage of packages with attestations)
- **Adoption requirements**: Publishers must use trusted publishing or explicitly generate attestations
- **Limitations**:
  - New feature with limited adoption so far
  - Requires publisher adoption of trusted publishing workflows
  - Existing packages lack attestations unless republished
  - Ecosystem tooling still developing verification capabilities

### Java Ecosystem — Maven Central

- **Maturity**: Recent (shipped August 2024, portal validation January 2025)
- **Coverage**: Optional/voluntary - adoption rate unknown but growing
- **Adoption requirements**: Publishers must integrate Sigstore Maven/Gradle plugins into build process
- **Limitations**:
  - Sigstore signatures are optional (not required for publication as of 2024/2025)
  - PGP signatures still required alongside Sigstore (dual signature requirement)
  - No OIDC-based trusted publishing; relies on traditional Maven Central authentication
  - Requires manual integration of Sigstore tooling into build pipelines
  - Invalid signatures currently generate warnings, not errors (will change in future)
  - Publishers must explicitly add plugin configuration to their builds

### Ruby Ecosystem — RubyGems

- **Maturity**: Very recent (attestations shipped November 2024; trusted publishing December 2023)
- **Coverage**: 20 of the top gems shipping attestations as of 2024 (tracking at https://segiddins.github.io/are-we-attested-yet/)
- **Adoption requirements**: Use of trusted publishing workflows from GitHub Actions
- **Limitations**:
  - Very new feature with limited but growing adoption
  - Ecosystem tooling still developing (sigstore-ruby gem is foundational but ecosystem integration ongoing)
  - Requires GitHub Actions for trusted publishing integration
  - Verification requires understanding of Sigstore and DSSE signing
  - API endpoint documentation incomplete
  - Most gems lack attestations (only 20 of top gems have them)

### macOS Ecosystem — Homebrew

- **Maturity**: Recent (shipped May 2024, currently in public beta)
- **Coverage**: All bottles built by official Homebrew CI have provenance attestations
- **Adoption requirements**:
  - Verification currently opt-in (`HOMEBREW_VERIFY_ATTESTATIONS=1` or `brew verify` command)
  - Working toward default-enabled verification for all bottles
- **Limitations**:
  - No OIDC-based trusted publishing for third-party contributors
  - Attestations only available for bottles built by official Homebrew CI
  - Build provenance specific to Homebrew's centralized bottle building process
  - Verification requires GitHub authentication for API access
  - Currently in beta - not yet enforced by default
  - Requires external tooling (`gh` CLI or Trail of Bits tap) for verification
  - Third-party taps may not have attestations

### Ecosystems without Full Support

#### .NET Ecosystem — NuGet

- **Status**: Trusted publishing available but attestations still proposed
- **Gap**: Publishers can use OIDC authentication but no provenance generation yet

#### Rust Ecosystem — Cargo

- **Status**: Trusted publishing available but artifact signing still proposed
- **Gap**: Authentication improved but no cryptographic attestations yet

#### PHP Ecosystem — Composer (Packagist)

- **Status**: No attestation or trusted publishing support
- **Alternative security measures**: Takeover prevention, repo jacking protection, vulnerability notifications

#### Dart Ecosystem — pub.dev

- **Status**: Trusted publishing available (shipped February 2024) but no attestation/provenance system
- **Gap**: OIDC authentication from GitHub Actions, GitLab CI, and Google Cloud available but no cryptographic attestations or build provenance
- **Current security**: Audit logging shows link to GitHub Action run that published package, but no cryptographic proof
- **What exists**: Tag pattern matching, environment requirements, service account verification
- **What's missing**: Sigstore attestations, SLSA provenance, verifiable build claims

## 7. Transformation Requirements

This section outlines the steps required to retrieve, parse, and verify attestation information for each ecosystem that supports it.

### JavaScript Ecosystem — npm

1. **Retrieve attestation data**:
   - Query npm registry API: `GET https://registry.npmjs.org/-/npm/v1/attestations/${name}@${version}`
   - Returns JSON in-toto Statement format with SLSA v0.2 provenance
   - Alternative: Use `npm audit signatures` CLI command

2. **Parse attestation format**:
   - Parse in-toto attestation JSON structure (`_type`: `https://in-toto.io/Statement/v0.1`)
   - Extract `subject` (package name and SHA512 digest)
   - Extract `predicateType`: `https://slsa.dev/provenance/v0.2`
   - Extract `predicate` containing build details:
     - `builder.id`: Build type (e.g., `https://github.com/npm/cli/gha/v2`)
     - `materials`: Source repository URI and commit SHA
     - `invocation`: Build configuration and workflow details

3. **Verify signatures**:
   - Extract Sigstore bundle (signature, certificate, transparency log entry)
   - Verify certificate chain against Sigstore Fulcio CA root
   - Verify transparency log inclusion in Rekor: `GET https://rekor.sigstore.dev/api/v1/log/entries?logIndex=${logIndex}`
   - Validate OIDC identity claims embedded in certificate
   - Verify signature matches package content (SHA512)

4. **Extract provenance claims**:
   - Parse SLSA provenance to determine:
     - Build platform (GitHub Actions workflow)
     - Source repository and commit
     - Builder identity and environment
     - Build invocation parameters
   - Cross-reference repository URI with package metadata

5. **Verification tools**:
   - npm CLI: `npm audit signatures`
   - Sigstore libraries for programmatic verification
   - Manual Rekor API verification

### Python Ecosystem — PyPI (pip)

1. **Retrieve attestation data**:
   - Query PyPI Integrity API: `GET https://pypi.org/integrity/<project>/<version>/<filename>/provenance`
   - Example: `GET https://pypi.org/integrity/sampleproject/4.0.0/sampleproject-4.0.0.tar.gz/provenance`
   - Returns JSON provenance object with attestation bundles grouped by Trusted Publisher identity
   - Alternative: Check `provenance` key in Simple API or `data-provenance` attribute in PEP 503 index
   - CLI: Use `pypi-attestations` Python library

2. **Parse attestation format**:
   - Parse PEP 740 attestation bundle structure
   - Extract in-toto Attestation Framework data
   - Identify attestation predicates:
     - SLSA Provenance (v1.0)
     - PyPI Publish attestations
   - Extract verification material (certificate, transparency log)
   - Parse publisher identity information (GitHub Actions, GitLab CI, Google Cloud)

3. **Verify attestations**:
   - Use `pypi-attestations` library for verification
   - Verify OIDC identity-based signatures
   - Validate certificate and transparency log information
   - Confirm attestation matches file digest
   - Note: PyPI only accepts attestations with verifiable signatures at upload time

4. **Extract provenance claims**:
   - Parse SLSA provenance to determine:
     - Publishing platform (GitHub Actions, GitLab CI, etc.)
     - Source repository and commit
     - Workflow information
     - Build environment context
   - Extract PyPI Publish attestation for registry-specific claims
   - Verify trusted publisher configuration

5. **Verification tools and methods**:
   - `pypi-attestations` Python library supports:
     - Local file verification
     - `pypi:` prefixed filename verification
     - Direct URL verification
   - Web UI: Check file details pages on pypi.org
   - Programmatic: Query Integrity API for automation

### Java Ecosystem — Maven Central

1. **Retrieve Sigstore bundle**:
   - Construct URL: `https://repo1.maven.org/maven2/{group}/{artifact}/{version}/{artifact}-{version}.{ext}.sigstore.json`
   - Replace `{group}` with group ID (replace dots with slashes, e.g., `org.leplus` → `org/leplus`)
   - Replace `{artifact}`, `{version}`, and `{ext}` appropriately
   - Example: `https://repo1.maven.org/maven2/org/leplus/ristretto/2.0.0/ristretto-2.0.0.jar.sigstore.json`
   - Download both the artifact and corresponding `.sigstore.json` bundle via HTTP GET

2. **Parse Sigstore bundle**:
   - Parse Sigstore bundle JSON format
   - Extract components:
     - Signature data (cryptographic signature of artifact)
     - Certificate (from Sigstore Fulcio CA, contains OIDC identity)
     - Transparency log entry (Rekor inclusion proof)
   - Identify signing identity from certificate extensions

3. **Verify signatures**:
   - Use Sigstore Java libraries (`dev.sigstore:sigstore-java`) for programmatic verification
   - OR use cosign CLI: `cosign verify-blob --bundle <file>.sigstore.json --certificate-oidc-issuer <issuer> --certificate-identity-regexp=<pattern> <artifact>`
   - Verify certificate chain against Sigstore Fulcio CA root
   - Verify transparency log inclusion in Rekor
   - Validate OIDC identity claims match expected publisher
   - Confirm signature matches artifact digest

4. **Extract provenance information**:
   - Parse OIDC identity from certificate to determine:
     - Issuer (e.g., GitHub Actions, GitLab CI)
     - Subject (workflow/job identifier)
     - Repository information (if available in certificate extensions)
   - Note: Provenance details depend on how publisher configured signing
   - May include workflow URL, commit SHA, and build environment

5. **Build integration**:
   - For signing: Add `dev.sigstore:sigstore-maven-plugin` to `pom.xml` or `dev.sigstore.sign` Gradle plugin
   - For verification: Integrate Sigstore Java API into dependency verification workflows
   - Portal validation: Maven Central validates during deployment and provides feedback

### Ruby Ecosystem — RubyGems

1. **Retrieve attestation data**:
   - RubyGems.org API with attestation endpoints (specific URL patterns require documentation)
   - Attestations stored alongside gem metadata in RubyGems registry
   - For verification: Download gem and retrieve associated attestation bundle
   - Check "Are We Attested Yet?" tracker to see if gem has attestations: https://segiddins.github.io/are-we-attested-yet/

2. **Parse attestation format**:
   - Parse Sigstore bundle format with DSSE signing envelope
   - Extract components:
     - DSSE signature (Dead Simple Signing Envelope)
     - Certificate (from Sigstore Fulcio CA with GitHub OIDC identity)
     - Transparency log entry (Rekor inclusion proof)
   - Identify GitHub Actions workflow identity from certificate
   - Parse attestation payload for provenance claims

3. **Verify attestations**:
   - Use `sigstore-ruby` gem for verification:
     ```ruby
     gem sigstore_cosign_verify_bundle \
       --certificate-oidc-issuer https://token.actions.githubusercontent.com \
       --certificate-identity <expected-identity>
     ```
   - Verify DSSE signature matches gem content
   - Validate certificate chain against Sigstore Fulcio CA
   - Verify Rekor transparency log inclusion
   - Confirm OIDC identity matches expected GitHub repository/workflow
   - Alternative: Use DataDog's `go-attestations-verifier`: `go run ./cmd rubygems --name <gem> --version <version>`

4. **Extract provenance claims**:
   - Parse attestation to determine:
     - GitHub repository that built the gem
     - GitHub Actions workflow that performed the build
     - Git commit SHA that was built
     - Workflow run ID for audit trail
   - Link to trusted publisher configuration on RubyGems.org
   - Verify workflow came from expected repository

5. **Publishing workflow**:
   - For publishers: Use `gem push --attestation FILE` with trusted publishing from GitHub Actions
   - Attestations uploaded as JSON arrays during publish
   - Multiple attestation files can be provided
   - Requires trusted publishing configuration on RubyGems.org

### macOS Ecosystem — Homebrew

1. **Retrieve provenance data**:
   - Attestations stored in GitHub's native attestation system
   - Access via GitHub API endpoints (requires authentication)
   - Homebrew wraps `gh attestation` CLI internally
   - For manual access: Use `gh attestation` commands
   - Example workflow: `brew verify <formula>` or set `HOMEBREW_VERIFY_ATTESTATIONS=1` during install

2. **Parse provenance format**:
   - Parse GitHub Artifact Attestation (in-toto statement format)
   - Extract SLSA Build L2 compliant metadata:
     - `subject`: Bottle file with digest
     - `predicateType`: GitHub attestation predicate
     - `predicate` containing:
       - GitHub owner and repository (e.g., `Homebrew/homebrew-core`)
       - Git commit hash
       - GitHub Actions workflow identifier
       - Workflow trigger event
       - GitHub Actions run ID
   - Parse Sigstore signature and certificate data

3. **Verify provenance**:
   - **Method 1**: Use Homebrew's built-in verification
     ```bash
     brew tap trailofbits/brew-verify
     brew verify <formula>
     ```
   - **Method 2**: Verify during installation
     ```bash
     HOMEBREW_VERIFY_ATTESTATIONS=1 brew install <formula>
     ```
   - **Method 3**: Use cosign directly (v2.4.0+)
     ```bash
     cosign verify-blob-attestation \
       --certificate-oidc-issuer https://token.actions.githubusercontent.com \
       --certificate-identity-regexp='^https://github.com/Homebrew/.*' \
       <bottle-file>
     ```
   - Verification follows waterfall strategy:
     - First checks upstream provenance from Homebrew/homebrew-core
     - Falls back to backfilled attestations if available
     - Hard failure if neither exists (prevents downgrade attacks)

4. **Extract build information**:
   - Parse attestation to determine:
     - Exact GitHub Actions workflow that built the bottle
     - Git commit SHA of Homebrew formula
     - Workflow run ID (provides audit trail to specific CI build)
     - Trigger event (e.g., push, pull_request)
   - Verify bottle was built by official Homebrew CI infrastructure
   - Link to GitHub Actions run page for full build logs

5. **Integration and automation**:
   - Programmatic access via GitHub API (requires auth token)
   - Use `gh` CLI for scripting: `gh attestation verify`
   - Homebrew's Ruby API: `Homebrew::Attestation` module
   - Future: Verification will be enabled by default for all installs
   - Status check: Attestations change integrity from "matches digest" to "matches digest AND built on Homebrew CI"

---

## Concrete Examples

This section provides real-world examples of attestations from different ecosystems, showing the actual data structures and how to inspect them.

### Example: npm Attestation in Sigstore Rekor

npm attestations are logged in Sigstore's Rekor transparency log. Here's an example entry:
- **Rekor log index**: 274262258
- **Search**: https://search.sigstore.dev/?logIndex=274262258
- **Format**: in-toto Statement with SLSA v0.2 provenance
- **Verification**: The Rekor entry provides tamper-evident proof of when the attestation was created

To inspect an npm attestation:
1. Query npm registry API: `https://registry.npmjs.org/-/npm/v1/attestations/${package}@${version}`
2. Extract `logIndex` from the response
3. Verify in Rekor: `https://rekor.sigstore.dev/api/v1/log/entries?logIndex=${logIndex}`

### Example: PyPI Attestation Structure

Real example from urllib3 package:
- **URL**: https://pypi.org/integrity/urllib3/2.5.0/urllib3-2.5.0-py3-none-any.whl/provenance
- **Response structure**:
  ```json
  {
    "attestation_bundles": [{
      "attestations": [{
        "envelope": {
          "signature": "<base64-encoded>",
          "statement": "<base64-encoded JSON>"
        },
        "verification_material": {
          "certificate": "<PEM-encoded X.509>",
          "transparency_entries": [...]
        }
      }]
    }],
    "publisher": {
      "kind": "GitHub",
      "repository": "urllib3/urllib3",
      "workflow": "publish.yml"
    }
  }
  ```

**Decoding the statement**: The `statement` field is base64-encoded. When decoded, it reveals:
```json
{
  "_type": "https://in-toto.io/Statement/v1",
  "subject": [{
    "name": "urllib3-2.5.0-py3-none-any.whl",
    "digest": {
      "sha256": "e6b01673c0fa6a13e374b50871808eb3bf7046c4b125b216f6bf1cc604cff0dc"
    }
  }],
  "predicateType": "https://docs.pypi.org/attestations/publish/v1",
  "predicate": null
}
```

**Understanding the attestation**:
- `_type`: Uses in-toto Statement v1 format
- `subject`: Identifies the wheel file and its SHA256 digest
- `predicateType`: Points to PyPI Publish attestation v1 specification
- `predicate`: Empty/null for PyPI Publish attestations (confirms Trusted Publisher usage)
- `publisher` metadata: Shows this was published from `urllib3/urllib3` repository via `publish.yml` workflow

**Inspection tools**:
- Online decoder: https://dsse.io/ (for Sigstore bundles)
- Manual: Base64 decode the `statement` field to see attestation contents
- Verification: Use `pypi-attestations` library to cryptographically verify

### Example: Maven Central Sigstore Bundle

Real example from ristretto Java library:
- **URL**: https://repo1.maven.org/maven2/org/leplus/ristretto/2.0.0/ristretto-2.0.0.jar.sigstore.json
- **Format**: Sigstore bundle v0.3
- **Response structure**:
  ```json
  {
    "mediaType": "application/vnd.dev.sigstore.bundle.v0.3+json",
    "verificationMaterial": {
      "tlogEntries": [{
        "logIndex": "<rekor-log-index>",
        "logId": { "keyId": "<base64>" },
        "kindVersion": { "kind": "hashedrekord", "version": "0.0.1" },
        "integratedTime": "<unix-timestamp>",
        "inclusionPromise": { "signedEntryTimestamp": "<base64>" },
        "inclusionProof": {
          "logIndex": "<index>",
          "rootHash": "<hash>",
          "treeSize": "<size>",
          "hashes": ["<base64>", ...],
          "checkpoint": { "envelope": "<signature>" }
        },
        "canonicalizedBody": "<base64-encoded-metadata>"
      }],
      "certificate": "<X.509-cert-raw-bytes>"
    },
    "messageSignature": {
      "messageDigest": {
        "algorithm": "SHA2_256",
        "digest": "<base64-sha256>"
      },
      "signature": "<base64-ecdsa-signature>"
    }
  }
  ```

**Understanding the Maven Central bundle**:
- `mediaType`: Sigstore bundle v0.3 format
- `tlogEntries`: Rekor transparency log entry with Merkle tree inclusion proof
- `certificate`: X.509 certificate containing OIDC identity claims (GitHub Actions details, workflow, git tags)
- `messageSignature`: ECDSA signature and SHA-256 digest of the JAR file
- `canonicalizedBody`: Base64-encoded metadata about the signed artifact

**Verification process**:
1. Extract certificate and verify against Sigstore Fulcio CA
2. Verify Rekor transparency log inclusion using `inclusionProof`
3. Verify signature matches JAR file digest
4. Validate OIDC identity from certificate matches expected publisher

**Example cosign verification**:
```bash
cosign verify-blob --bundle ristretto-2.0.0.jar.sigstore.json \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  --certificate-identity-regexp='^https://github.com/leplusorg/ristretto/.+' \
  ristretto-2.0.0.jar
```

### Example: RubyGems Sigstore Attestation

RubyGems uses Sigstore bundles with DSSE (Dead Simple Signing Envelope) format:
- **Format**: JSON attestation bundles uploaded during `gem push --attestation FILE`
- **Adoption tracking**: https://segiddins.github.io/are-we-attested-yet/
- **Bundle structure**: Follows standard Sigstore bundle specification similar to npm and Homebrew

**Publishing example** (from Rails gem):
```bash
# Attestation automatically added when publishing from GitHub Actions
gem push --attestation attestation.json rails-7.2.0.gem
```

**Verification example**:
```bash
gem sigstore_cosign_verify_bundle \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  --certificate-identity https://github.com/rails/rails/.github/workflows/release.yml@refs/tags/v7.2.0
```

**Bundle components**:
- **DSSE envelope**: Contains signature and statement
- **Certificate**: X.509 cert from Sigstore Fulcio with GitHub identity
- **Transparency log**: Rekor entry with inclusion proof
- **Statement**: in-toto format linking gem file to build provenance

The attestation confirms the gem was built and published from the specified GitHub Actions workflow.

### Example: Homebrew Bottle Attestation

Homebrew uses GitHub's artifact attestations:
- **Format**: in-toto Statement with SLSA Build L2 predicate
- **Storage**: GitHub's native attestation system
- **View attestations**: https://github.com/Homebrew/homebrew-core/attestations

**Attestation structure**:
```json
{
  "subject": [{
    "name": "bottle-filename.tar.gz",
    "digest": {
      "sha256": "7d01bc414859db57e055c814daa10e9c586626381ea329862ad4300f9fee78ce"
    }
  }],
  "predicateType": "https://slsa.dev/provenance/v1",
  "predicate": {
    "buildDefinition": {
      "buildType": "https://github.com/Homebrew/actions/...",
      "externalParameters": {
        "workflow": {
          "repository": "https://github.com/Homebrew/homebrew-core",
          "ref": "refs/heads/master"
        }
      }
    },
    "runDetails": {
      "builder": {
        "id": "https://github.com/Homebrew/actions/generate-build-provenance"
      },
      "metadata": {
        "invocationId": "https://github.com/Homebrew/homebrew-core/actions/runs/<run-id>"
      }
    }
  }
}
```

**Understanding the Homebrew attestation**:
- Links bottle to specific GitHub Actions workflow run
- SLSA Build L2 compliant provenance
- Stored in Sigstore bundle format with signature

**Verification example**:
```bash
# Method 1: Using Homebrew
HOMEBREW_VERIFY_ATTESTATIONS=1 brew install <formula>

# Method 2: Using cosign directly
cosign verify-blob-attestation \
  --bundle <bottle>.jsonl \
  --new-bundle-format \
  --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
  --certificate-identity="https://github.com/Homebrew/homebrew-core/.github/workflows/dispatch-rebottle.yml@refs/heads/master" \
  <bottle-file>
```

**What's attested**:
- Bottle was built by official Homebrew CI (not a third party)
- Specific GitHub Actions workflow that built it
- Git commit SHA of the formula
- Workflow run ID for complete audit trail

### Example: Interpreting Predicate Types

Different predicate types provide different kinds of attestations:

1. **SLSA Provenance** (`https://slsa.dev/provenance/v0.2` or `v1.0`):
   - Describes build process
   - Includes builder identity, materials (source repository), invocation parameters
   - Provides evidence about HOW the artifact was built

2. **PyPI Publish** (`https://docs.pypi.org/attestations/publish/v1`):
   - Minimal attestation (predicate is null or empty)
   - Confirms artifact was uploaded via Trusted Publisher
   - Publisher identity is in the bundle metadata (not predicate)
   - Provides evidence about WHO published (authenticated via OIDC)

3. **GitHub Artifact Attestations** (used by Homebrew):
   - Includes GitHub workflow information
   - Links artifact to specific GitHub Actions run
   - Provides GitHub-specific provenance metadata

### Verifying Attestations Manually

For hands-on verification of attestations:

1. **Fetch the attestation**: Use the ecosystem's API endpoint
2. **Extract the statement**: Base64 decode if necessary
3. **Inspect the predicate type**: Determines what is being attested
4. **Verify the signature**:
   - Check certificate against Sigstore Fulcio CA
   - Verify transparency log inclusion (Rekor)
   - Validate OIDC identity claims in certificate
5. **Cross-reference publisher metadata**: Confirm expected workflow/repository
6. **Verify digest**: Ensure `subject` digest matches actual artifact

## Notes on Trusted Publishing vs. Attestations

It's important to distinguish between **trusted publishing** and **attestations**:

- **Trusted Publishing**: An authentication mechanism using OIDC (OpenID Connect) that allows publishers to authenticate to package registries without long-lived credentials (API tokens). Publishers prove their identity through their CI/CD platform (e.g., GitHub Actions).

- **Attestations/Provenance**: Cryptographically signed metadata about how a package was built, including the build environment, source repository, and build process. Attestations provide verifiable claims that can be independently verified.

Ecosystems may have one without the other:
- **NuGet** and **Cargo** have trusted publishing but not yet attestations
- **Maven Central** has attestations but not OIDC-based trusted publishing
- **npm**, **PyPI**, and **RubyGems** have both

### Attestations Generated During Trusted Publishing

In ecosystems with both trusted publishing and attestations (npm, PyPI, RubyGems), attestations are often automatically generated as part of the trusted publishing workflow:

**Example: PyPI trusted publishing flow**
1. Package is published from GitHub Actions using OIDC token (no API key needed)
2. PyPI validates the OIDC token and authenticates the publisher
3. PyPI automatically generates attestations:
   - **PyPI Publish attestation**: Confirms package was uploaded via Trusted Publisher
   - **SLSA Provenance** (if available): Contains build provenance details
4. Attestations are signed using the OIDC identity
5. Attestations are uploaded to Sigstore Rekor transparency log
6. Attestations are made available via PyPI Integrity API

This tight integration means that using trusted publishing automatically provides attestations, creating a complete chain of trust from source repository → CI build → registry publication.

**Example: npm provenance**
- Publishing with `npm publish --provenance` from GitHub Actions automatically:
  - Creates SLSA v0.2 provenance statement
  - Signs with ephemeral key and Sigstore Fulcio certificate
  - Logs in Rekor transparency log
  - Stores attestation in npm registry

The combination of trusted publishing and attestations provides the strongest security guarantees: trusted publishing ensures authenticated uploads without long-lived credentials, while attestations provide cryptographically verifiable provenance of what was uploaded and how it was built.
