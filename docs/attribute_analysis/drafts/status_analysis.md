# Package Status Metadata Analysis

This document analyzes how different package manager registries expose package and version status metadata, including deprecation, removal, yanking, and other lifecycle states.

## 1. Key findings summary

_TBD after sections 2-7 are finalized._

## 2. Data Collection Overview

Package status metadata indicates whether a package or specific version is active, deprecated, removed, or otherwise restricted. This information is critical for supply chain security, dependency management, and automated tooling. Registries handle status in fundamentally different ways: some track status at the package level, others at the version level, and some at both.

### Rust Ecosystem - Cargo

**Status Information Available**: Version-level yanking with optional message (yank reasons added as 2024h2 goal)

**References**:
- [Cargo Book - Publishing](https://doc.rust-lang.org/cargo/reference/publishing.html)
- [crates.io Development Update (Feb 2025)](https://blog.rust-lang.org/2025/02/05/crates-io-development-update/)

### Python Ecosystem - PyPI

**Status Information Available**: Package-level lifecycle status (active, archived, quarantined, deprecated); version-level yanking with reason

**References**:
- [PyPI JSON API](https://warehouse.pypa.io/api-reference/json/)
- [PEP 592 - Adding "Yank" Support to the Simple API](https://peps.python.org/pep-0592/)
- [PEP 792 - Project Status Markers for the Simple Index](https://peps.python.org/pep-0792/)
- [PyPI Blog - Project Status Markers (Aug 2025)](https://blog.pypi.org/posts/2025-08-14-project-status-markers/)

### JavaScript Ecosystem - npm

**Status Information Available**: Version-level deprecation messages; package-level inference from version states

**Reference**: [npm registry API](https://github.com/npm/registry/blob/main/docs/REGISTRY-API.md)

### Go Ecosystem - Go Modules

**Status Information Available**: Version-level retraction via go.mod directive

**References**:
- [Go Modules Reference - Retract](https://go.dev/ref/mod#go-mod-file-retract)
- [pkg.go.dev](https://pkg.go.dev)

### PHP Ecosystem - Composer (Packagist)

**Status Information Available**: Package-level abandonment with optional replacement suggestion

**References**:
- [Packagist API](https://packagist.org/apidoc)
- [Composer schema](https://getcomposer.org/doc/04-schema.md)

### Dart Ecosystem - Pub

**Status Information Available**: Package-level discontinuation flag

**Reference**: [Pub API](https://pub.dev/help/api)

### Ruby Ecosystem - RubyGems

**Status Information Available**: Version yanking via CLI and API; 2024 policy restricts yanking for gems over 100k downloads or older than 30 days

**References**:
- [RubyGems API](https://guides.rubygems.org/rubygems-org-api/)
- [April 2024 RubyGems Updates](https://blog.rubygems.org/2024/05/15/april-rubygems-updates.html)

### .NET Ecosystem - NuGet

**Status Information Available**: Version-level deprecation with reasons (Legacy, Critical bugs, Other) and alternate package suggestions; version-level listing/unlisting

**References**:
- [NuGet API](https://docs.microsoft.com/en-us/nuget/api/overview)
- [Deprecating packages on nuget.org](https://learn.microsoft.com/en-us/nuget/nuget-org/deprecate-packages)

### Elixir Ecosystem - Hex

**Status Information Available**: Version retirement with structured reasons (renamed, deprecated, security, invalid, other) and message

**References**:
- [Hex FAQ](https://hex.pm/docs/faq)
- [mix hex.retire](https://hexdocs.pm/hex/Mix.Tasks.Hex.Retire.html)

### VS Code Extensions - OpenVSX

**Status Information Available**: Version-level downloadable flag; namespace verification status

**Reference**: [OpenVSX API](https://open-vsx.org/swagger-ui/)

### Java Ecosystem - Maven Central

**Status Information Available**: No native deprecation or status mechanism in Maven Central

**Notes**: Maven Central does not provide a built-in way to mark artifacts as deprecated. Some projects use naming conventions (e.g., publishing a final version with "deprecated" in the description) or documentation. Third-party tools like the `artifact-deprecation` project attempt to fill this gap.

**Reference**: [Maven Central](https://central.sonatype.org/)

### Swift Ecosystem - Swift Package Manager

**Status Information Available**: No central registry; status derived entirely from source repository

**Notes**: Swift PM is decentralized with packages referenced by repository URL. Package status must be inferred from repository metadata (archived, description) or README content. The Swift Package Index (swiftpackageindex.com) is a community registry but does not provide status fields.

**Reference**: [Swift Package Manager](https://swift.org/package-manager/)

### GitHub Actions

**Status Information Available**: Repository metadata (archived, visibility); no registry-level status

**Notes**: GitHub Actions are referenced directly by repository. An archived or deleted repository makes the action unusable. The GitHub Marketplace does not expose deprecation status for actions.

**Reference**: [GitHub Actions](https://docs.github.com/en/actions)

### macOS/Linux Ecosystem - Homebrew

**Status Information Available**: Formula/cask-level deprecation and disabling with structured reasons, dates, and optional replacement suggestions

**References**:
- [Deprecating, Disabling and Removing Formulae](https://docs.brew.sh/Deprecating-Disabling-and-Removing-Formulae)
- [Homebrew Ruby API - Formula](https://docs.brew.sh/rubydoc/Formula)

## 3. Field Analysis

### Package-Level Status Fields

#### npm
- **Field**: No explicit package-level status field
- **Inference**: Package considered deprecated if all non-prerelease versions have `deprecated` field set
- **Security removals**: Replaced with holder packages having description "security holding package"
- **Unpublished**: Package exists but `versions` object is empty

#### Packagist (PHP)
- **Field**: `abandoned`
- **Type**: String or boolean
- **Values**:
  - `false` or absent: Package is maintained
  - `true`: Package is abandoned with no replacement
  - `"vendor/replacement"`: Package is abandoned, string contains suggested replacement
- **Location**: Package metadata root

#### Pub (Dart)
- **Field**: `isDiscontinued`
- **Type**: Boolean
- **Values**: `true` indicates package is no longer maintained
- **Location**: Package API response root

#### PyPI
- **Field**: `project-status` (PEP 792)
- **Type**: Object with `state` and optional `reason` strings
- **Values** (mutually exclusive, exactly one applies):
  - `active` (default): Project is actively maintained
  - `archived`: Project does not expect to be updated in the future
  - `quarantined`: Project is considered generally unsafe for use (e.g., malware)
  - `deprecated`: Project is considered obsolete, may have been superseded
- **Location**: JSON API response root; HTML Simple Index via meta tags
- **Reference**: [PEP 792](https://peps.python.org/pep-0792/)

#### Homebrew
- **Methods**: `deprecate!` and `disable!` in formula/cask definitions
- **Fields**:
  - `date`: Date of deprecation/disabling (required)
  - `because`: Reason symbol (required)
  - `replacement`: String shown in install help text (optional)
  - `replacement_formula`: Specific replacement formula (optional)
  - `replacement_cask`: Specific replacement cask (optional)
- **Reason values** (symbols):
  - `does_not_build`: Formula fails to build
  - `no_license`: No license specified
  - `repo_archived`: Source repository has been archived
  - `repo_removed`: Source repository has been removed
  - `unmaintained`: No longer maintained upstream
  - `unsupported`: No longer supported
  - `deprecated_upstream`: Deprecated by upstream project
  - `versioned_formula`: Versioned formula no longer needed
  - `checksum_mismatch`: Checksum verification failed
- **Lifecycle**: Deprecated formulae show warnings; disabled formulae cannot be installed; removed after 1 year of being disabled
- **Example**:
```ruby
deprecate! date: "2024-01-10", because: :repo_archived, replacement: "new-formula"
```

### Version-Level Status Fields

#### Cargo (Rust)
- **Fields**: `yanked`, `yank_message`
- **Types**: Boolean, String (optional)
- **Location**: Each version object in API response
- **Behavior**: Yanked versions are excluded from default resolution but can still be fetched if explicitly specified
- **Example**:
```json
{
  "num": "1.0.0",
  "yanked": true,
  "yank_message": "Critical security vulnerability, use 1.0.1"
}
```

#### PyPI (Python)
- **Fields**: `yanked`, `yanked_reason`
- **Types**: Boolean, String (optional)
- **Location**: Each file object within release arrays
- **Behavior**: Yanked versions hidden from default pip resolution unless pinned exactly
- **Example**:
```json
{
  "releases": {
    "1.0.0": [{
      "yanked": true,
      "yanked_reason": "Broken release, missing dependencies"
    }]
  }
}
```

#### npm (JavaScript)
- **Field**: `deprecated`
- **Type**: String (deprecation message) or absent
- **Location**: Each version object
- **Behavior**: Deprecated versions can still be installed; npm CLI shows warning
- **Example**:
```json
{
  "versions": {
    "1.0.0": {
      "deprecated": "This version has a critical bug, please upgrade to 2.0.0"
    }
  }
}
```

#### Go Modules
- **Mechanism**: `retract` directive in go.mod
- **Location**: Module's own go.mod file, displayed on pkg.go.dev
- **Behavior**: Retracted versions excluded from version selection by go command
- **Note**: Not exposed via API; must parse go.mod or scrape pkg.go.dev HTML
- **Example** (in go.mod):
```
retract (
    v1.0.0 // Security vulnerability
    [v1.1.0, v1.2.0] // Broken releases
)
```

#### NuGet (.NET)
- **Listing field**: `listed` boolean in catalog entry
- **Deprecation fields**: `deprecation` object containing:
  - `reasons`: Array of strings (`Legacy`, `CriticalBugs`, `Other`)
  - `alternatePackage`: Object with `id` and optional `range` for recommended replacement
  - `message`: Custom message (only displayed on nuget.org, not in CLI tools)
- **Behavior**:
  - Unlisted versions hidden from search but installable if version specified exactly
  - Deprecated versions remain listed and discoverable, but display warnings
- **Additional**: Gallery may show deletion messages in HTML:
  - "This package has been deleted from the gallery."
  - "This package's content is hidden"
- **Reference**: [Deprecating packages on nuget.org](https://learn.microsoft.com/en-us/nuget/nuget-org/deprecate-packages)

#### Hex (Elixir)
- **Fields**: `retirement` object containing `reason` and `message`
- **Reason values**:
  - `renamed`: Package has been renamed (include new package name in message)
  - `deprecated`: Package has been deprecated (include replacement in message if available)
  - `security`: Package has a security vulnerability
  - `invalid`: Package is invalid (e.g., does not compile correctly)
  - `other`: Any other reason (clarify in message)
- **Message**: Required field, up to 140 characters
- **Location**: Version metadata in API response
- **Reference**: [mix hex.retire](https://hexdocs.pm/hex/Mix.Tasks.Hex.Retire.html)

#### OpenVSX
- **Field**: `downloadable`
- **Type**: Boolean
- **Location**: Version detail response
- **Behavior**: `false` indicates version has been yanked/withdrawn

## 4. Data Format Analysis

### Cargo (crates.io)

**API Endpoint**: `https://crates.io/api/v1/crates/{name}`

**Response structure**:
```json
{
  "crate": { ... },
  "versions": [
    {
      "id": 123456,
      "num": "1.0.0",
      "yanked": false,
      "yank_message": null,
      "created_at": "2023-01-01T00:00:00Z"
    },
    {
      "id": 123455,
      "num": "0.9.0",
      "yanked": true,
      "yank_message": "Security issue CVE-2023-XXXX",
      "created_at": "2022-06-01T00:00:00Z"
    }
  ]
}
```

### PyPI

**JSON API Endpoint**: `https://pypi.org/pypi/{name}/json`

**Response structure**:
```json
{
  "info": { ... },
  "releases": {
    "1.0.0": [
      {
        "filename": "package-1.0.0.tar.gz",
        "yanked": false,
        "yanked_reason": null
      }
    ],
    "0.9.0": [
      {
        "filename": "package-0.9.0.tar.gz",
        "yanked": true,
        "yanked_reason": "Accidentally published with test credentials"
      }
    ]
  },
  "project-status": {
    "state": "deprecated",
    "reason": "This project has been superseded by new-package"
  }
}
```

**Simple Index (HTML, PEP 792)**:
```html
<meta name="pypi:project-status" content="quarantined"/>
<meta name="pypi:project-status-reason" content="Malware detected"/>
```

**Simple Index (JSON, PEP 792)**:
```json
{
  "meta": {
    "api-version": "1.4"
  },
  "name": "package-name",
  "project-status": {
    "state": "quarantined",
    "reason": "Malware detected"
  },
  "files": [ ... ]
}
```

### npm

**API Endpoint**: `https://registry.npmjs.org/{name}`

**Response structure**:
```json
{
  "name": "package-name",
  "description": "...",
  "versions": {
    "1.0.0": {
      "name": "package-name",
      "version": "1.0.0"
    },
    "0.9.0": {
      "name": "package-name",
      "version": "0.9.0",
      "deprecated": "This version contains a critical vulnerability. Upgrade to 1.0.0."
    }
  }
}
```

**Security holder packages**:
```json
{
  "name": "malicious-package",
  "description": "security holding package",
  "versions": {}
}
```

### Packagist

**API Endpoint**: `https://packagist.org/packages/{vendor}/{name}.json`

**Response structure**:
```json
{
  "package": {
    "name": "vendor/package",
    "abandoned": "vendor/new-package",
    "versions": { ... }
  }
}
```

Alternative abandoned values:
- `"abandoned": false` - not abandoned
- `"abandoned": true` - abandoned with no replacement
- `"abandoned": "other/package"` - abandoned, use this instead

### Pub

**API Endpoint**: `https://pub.dev/api/packages/{name}`

**Response structure**:
```json
{
  "name": "package_name",
  "isDiscontinued": true,
  "latest": { ... },
  "versions": [ ... ]
}
```

### NuGet

**Registration Endpoint**: `https://api.nuget.org/v3/registration5-gz-semver2/{name}/index.json`

**Catalog entry structure** (with deprecation):
```json
{
  "items": [{
    "items": [{
      "catalogEntry": {
        "version": "1.0.0",
        "listed": true,
        "deprecation": {
          "reasons": ["Legacy"],
          "alternatePackage": {
            "id": "NewPackage",
            "range": "*"
          },
          "message": "This package is no longer maintained"
        }
      }
    }]
  }]
}
```

**Deprecation reasons**: `Legacy`, `CriticalBugs`, `Other`

### Hex

**API Endpoint**: `https://hex.pm/api/packages/{name}/releases/{version}`

**Response structure** (retired version):
```json
{
  "version": "1.0.0",
  "retirement": {
    "reason": "security",
    "message": "CVE-2023-XXXX: Remote code execution vulnerability"
  }
}
```

**Retirement reasons**: `other`, `invalid`, `security`, `deprecated`, `renamed`

## 5. Access Patterns

### Cargo
- **API**: `yanked` and `yank_message` fields in version objects
- **CLI**: `cargo yank --version 1.0.0` to yank; `cargo yank --version 1.0.0 --undo` to reverse
- **Web**: crates.io shows "yanked" badge on version pages

### PyPI
- **JSON API**: `project-status` object with `state` and `reason` (PEP 792); `yanked` and `yanked_reason` in release file objects (PEP 592)
- **Simple API (HTML)**: `pypi:project-status` and `pypi:project-status-reason` meta tags; `data-yanked` attribute on file links
- **Simple API (JSON)**: `project-status` object in response root
- **CLI**: `pip index versions {package}` excludes yanked by default
- **Web**: pypi.org shows status indicators and "yanked" badges with reason tooltips

### npm
- **API**: `deprecated` string in version objects
- **CLI**: `npm deprecate package@version "message"` to deprecate; empty message to undeprecate
- **Web**: npmjs.com shows deprecation banner on package pages

### Go
- **go.mod**: `retract` directive declares retracted versions
- **CLI**: `go list -m -versions` excludes retracted; `go get` warns about retracted
- **Web**: pkg.go.dev shows "retracted" chip next to version numbers

### Packagist
- **API**: `abandoned` field in package response
- **CLI**: Composer warns when installing abandoned packages
- **Web**: packagist.org shows "Abandoned!" banner with replacement link if available
- **Marking**: Package owners mark abandonment via web interface

### Pub
- **API**: `isDiscontinued` boolean in package response
- **CLI**: `dart pub` shows warning for discontinued packages
- **Web**: pub.dev shows "discontinued" badge

### NuGet
- **API**: `listed` boolean and `deprecation` object in catalog entries
- **CLI**: `dotnet list package --deprecated` shows deprecated packages; unlisted packages hidden from `dotnet search` but installable with exact version
- **Web**: nuget.org shows deprecation warnings with reasons and alternate package suggestions; hides unlisted versions by default
- **Marking**: Package owners deprecate/unlist via web interface; deprecation REST API available (issue #8873)

### Hex
- **API**: `retirement` object in release response
- **CLI**: `mix hex.retire {package} {version} {reason}` to retire
- **Web**: hex.pm shows retirement reason and message

### Homebrew
- **Formula files**: `deprecate!` and `disable!` methods in Ruby formula definitions
- **CLI**: `brew info <formula>` shows deprecation/disable status with reason and date
- **Web**: formulae.brew.sh shows status badges
- **JSON API**: `https://formulae.brew.sh/api/formula.json` includes `deprecated`, `disabled`, `deprecation_date`, `deprecation_reason`, `disable_date`, `disable_reason` fields
- **Behavior**: Deprecated formulae install with warning; disabled formulae refuse to install

## 6. Quality Assessment

### Feature Comparison

| Ecosystem | Package Status | Version Status | Status Message | Replacement Suggestion | Reversible |
|-----------|---------------|----------------|----------------|----------------------|------------|
| Cargo | No | Yes (yanked) | Yes (yank_message) | No | Yes |
| PyPI | Yes (PEP 792: archived, quarantined, deprecated) | Yes (yanked) | Yes (reason field, yanked_reason) | No | Yes |
| npm | Inferred | Yes (deprecated) | Yes (message is the field) | No | Yes |
| Go | No | Yes (retract) | Yes (comment in go.mod) | No | Yes |
| Packagist | Yes (abandoned) | No | No | Yes | Yes |
| Pub | Yes (isDiscontinued) | No | No | No | Yes |
| NuGet | No | Yes (deprecated, unlisted) | Yes (message field) | Yes (alternatePackage) | Yes |
| RubyGems | No | Yes (yank) | No | No | Yes |
| Hex | No | Yes (retirement) | Yes (message, required) | Via "renamed" reason | Yes |
| OpenVSX | No | Yes (downloadable) | No | No | Unknown |
| Homebrew | Yes (deprecated, disabled) | No | Yes (reason symbols) | Yes (replacement fields) | Yes |
| Maven | No | No | No | No | N/A |
| Swift PM | Via repository | No | Via repository | No | N/A |
| Actions | Via repository | No | Via repository | No | N/A |

### Limitations

**Inconsistent terminology**: Registries use different terms for similar concepts:
- "yanked" (Cargo, PyPI, RubyGems)
- "deprecated" (npm)
- "retracted" (Go)
- "retired" (Hex)
- "unlisted" (NuGet)

**Package vs version granularity**: Some registries only support package-level status (Packagist, Pub), while others only support version-level (Cargo, Go). npm is unique in having version-level status that can be aggregated to infer package-level status.

**Message support varies**: Cargo, PyPI, npm, Go, and Hex support explanatory messages. Packagist and Pub do not.

**Replacement suggestions**: Only Packagist explicitly supports suggesting a replacement package. Hex's "renamed" retirement reason implies a replacement but doesn't specify it.

**API consistency**: Go's retraction is declared in go.mod rather than registry metadata, requiring different access patterns than other ecosystems.

## 7. Additional Notes

### Security Removals

npm has a unique pattern for security-related removals where packages are replaced with "holder" packages:
- `npm/security-holder`: For packages removed due to security issues
- `npm/deprecate-holder`: For packages removed for other policy violations

These holder packages have `description: "security holding package"` and empty `versions` objects.

### Soft vs Hard Removal

Most registries distinguish between:
- **Soft removal** (yanking/deprecation): Version metadata remains accessible; version cannot be resolved by default but can be fetched if explicitly specified
- **Hard removal**: Package or version completely removed from registry; returns HTTP 404

Soft removal is preferred as it prevents breaking existing builds that depend on specific versions via lockfiles.

### Project Lifecycle Status (PyPI, PEP 792)

PEP 792 defines a standardized set of project status markers for PyPI:

- **active**: Default state, project is actively maintained
- **archived**: Project does not expect future updates (author-initiated)
- **quarantined**: Project is considered unsafe, e.g., due to malware (index-initiated)
- **deprecated**: Project is obsolete, may have been superseded (author-initiated)

Each project has exactly one status at any time. The `quarantined` status is typically set by the index (PyPI) rather than the package author, used for packages under review or confirmed to contain malware. This is distinct from `deprecated` which is author-initiated.

Status is exposed via both the JSON API (`project-status.state`, `project-status.reason`) and Simple Index (HTML meta tags or JSON `project-status` object).

**Implementation timeline**:
- November 2024: Quarantine functionality introduced
- January 2025: Archival feature built on quarantine infrastructure
- August 2025: Full PEP 792 status markers in API responses

Archiving a project also prevents further uploads, ensuring no new releases are pushed to unmaintained software. Project owners can archive via their project's settings page on PyPI.

### RubyGems Yank Policy (2024)

As of April 2024, RubyGems set a provisional limit on gems that can be yanked without public review. Gems with over 100,000 downloads or those older than 30 days require coordination through RubyGems staff. This aligns more closely with other ecosystems that restrict deletions of widely-used packages.

### Repository-Derived Status Signals

For package managers that use source repositories (especially GitHub) as their primary source, repository metadata can provide status signals that the registry itself may not track.

**GitHub Repository Status Fields**:
- `archived`: Boolean indicating the repository is read-only and no longer actively maintained
- `disabled`: Repository has been disabled (rare, typically due to ToS violations)
- `visibility`: Repository may have been made private or deleted entirely (404 response)
- `description`: May contain deprecation notices like "DEPRECATED", "No longer maintained", "Use X instead"

**Ecosystems heavily dependent on repository status**:

| Ecosystem | Source Relationship | Repository Status Relevance |
|-----------|--------------------|-----------------------------|
| Go | Module path is the repository URL | High - no registry-level status; repository archived/removed is primary signal |
| Swift PM | Package URL points to repository | High - no central registry; repository is the only source |
| GitHub Actions | Repository is the package | High - action unusable if repository archived/removed/private |
| Carthage | Package URL points to repository | High - decentralized; repository status is only status |
| Packagist | `source` field links to repository | Medium - has `abandoned` field, but repository status provides additional signal |
| Homebrew | Formula references repository | Medium - formulae can be deprecated independently |

**Detecting deprecation from repository content**:

Beyond structured metadata, deprecation signals may appear in:
- **README.md**: Badges, banners, or text indicating deprecation (e.g., "This project is deprecated", "No longer maintained")
- **Repository description**: Short text visible in GitHub UI and API
- **Latest commit messages**: May indicate final/archival commits
- **Topics/tags**: Some projects add "deprecated", "unmaintained", or "archived" topics

**GitHub API access**:

Repository metadata is available via the GitHub API:
```
GET https://api.github.com/repos/{owner}/{repo}
```

Response includes:
```json
{
  "archived": true,
  "disabled": false,
  "description": "DEPRECATED: Use new-package instead",
  "topics": ["deprecated", "unmaintained"]
}
```

**Automated repository status integration**:

Some registries automatically incorporate repository status:
- **Private Packagist**: Automatically marks packages as abandoned when the GitHub repository is archived
- **Packagist**: The `abandoned` property in composer.json can be set, and Private Packagist syncs this automatically
- **Homebrew**: Formulae can be marked as deprecated independently of repository status, but repository archival is often a trigger for deprecation

**Limitations of repository-derived status**:

- Repository status may not reflect package status (monorepos with multiple packages)
- Repository may be archived but package still functional and secure
- README deprecation notices are unstructured and require text parsing
- Repository transfers/renames create redirect chains that complicate tracking
- Private repositories return 404, indistinguishable from deleted repositories without authentication
- Rate limiting on GitHub API affects large-scale status checking

**Ecosystems with no registry status that benefit most from repository signals**:

- **Go Modules**: The module proxy provides no status metadata; repository archived status on GitHub/GitLab is the primary deprecation signal
- **Swift Package Manager**: Fully decentralized with no registry; repository status is the only status
- **GitHub Actions**: The repository IS the package; archived repositories make actions effectively deprecated
- **Carthage**: Similar to Swift PM; repository-based with no central status tracking
