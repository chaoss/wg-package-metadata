# License Metadata Analysis — Go Ecosystem

This document is part of a broader research effort by the CHAOSS WG Package Metadata group analyzing how license information is captured and exposed across package ecosystems. The full cross-ecosystem analysis covers 35 package managers, including Go, Rust (Cargo), Python (PyPI), JavaScript (npm), PHP (Composer), and Alpine Linux (apk), among others. It is available in the [License Metadata Analysis](../../../attribute_analysis/drafts/license_analysis.md) document. Supporting data can be found in the [coverage results](../../../attribute_analysis/drafts/license_coverage_results.txt), the [per-ecosystem summary](../../../attribute_analysis/drafts/license_summary.csv), and the [appendix with registry-level license distribution data](../../../attribute_analysis/drafts/license_appendix.md).

This document distills the Go-relevant findings from that research for review by Go module maintainers.

---

## 1. Key Findings Summary

Across all ecosystems studied, we grouped package managers into three categories based on how license information is declared:

**Unambiguously specified** — a structured field exists with defined semantics (typically SPDX). Examples: Rust (Cargo), JavaScript (npm), PHP (Composer).

**Ambiguously specified** — license information is present but not in a structured field; detection depends on file scanning or heuristics. Examples: Go (Go Modules), Python (PyPI).

**Unspecified** — no mechanism for license metadata exists at all. Examples: Docker, Carthage.

Go falls in the **ambiguously specified** category. There is no `license` field in `go.mod` or in the module proxy protocol. License information must be inferred from the presence and content of `LICENSE` files in the module source. The `pkg.go.dev` service surfaces heuristically detected license data but this is not exposed through any official API or CLI command.

---

## 2. Go Module License Metadata

### Field availability

Go modules have no dedicated license field. The `go.mod` manifest and the `.mod`, `.info`, and `.zip` files served by the [module proxy protocol](https://go.dev/ref/mod#goproxy-protocol) contain no license attribute. There is no official `go` CLI subcommand that returns license information.

**References**:
- [Go Modules Reference](https://go.dev/ref/mod)
- [pkg.go.dev License Policy](https://pkg.go.dev/license-policy)
- [Go module proxy protocol](https://golang.org/ref/mod#protocol)

### How license information is obtained in practice

License discovery for Go modules relies on file scanning:

1. Download the module source or zip from the proxy (e.g., `https://proxy.golang.org/<module>/@v/<version>.zip`).
2. Identify license files at the module root or common subdirectories (typically named `LICENSE`, `LICENSE.md`, `COPYING`, etc.).
3. Use a scanner such as [`licensecheck`](https://pkg.go.dev/golang.org/x/license), [`go-licenses`](https://github.com/google/go-licenses), or [scancode-toolkit](https://github.com/nexB/scancode-toolkit) to match file contents to known license patterns.
4. Map results to SPDX identifiers where possible.

The [`pkg.go.dev`](https://pkg.go.dev) website uses this approach internally via `licensecheck` and marks modules as redistributable or non-redistributable based on the detected license. This classification is not exposed through a public API.

### Data format

| Attribute | Value |
|-----------|-------|
| Field in manifest | None |
| SPDX expression support | Not supported |
| Escape hatch | Not applicable |
| Distribution | License files included in module zip |
| Tooling | `licensecheck`, `go-licenses`, `scancode-toolkit` |

### Access patterns

| Access method | Available |
|---------------|-----------|
| `go.mod` / manifest field | No |
| `go` CLI command | No |
| Module proxy API | No |
| `pkg.go.dev` website | Yes (heuristic, not machine-readable via API) |
| Module zip (file scan) | Yes |

## 3. Quality Assessment

To measure license metadata coverage, we analyzed package data sourced from [Ecosyste.ms](https://ecosyste.ms/) (CC BY-SA 4.0), which aggregates metadata from public registries including `proxy.golang.org`. Coverage is defined as the percentage of packages for which a valid SPDX license expression can be extracted or mapped from available metadata. Packages with null, empty, or unresolvable values are counted as lacking coverage. Escape hatch values such as `NONE`, `NOASSERTION`, `UNKNOWN`, and `SEE LICENSE IN` are excluded from the coverage percentage, as they indicate an absent or deferred declaration rather than a valid license.

Because Go has no structured license field, coverage figures for the Go ecosystem reflect the success rate of heuristic file scanning against the module zip contents, not the presence of a declared field. This makes Go's coverage inherently dependent on module authors following file naming conventions and including unmodified license texts.

Data was analyzed across four samples to understand how coverage varies with package popularity. The full results, including all ecosystems, are available in the [coverage results document](../../../attribute_analysis/drafts/license_coverage_results.txt).

- **Top 0.1%**: the most downloaded packages (highest visibility, typically well-maintained).
- **Top 1%**: broader popular packages.
- **Top 10%**: a large cross-section including many less-maintained modules.
- **Balanced sample**: 500 randomly selected packages from the top 10% data, equally weighted per ecosystem, to avoid the Go dataset's size distorting cross-ecosystem comparisons.

| Sample | Total packages | Valid SPDX | Coverage |
|--------|---------------|------------|----------|
| Top 0.1% | 40 | 38 | 95.00% |
| Top 1% | 1,916 | 1,817 | 94.83% |
| Top 10% | 1,590,932 | 678,049 | 42.62% |
| Balanced (500) | 500 | 462 | 92.40% |

Coverage is high among popular modules (95% in the top 0.1%), reflecting that well-maintained projects tend to include standard license files. It drops sharply in the broader population (42.62% in the top 10%), driven by the large number of modules with no license file or unrecognized content. Across the 1,733,758 Go modules analyzed, 43.1% lack extractable license information and 13.0% have a null value, meaning over half of all Go modules have no detectable license metadata.

**Reliability**: Weak. Results depend on file naming conventions and license text being unmodified. Variations in naming or content reduce detection accuracy. There is no authoritative structured source to validate against.

---

## 4. Transformation Requirements

Because Go modules provide no structured license field, producing machine-readable SPDX expressions requires a file-scanning pipeline applied to the module source. The steps below describe the process for transforming raw module content into validated SPDX output. This transformation is necessary for any automated license compliance or dependency analysis tooling that needs to operate across Go modules.

1. Retrieve the module source or download the zip from the proxy (e.g., `https://proxy.golang.org/<module>/@v/<version>.zip`).
2. Identify license files at the module root or common subdirectories (typically named `LICENSE`, `LICENSE.md`, `COPYING`, etc.).
3. Apply a license scanner such as [`licensecheck`](https://pkg.go.dev/golang.org/x/license), [`go-licenses`](https://github.com/google/go-licenses), or [scancode-toolkit](https://github.com/nexB/scancode-toolkit) to detect known license texts.
4. Map detected results to SPDX identifiers where possible.
5. Normalize multiple findings into an SPDX expression and validate with an SPDX parser.
