# Source Code URL Metadata Analysis

This document analyzes how different package managers handle source code URL metadata across ecosystems.

## 1. Key findings summary

_TBD after sections 2–7 are finalized._

## 2. Data Collection Overview

This section provides an overview of the ecosystems and package managers reviewed to determine whether they make source code URL information available as part of their metadata. For each package manager, we indicate the level of support for source code URL data and point to the relevant specification or documentation. This establishes the foundation for deeper analysis in subsequent sections.

### Rust Ecosystem — Cargo

**Source Code URL Information Available**: Yes, via the `repository` field in `Cargo.toml`

**Reference**: [Cargo Reference: The Manifest Format](https://doc.rust-lang.org/cargo/reference/manifest.html)

### Python Ecosystem — PyPI (pip)

**Source Code URL Information Available**: Yes, via `project_urls` (or legacy `home_page` field) in package metadata

**References**:
- [Python Packaging User Guide — Core Metadata Specifications](https://packaging.python.org/en/latest/specifications/core-metadata/)
- PEP 621 ([Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/))
- [Python Packaging User Guide — Dependency Specifiers](https://packaging.python.org/en/latest/specifications/dependency-specifiers/#dependency-specifiers)

### Container Ecosystem — Docker

**Source Code URL Information Available**: Yes, but loaded via registry API rather than embedded in images. Docker Hub and other registries can provide source code URLs through their metadata APIs, but this information is not part of the image itself.

**Reference**: [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)

### Go Ecosystem — Go Modules

**Source Code URL Information Available**: Yes, derived from the module path itself. Go module paths are URL-based (e.g., `github.com/user/repo`), and the module path directly encodes the source code location. There is no separate repository URL field in `go.mod`.

**References**:
- [Go Modules Reference](https://go.dev/ref/mod)
- [Go module proxy protocol](https://golang.org/ref/mod#protocol)

### JavaScript Ecosystem — npm

**Source Code URL Information Available**: Yes, via the `repository` field in `package.json`. The field can contain either a string URL or an object with `type` and `url` properties. npm surfaces this metadata through both its web interface and JSON API.

**References**:
- [npm package.json specification – repository field](https://docs.npmjs.com/cli/v10/configuring-npm/package-json#repository)
- [npm registry API reference](https://github.com/npm/registry/blob/main/docs/REGISTRY-API.md)

### PHP Ecosystem — Composer (Packagist)

**Source Code URL Information Available**: Yes, via the `source` field in `composer.json`, which contains `type` and `url` properties. Packagist surfaces this metadata on package pages and through its JSON API.

**References**:
- [Composer schema — source field](https://getcomposer.org/doc/04-schema.md#source)
- [Packagist API reference](https://packagist.org/apidoc)

## 3. Field Analysis

This section groups ecosystems according to how source code URL information can be specified in their package metadata. The focus here is on whether the declaration is unambiguous, ambiguous, or not supported at all, along with the types of definitions that are accepted in practice.

### Unambiguously specified

#### Rust Ecosystem — Cargo

- **Accepted definitions**:
  - String containing a repository URL in the `repository` field
  - String containing a homepage URL in the `homepage` field (used as fallback)
- Cargo provides dedicated fields for repository and homepage URLs in `Cargo.toml`. While the specification does not enforce URL validation or require specific URL formats, the semantic intent is clear: `repository` should point to the source code repository, while `homepage` represents the project website.
- The field names are standardized and unambiguous, though the content validation is minimal.

#### JavaScript Ecosystem — npm

- **Accepted definitions**:
  - Shorthand string: `"user/repo"` (implies GitHub)
  - Full URL string: `"https://github.com/user/repo.git"`
  - Object with type and URL: `{"type": "git", "url": "https://..."}`
  - Arrays occasionally appear in practice (not officially supported; tools typically use the first element)
- npm provides a dedicated `repository` field in `package.json` with well-documented formats. The specification explicitly supports multiple declaration styles, making it flexible but requiring parsing logic to normalize the various formats. Note that arrays are not part of the official specification, but some tools handle them defensively by taking the first element.
- The semantic meaning is unambiguous: the `repository` field indicates where the source code is hosted.

#### PHP Ecosystem — Composer (Packagist)

- **Accepted definitions**:
  - Object with `type` and `url` properties: `{"type": "git", "url": "https://..."}`
  - The `type` field indicates the VCS type (git, svn, hg, etc.)
  - The `url` field contains the repository URL
- Composer provides a structured `source` field in `composer.json` with a consistent object format. The schema is well-defined and the semantic intent is clear.
- Unlike npm's flexible formats, Composer requires a specific object structure, making parsing more predictable.

### Ambiguously specified

#### Python Ecosystem — PyPI (pip)

- **Accepted definitions**:
  - Dictionary of arbitrary URL labels in `project_urls` (e.g., `{"Homepage": "...", "Repository": "...", "Source": "..."}`)
  - Legacy `home_page` field (may or may not point to repository)
  - URLs embedded in package description text
- PyPI's `project_urls` field accepts arbitrary key-value pairs without standardized key names. While common conventions exist (e.g., "Repository", "Source", "Source Code"), package authors can use any labels they choose.
- The lack of a dedicated, required `repository` field means tools must implement heuristics to identify which URL represents the source code repository. Common strategies include:
  - Checking priority keys in a predefined order
  - Scanning all `project_urls` values for repository-like URLs
  - Falling back to `home_page` (which may be a marketing site rather than source code)
  - Parsing URLs from description text as a last resort
- This flexibility creates significant ambiguity, requiring complex detection logic and making repository URL extraction unreliable across the ecosystem.

#### Go Ecosystem — Go Modules

- **Accepted definitions**:
  - Module path that encodes the repository location (e.g., `github.com/user/repo`)
  - No dedicated repository URL field in `go.mod`
- Go modules use a unique approach where the module path itself serves as the repository identifier. The module path follows a URL-like format that includes the hosting platform and repository location.
- While this design is elegant for well-known platforms (GitHub, GitLab, Bitbucket), it creates ambiguity because:
  - Module paths may use custom domains with redirects (vanity URLs)
  - Converting a module path to a browsable repository URL requires knowledge of platform-specific conventions:
    - **GitHub**: `github.com/user/repo` → `https://github.com/user/repo` (straightforward conversion)
    - **GitLab**: `gitlab.com/group/project` → `https://gitlab.com/group/project` (may include nested groups)
    - **Bitbucket**: Module paths need different URL structures for Bitbucket Cloud vs. self-hosted instances
    - **Vanity domains**: Custom domains like `golang.org/x/tools` require following HTML meta tags or DNS TXT records to discover the actual repository (in this case `https://github.com/golang/tools`)
    - **Submodules**: Module paths like `github.com/org/repo/subpkg/v2` may point to subdirectories, requiring logic to identify the repository root
  - The `go.mod` file contains no explicit repository URL field
  - Tools must either scrape pkg.go.dev HTML or implement URL derivation logic for each platform
- The implicit nature of repository location makes automated extraction dependent on heuristics and external services.

### Unspecified

#### Container Ecosystem — Docker

- **Accepted definitions**:
  - No field in Docker images or Dockerfiles for repository URLs
  - External metadata available through Docker Hub registry API
  - Official library images hardcoded to `https://github.com/docker-library/official-images`
- Docker images themselves contain no repository URL metadata. The Dockerfile format and image manifest specifications do not include fields for source code location.
- Repository information, when available, exists only as external registry metadata maintained by Docker Hub or other registries. This information:
  - Is not embedded in or distributed with the image
  - Depends on publishers configuring source information in registry settings
  - Varies by registry (Docker Hub, GHCR, etc.)
  - Cannot be accessed offline or from the image artifact alone
- This absence of structured, embedded repository metadata makes Docker fundamentally different from other package ecosystems. Automated tools must rely entirely on registry APIs, which may be unavailable, incomplete, or inconsistent across different registries.

### Repository URL Stability and Redirects

Beyond the challenges of extracting repository URLs from package metadata, there are cross-ecosystem concerns about repository URL stability over time. Repository hosting platforms, particularly GitHub, support repository renames and transfers that create redirect chains. This introduces identity and deduplication challenges that affect all ecosystems relying on repository URLs as identifiers.

#### GitHub Repository Renames and Redirects

When a GitHub repository is renamed or transferred to a different user or organization, GitHub automatically creates HTTP redirects from the old URL to the new one. For example:
- Original URL: `https://github.com/olduser/oldname`
- Renamed to: `https://github.com/olduser/newname`
- Both URLs now resolve to the same repository

This creates several problems for package metadata:
1. **Multiple apparent packages**: Two packages declaring different repository URLs may actually point to the same repository after following redirects. Without redirect resolution, automated tools may treat them as distinct packages.
2. **Outdated metadata**: Package metadata published before a rename will contain the old URL. Unless the package is republished with updated metadata, consumers will encounter redirects.
3. **Redirect breakage**: If the old namespace is claimed by a new repository, the redirect breaks and the old URL points to unrelated code. This creates security and correctness risks.
4. **Deduplication challenges**: Tools attempting to deduplicate packages or track dependencies must resolve redirects to identify that `github.com/old/name` and `github.com/new/name` refer to the same repository.

#### Impact Across Ecosystems

This challenge affects all ecosystems that use repository URLs as part of package identification:
- **Rust (Cargo)**, **JavaScript (npm)**, **PHP (Composer)**: These ecosystems embed repository URLs in package metadata that is typically not updated after publication unless a new version is released.
- **Python (PyPI)**: The already-ambiguous URL extraction is further complicated by outdated URLs that now redirect.
- **Go (Go Modules)**: Module paths that include the repository location (e.g., `github.com/user/repo`) become stale after renames. Go's import path conventions mean that renaming a repository typically requires changing all import paths, but old module versions still reference the old path.

#### Mitigation Strategies

Tools working with repository URLs should consider:
1. **Redirect resolution**: Follow HTTP redirects to determine the canonical repository URL. Cache redirect mappings to avoid repeated requests.
2. **URL normalization**: Treat URLs that redirect to the same destination as equivalent during deduplication and comparison operations.
3. **Temporal awareness**: Recognize that repository URLs are point-in-time references that may change. Historical URLs may no longer be valid or may redirect elsewhere.
4. **Validation**: Periodically re-validate repository URLs to detect broken redirects or namespace hijacking.

## 4. Data Format Analysis

Source code URL metadata is not only expressed in different formats, but also stored in different locations across ecosystems. Some package managers require the source code URL to be declared directly in project source files, others embed it into the distributed package, and some expose it only through registry metadata or websites. These variations affect both the reliability of source code URL declarations and the ease with which automated tools can access them.

### Rust Ecosystem — Cargo

- **Data type**: String containing a URL
- **URL format support**: Any valid URL format (typically HTTPS URLs to Git hosting platforms)
- **Location**: Declared in `Cargo.toml` under the `[package]` section as the `repository` field. The manifest file is included in the `.crate` package uploaded to crates.io.
- **Fallback fields**: If `repository` is not present, the `homepage` field can be used as a fallback
- **Notes**: Both the primary repository field and homepage fallback are redistributed with the package. The crates.io API exposes both fields.

### Python Ecosystem — PyPI (pip)

- **Data type**: String containing a URL, typically within a dictionary of project URLs
- **URL format support**: Any valid URL format
- **Location**: Declared in project configuration files (`pyproject.toml`, `setup.cfg`, `setup.py`) under `project_urls` or the legacy `home_page` field. Available via PyPI registry API.
- **Fallback fields**: Complex fallback chain with multiple strategies:
  1. Priority keys in `project_urls`: `"Repository"`, `"Source"`, `"Source Code"`, `"Code"` (checked in order)
  2. Other URLs found in `project_urls` values
  3. Legacy `home_page` field
  4. Repository URL parsed from package description text
- **Notes**: PyPI has the most complex repository URL detection logic due to lack of standardization. The `project_urls` field allows arbitrary key names, requiring heuristic matching. GitHub sponsor links are explicitly excluded.

### Container Ecosystem — Docker

- **Data type**: String containing a URL, retrieved via Docker Hub API
- **URL format support**: GitHub URLs (primary support), potentially other hosting platforms
- **Location**: Not embedded in Docker images. Retrieved from Docker Hub registry API by querying image source information.
- **Fallback fields**:
  - Official library images: Hardcoded to `https://github.com/docker-library/official-images`
  - User images: Extracted from Docker Hub API source provider information
  - Returns `nil` if no repository information is available
- **Notes**: Unlike other ecosystems, repository URL is not part of the image artifact itself. It exists only as external registry metadata. Detection depends entirely on Docker Hub's API and whether publishers have configured source information.

### Go Ecosystem — Go Modules

- **Data type**: String containing a URL, derived from module path or extracted from pkg.go.dev
- **URL format support**: URLs derived from module paths (e.g., `github.com/user/repo` becomes `https://github.com/user/repo`)
- **Location**: Not declared in `go.mod`. The module path itself encodes the repository location. Repository metadata is displayed on pkg.go.dev but not stored in module files.
- **Fallback fields**:
  - Primary: HTML-scraped from pkg.go.dev page (which displays repository links)
  - Fallback: Algorithmically derive repository URL from the module path itself
  - Both `repository_url` and `homepage` typically use the same value
- **Notes**: Go's approach is unique—the module path IS the repository location. The `go.mod` file contains no separate repository field. Tools must either parse the module path or scrape pkg.go.dev to obtain a full URL.

### JavaScript Ecosystem — npm

- **Data type**: String or object containing repository information
- **URL format support**:
  - String shorthand: `"user/repo"` (assumes GitHub)
  - Object form: `{"type": "git", "url": "https://..."}`
  - Arrays may appear (not officially supported; tools handle defensively by using first element)
- **Location**: Declared in `package.json` under the `repository` field. Included in published package tarball and exposed via npm registry API.
- **Fallback fields**:
  - Primary: `latest_version.repository.url` (from the latest version's metadata)
  - Fallback: `package.homepage`
  - Excludes placeholder URLs: `npm/deprecate-holder` and `npm/security-holder`
- **Notes**: npm supports flexible repository declaration formats. The registry metadata preserves whatever format was published, requiring tools to handle both string shortcuts and full URL objects. Known placeholder repositories are explicitly filtered out.

### PHP Ecosystem — Composer (Packagist)

- **Data type**: Object containing repository type and URL
- **URL format support**: Object with `type` (e.g., "git", "svn") and `url` properties
- **Location**: Declared in `composer.json` under the `source` field. The manifest is included in distributed packages and available through Packagist API.
- **Fallback fields**:
  - Primary: `latest_version.source.url`
  - Fallback: `latest_version.homepage`
- **Notes**: Composer uses a structured `source` object that includes both the repository type and URL. This provides clear semantics about the version control system in use. The fallback to homepage is straightforward, following the same pattern as Cargo.

## 5. Access Patterns

Access to source code URL metadata varies across ecosystems. Some make it directly available from the project source or distribution, while others rely on registry infrastructure or provide no access at all.

### Rust Ecosystem — Cargo

- **Direct access**: Repository URL is available in the `Cargo.toml` file within the source code and redistributed in the `.crate` package. The manifest can be read directly from any downloaded crate.
- **CLI access**: The `cargo metadata` command provides repository information as part of the structured JSON output. The `cargo search` command displays basic package information but not repository URLs.
- **Registry access**: crates.io package pages prominently display repository links when available.
- **API access**: The crates.io JSON API exposes the `repository` field for each crate version (e.g., `https://crates.io/api/v1/crates/{crate}`). The homepage field is also available as a fallback.

### Python Ecosystem — PyPI (pip)

- **Direct access**: Repository URL may be declared in configuration files (`pyproject.toml`, `setup.cfg`, `setup.py`) under `project_urls` or `home_page`, but these declarations may or may not be preserved in built distributions (wheels or sdists). Reading from source is most reliable.
- **CLI access**: `pip show <package>` displays URLs for installed packages, but the output includes multiple URL types mixed together, requiring manual inspection. The tool does not query PyPI directly and only shows information for locally installed packages.
- **Registry access**: PyPI package pages display project URLs in a dedicated sidebar section. However, there is no standardized label, so repository URLs may appear under various names ("Repository", "Source", "Code", etc.).
- **API access**: The PyPI JSON API exposes `project_urls` and `home_page` fields (e.g., `https://pypi.org/pypi/{package}/json`). Consumers must implement heuristics to identify which URL represents the repository, as discussed in the Field Analysis section.

### Container Ecosystem — Docker

- **Direct access**: None. Docker images do not contain repository URL metadata. Inspecting an image with `docker inspect` reveals configuration and layer information but no source code location.
- **CLI access**: The Docker CLI provides no commands to retrieve repository URLs. The `docker inspect` command does not expose this information because it is not part of the image manifest.
- **Registry access**: Docker Hub and other container registries may display repository links on image pages, but this is optional and depends on publishers configuring source information in their registry settings. The presentation varies across registries (Docker Hub, GHCR, Quay.io, etc.).
- **API access**: Docker Hub provides APIs to query image metadata, which may include source repository information if configured by the publisher. However, this is registry-specific and not standardized. Other registries have different API structures and may not expose repository URLs at all.

### Go Ecosystem — Go Modules

- **Direct access**: Module paths in `go.mod` encode repository locations, but converting them to browsable URLs requires understanding platform conventions. The `go.mod` file contains no explicit repository URL field.
- **CLI access**: The `go` command does not provide a subcommand to retrieve repository URLs. Commands like `go list -m -json <module>` show module path and version information but not repository URLs. Tools must derive URLs from module paths.
- **Registry access**: pkg.go.dev displays repository links for modules, extracting them from module metadata or deriving them from module paths. The website also shows license information and documentation, making it the primary discovery point for Go modules.
- **API access**: The Go module proxy protocol serves `.mod`, `.zip`, and `.info` files but does not include repository metadata. To programmatically obtain repository URLs, tools must either scrape pkg.go.dev HTML or implement URL derivation logic based on module path conventions.

### JavaScript Ecosystem — npm

- **Direct access**: Repository URL is available in the `package.json` file within the source code and in the published tarball retrieved from the registry. The manifest can be extracted from any downloaded package.
- **CLI access**: The `npm view <package> repository` command displays the repository field from the registry. Other commands like `npm info` and `npm show` also expose this metadata. These commands query the registry, so they work without installing the package locally.
- **Registry access**: The npm website displays repository information prominently on package pages, typically with a direct link to the repository. The display handles both shorthand (`user/repo`) and full URL formats.
- **API access**: The npm registry JSON API exposes the `repository` field under each package version's metadata (e.g., `https://registry.npmjs.org/{package}`). The API returns the field exactly as published, so consumers must handle various formats (string, object, and occasionally arrays despite not being officially supported).

### PHP Ecosystem — Composer (Packagist)

- **Direct access**: Repository URL is available in the `composer.json` file within the package source under the `source` field. This file is included in distributed archives and source repositories.
- **CLI access**: The `composer show <package>` command displays the source URL for installed packages. It retrieves this information from the local `composer.lock` file or the package's manifest. The `composer info` command provides similar functionality.
- **Registry access**: Packagist displays source repository information prominently on package pages, including both the repository type (git, svn, etc.) and URL. The display is consistent across packages.
- **API access**: The Packagist API exposes source information for each package version through its JSON endpoints (e.g., `https://repo.packagist.org/p2/{vendor}/{package}.json`). The structured `source` object includes both type and URL, making parsing straightforward.

## 6. Quality Assessment

The quality of source code URL metadata across ecosystems varies widely, not only in terms of completeness but also in clarity and machine-readability. Below we evaluate coverage, reliability, and key limitations.

### Rust Ecosystem — Cargo

- **Coverage**: TBD
- **Reliability**: Good. The `repository` field in `Cargo.toml` has clear semantics, and the simple fallback to `homepage` provides a secondary source. Most published crates include repository information.
- **Limitations**:
  - The `repository` field is optional, not required for publication
  - No URL format validation at publish time; authors can provide invalid or placeholder URLs
  - The homepage fallback may point to project websites rather than source repositories
  - Some crates may omit both `repository` and `homepage` fields entirely

### Python Ecosystem — PyPI (pip)

- **Coverage**: TBD
- **Reliability**: Weak to mixed. The lack of a standardized repository field creates significant challenges. The `project_urls` dictionary accepts arbitrary keys, requiring heuristic matching that may fail or produce incorrect results.
- **Limitations**:
  - No dedicated `repository` field; must search through `project_urls` with uncertain key names
  - Priority key matching ("Repository", "Source", etc.) depends on community conventions that are not enforced
  - Many packages use `home_page` for marketing sites rather than source repositories
  - As a last resort, parsing URLs from description text is highly unreliable
  - GitHub sponsor links must be explicitly filtered out to avoid false positives
  - Older packages often have incomplete or missing URL metadata

### Container Ecosystem — Docker

- **Coverage**: TBD
- **Reliability**: Poor. Repository URLs are not part of the image artifact, making them fundamentally unreliable. Coverage depends entirely on whether publishers configure source information in registry settings.
- **Limitations**:
  - No repository metadata embedded in images or specified in Dockerfiles
  - Availability depends on registry-specific APIs and publisher configuration
  - Different registries (Docker Hub, GHCR, Quay.io) have different metadata structures
  - Official library images use a hardcoded repository URL that points to a metarepository, not the actual source
  - No offline access; requires registry API availability
  - No standardization across the container ecosystem

### Go Ecosystem — Go Modules

- **Coverage**: TBD
- **Reliability**: Mixed. For modules hosted on well-known platforms (GitHub, GitLab, Bitbucket), deriving repository URLs from module paths is reliable. For vanity URLs and custom domains, reliability decreases significantly.
- **Limitations**:
  - No explicit repository URL field in `go.mod`
  - Module paths encode repository location implicitly, requiring derivation logic
  - Vanity URLs and custom domains require DNS or HTTP resolution to discover actual repositories
  - Scraping pkg.go.dev HTML is fragile and depends on website structure remaining stable
  - No standardized way to obtain repository URLs through the Go toolchain or module proxy protocol
  - Submodules and monorepo packages may have paths that don't directly map to repository roots

### JavaScript Ecosystem — npm

- **Coverage**: TBD
- **Reliability**: Good. The dedicated `repository` field is well-documented and widely used. The specification supports multiple formats, which adds complexity but is manageable with proper parsing.
- **Limitations**:
  - The field supports multiple formats (string shorthand, full URL, object, array), requiring normalization logic
  - Shorthand format assumes GitHub, which may not always be correct
  - Some packages use placeholder repositories (`npm/deprecate-holder`, `npm/security-holder`) that must be filtered out
  - The `repository` field is optional; not all packages include it
  - Legacy packages may have incorrect or outdated repository URLs
  - Older package versions may lack repository fields that were added in later versions

### PHP Ecosystem — Composer (Packagist)

- **Coverage**: TBD
- **Reliability**: Good. The structured `source` object with explicit `type` and `url` fields provides clear, machine-readable repository information. The fallback to `homepage` is simple and predictable.
- **Limitations**:
  - The `source` field is optional, not required for package publication
  - Some packages may only provide `homepage`, which might not point to source code
  - The `source` URL typically points to the package's own repository, which may differ from the primary project repository in the case of forks or mirrors
  - VCS type information is included but may not always be accurate

## 7. Transformation Requirements

To make source code URL information usable across ecosystems, processes must account for the different formats and locations where URLs are declared. The goal is to produce validated and normalized source code URLs from heterogeneous sources.

### Rust Ecosystem — Cargo

1. Read the `repository` field from `Cargo.toml` under the `[package]` section.
   - If present and non-empty, use this value as the primary repository URL.
2. If the `repository` field is absent or empty, read the `homepage` field as a fallback.
   - Note that homepage URLs may point to project websites rather than source repositories.
3. Validate and normalize the extracted URL:
   - Ensure it is a well-formed URL
   - Standardize the protocol (prefer HTTPS)
   - Remove trailing slashes and `.git` suffixes for consistency
4. If neither field is present, the repository URL cannot be determined from package metadata.

### Python Ecosystem — PyPI (pip)

1. Query the PyPI JSON API to retrieve package metadata (`https://pypi.org/pypi/{package}/json`).
2. Extract the `project_urls` dictionary from `info.project_urls`.
3. Search for repository URLs using a priority key matching strategy:
   - Check for these keys in order: `"Repository"`, `"Source"`, `"Source Code"`, `"Code"`
   - Use the first matching key's value
   - Parse and validate the URL; skip GitHub sponsor URLs
4. If no priority keys match, scan all values in `project_urls` for repository-like URLs:
   - Look for URLs containing common hosting platform domains (github.com, gitlab.com, etc.)
   - Exclude sponsor, donation, and documentation URLs
5. If `project_urls` yields no results, fall back to the `home_page` field from `info.home_page`.
   - Be aware that this may point to a marketing site rather than source code
6. As a last resort, attempt to parse repository URLs from the package description text.
   - This is highly unreliable and should only be used when all other methods fail
7. Normalize the extracted URL using standard URL parsing and validation.

### Container Ecosystem — Docker

1. For official library images (e.g., `library/nginx`), use the hardcoded repository URL:
   - `https://github.com/docker-library/official-images`
   - Note that this points to a metarepository containing Dockerfiles, not the actual source code
2. For user images, query the Docker Hub API to retrieve image metadata.
   - Check for source repository information in the API response
   - If a GitHub provider is configured, construct the repository URL from the provider metadata
3. If the Docker Hub API returns no repository information, return `nil` or indicate that no URL is available.
4. For images hosted on registries other than Docker Hub (GHCR, Quay.io, etc.):
   - Check if the registry provides a metadata API with source information
   - Parse the registry-specific response format
   - Be aware that metadata structure varies significantly across registries
5. Validate and normalize any extracted URLs.
6. Document that Docker images lack embedded repository metadata, making offline extraction impossible.

### Go Ecosystem — Go Modules

1. Extract the module path from `go.mod` or module metadata.
2. Attempt to scrape pkg.go.dev for repository URL:
   - Fetch the module page HTML from `https://pkg.go.dev/{module_path}`
   - Parse the HTML and extract the repository link from the `.UnitMeta-repo a` element
   - If successful, use this as the primary repository URL
3. If pkg.go.dev scraping fails, derive the repository URL from the module path:
   - Apply URL derivation logic to convert the module path to a repository URL
   - For common platforms (github.com, gitlab.com, bitbucket.org), convert module path to HTTPS URL
   - For example: `github.com/user/repo` → `https://github.com/user/repo`
4. For vanity URLs and custom domains:
   - Perform DNS/HTTP resolution to discover the actual repository location
   - Follow redirects and parse HTML meta tags for go-import directives
   - Extract the repository URL from the VCS metadata
5. Handle submodules and monorepo paths:
   - The module path may point to a subdirectory within a repository
   - Strip subpaths to obtain the root repository URL when appropriate
6. Validate and normalize the extracted URL.
7. Document that the same URL should be used for both `repository_url` and `homepage` fields, as Go does not distinguish between them.

### JavaScript Ecosystem — npm

1. Read the `repository` field from `package.json` (prefer version-level metadata, fall back to package-level).
2. Parse the `repository` value based on its format:
   - **String shorthand** (e.g., `"user/repo"`): Prepend `https://github.com/` to construct the full URL
   - **Full URL string**: Use as-is, but validate and normalize
   - **Object** (e.g., `{"type": "git", "url": "..."}`): Extract the `url` property
   - **Array** (not officially supported but may appear): Use the first element and apply the appropriate parsing logic
3. If the `repository` field is absent or empty, fall back to the `homepage` field.
4. Filter out known placeholder repositories:
   - Exclude `https://github.com/npm/deprecate-holder`
   - Exclude `https://github.com/npm/security-holder`
5. Validate and normalize the extracted URL:
   - Ensure it is well-formed
   - Standardize protocol (prefer HTTPS)
   - Remove `.git` suffixes and trailing slashes
   - Handle git+https:// and git+ssh:// URL schemes by converting to standard HTTPS URLs
6. If no valid repository URL can be determined, return `nil` or an empty value.

### PHP Ecosystem — Composer (Packagist)

1. Read the `source` field from `composer.json` under the package version metadata.
   - This is typically an object with `type` and `url` properties
   - Example: `{"type": "git", "url": "https://github.com/vendor/package.git"}`
2. Extract the `url` property from the `source` object.
   - If present and non-empty, use this as the primary repository URL
3. If the `source` field is absent or the `url` is empty, fall back to the `homepage` field.
   - Be aware that homepage URLs may point to project websites rather than source repositories
4. Validate and normalize the extracted URL:
   - Ensure it is well-formed
   - Standardize protocol (prefer HTTPS)
   - Remove `.git` suffixes and trailing slashes
5. Optionally preserve the `type` field to indicate the version control system (git, svn, hg, etc.).
6. If neither `source` nor `homepage` is available, the repository URL cannot be determined from package metadata.
