# License Metadata Recommendations — Go Ecosystem

This document provides implementation guidance specific to the Go module ecosystem on how to introduce and improve license metadata support. It is a Go-focused distillation of the broader [License Metadata Recommendations](../../../attribute_analysis/drafts/license_recommendations.md) document, which covers implementation guidance across all studied ecosystems. For background on the current state of license metadata in Go modules, see [go-license-analysis.md](go-license-analysis.md).

Unlike ecosystems that already have a license field in need of improvement, Go modules currently have no structured license field at all. The recommendations below address both the long-term goal of introducing a native field and the interim steps that tooling authors and module publishers can take today.

---

## 1. General Recommendation

Add a dedicated `license` field to `go.mod` whose value is a single **SPDX expression string**.

```
module example.com/mymodule

go 1.22

license MIT OR Apache-2.0
```

SPDX expressions handle all compound-license cases through built-in operators:

| Scenario | Expression |
|---|---|
| Single license | `MIT` |
| Either of two licenses (disjunctive) | `Apache-2.0 OR MIT` |
| Both licenses apply (conjunctive) | `GPL-2.0-only AND MIT` |
| License with exception | `GPL-2.0-only WITH Classpath-exception-2.0` |

Do **not** accept an array of identifiers. Arrays require consumers to guess whether the semantics are AND or OR, and prevent the use of parenthesized sub-expressions or `WITH` clauses.

Until a native `go.mod` field exists, module authors should at minimum include a `LICENSE` file at the module root using a standard, unmodified license text. This is the primary input for all current heuristic detection tools (`licensecheck`, `go-licenses`, `scancode-toolkit`) and for `pkg.go.dev`'s redistributability classification.

**References:**
- [SPDX License List](https://spdx.org/licenses/) — canonical identifiers for all common open-source licenses.
- [SPDX Expression Grammar](https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/) — formal grammar for compound expressions.
- [Go Modules Reference](https://go.dev/ref/mod) — current `go.mod` format.

## 2. Escape Hatch: Custom Licenses

When a module uses a license not on the SPDX list — for example, a bespoke proprietary license — the `license` field should support a `LicenseRef-` reference as defined by the SPDX specification. Three approaches are valid for resolving what that reference points to.

### Option A — Convention-based directory (REUSE approach)

Custom license files are placed in a conventional `LICENSES/` directory. The resolution rule is: look for `LICENSES/<LicenseRef-name>.txt` (or `.md`). This approach is defined by the [REUSE specification](https://reuse.software/spec/).

Expression: `MIT AND LicenseRef-MyLicense`

File location: `LICENSES/LicenseRef-MyLicense.txt`

**Pros:** Short expressions; no explicit mapping; predictable and convention-based.

**Cons:** Requires agreement on and documentation of the directory convention.

### Option B — Path as identifier

The `LicenseRef-` suffix is interpreted as a relative file path from the module root. For example:

- `LicenseRef-LICENSE` references the file at `/LICENSE`
- `LicenseRef-licenses/custom.txt` references the file at `/licenses/custom.txt`

A compound expression: `MIT AND LicenseRef-licenses/custom.txt`

**Pros:** Machine-resolvable without additional metadata; simpler to implement.

**Cons:** Expressions become longer as paths grow; no short alias.

### Option C — Separate mapping field

A separate field (e.g., `license_files` in `go.mod` or a sidecar file) maps each `LicenseRef-` name to its relative path.

Expression: `MIT AND LicenseRef-MyLicense`

Mapping: `LicenseRef-MyLicense → licenses/custom.txt`

**Pros:** Shorter, more readable expressions.

**Cons:** Requires validation that every `LicenseRef-` name has a corresponding mapping entry.

> **Note:** In all three options, the referenced file must be present in the published module zip. Implementations should validate file presence.

### Scope of custom LicenseRefs

`LicenseRef-` should be reserved for:
- Licenses not present on the SPDX license list.
- Proprietary or bespoke licenses.
- Materially modified versions of an OSI license that cannot be expressed with a `WITH` clause.

Discourage use of `LicenseRef-` as a workaround for SPDX-listed licenses whose identifier the author is uncertain of.

## 3. Validation Guidance

Because Go has no centralized registry server that gatekeeps publication, validation cannot be enforced at upload time. It must instead be embedded in the tooling that module authors use day-to-day.

Require that the `license` field value is parseable by a conformant SPDX expression library before a module is published. This validation should be integrated into:
- The `go` CLI (`go mod tidy`, `go publish` or equivalent future commands).
- Module manifest linters (e.g., as a `go vet` check or a standalone linter).
- CI integration tooling used by module authors.

Reference SPDX parser implementations:
- Go: [`github.com/github/go-spdx`](https://pkg.go.dev/github.com/github/go-spdx/v2/spdxexp)
- Python: [`license-expression`](https://pypi.org/project/license-expression/)
- JavaScript: [`spdx-expression-parse`](https://www.npmjs.com/package/spdx-expression-parse)
- Rust: [`spdx`](https://crates.io/crates/spdx)

Warn or reject when the value:
- Is a bare string that is not a valid SPDX identifier or expression (e.g., `"gpl"`, `"BSD"`, `"GPL v2"`).
- Contains multiple identifiers separated by commas, slashes, or spaces without SPDX operators.
- References a `LicenseRef-` name that cannot be resolved via the chosen escape hatch option.
- Uses a deprecated SPDX identifier (e.g., `GPL-2.0` instead of `GPL-2.0-only`). Surface the current equivalent to the publisher.
- Uses a `WITH` clause referencing an identifier not on the [SPDX exception list](https://spdx.org/licenses/exceptions-index.html).

Roll out validation in two phases. First, add warnings in publisher tooling (the `go` CLI, linters, the publish workflow); once adoption is broad, escalate to hard failures on the publisher side. Consumer-side tooling (the dependency resolver, the install command) should never hard-fail on missing or invalid license fields — consumers have no control over the metadata of their dependencies — but should surface warnings so that the issue is visible.

## 4. Transition Guidance

Go modules have no existing license field to migrate away from. The transition is therefore about introducing a new field rather than replacing a legacy one. This changes the shape of the migration: the main dependency is on the Go proposal and toolchain adoption process, not on cleaning up existing data.

The five stages below adapt the general migration framework to Go's situation. Each stage requires a publicly committed date, set by the ecosystem maintainers. The specific dates are the ecosystem's responsibility to determine based on their community size, tooling maturity, and communication capacity — they are not set by these recommendations. The dates X, Y, Z, and W referenced in the stage headings below are placeholders for those committed dates. Expect the full migration from Stage 1 through Stage 5 to span multiple years; rushing the timeline risks breaking publisher workflows and eroding trust in the registry.

---

### Stage 1 — Community proposal and tooling groundwork

Submit a proposal to the Go project to add a `license` field to `go.mod`. In parallel, update third-party tooling (`go-licenses`, `licensecheck`, `scancode-toolkit`) to recognize and validate SPDX expressions from a future `go.mod` field.

Actions:
- File a Go proposal with the format specification, rationale, and SPDX grammar reference.
- Document best practices for module authors in the interim (include a `LICENSE` file at the module root using standard, unmodified license text).
- Once the proposal is accepted, update third-party tooling (`go-licenses`, `licensecheck`, `scancode-toolkit`) to recognize and validate SPDX expressions from the new `go.mod` field.

---

### Stage 2 — Experimental support in toolchain (from date X)

The `go` CLI and related tools accept and parse a `license` field in `go.mod` in an experimental or opt-in capacity. No hard validation; warnings only.

Actions:
- Expose the field in `go mod tidy` output and `go list -m -json`.
- Surface validation warnings (invalid SPDX expression, missing `LicenseRef-` file) in the `go` CLI.
- Update `pkg.go.dev` to display the declared field value alongside heuristically detected license information.

---

### Stage 3 — New modules encouraged to declare (from date Y)

The `license` field is officially supported. Module authors publishing new modules are strongly encouraged to include it. The primary point of influence at this stage is `go mod init`: updating this subcommand to prompt for or require a `license` value ensures that newly created modules start with a valid declaration from the outset. Tooling emits warnings for modules without a `license` field.

Existing modules without the field continue to work without errors.

---

### Stage 4 — Updated modules required to declare (from date Z)

From the announced date, any **update** to an existing module that does not include a valid `license` field triggers a warning in the `go` CLI publish workflow. For modules where the license is detectable from `LICENSE` files, offer automatic generation of the field value as a convenience.

---

### Stage 5 — Field required for all published modules (from date W)

The `license` field is required for all newly published modules. Modules lacking a valid SPDX `license` expression are rejected by the module proxy or flagged as non-redistributable by `pkg.go.dev`.

Communicate clearly that the transition window has closed. Modules without a declared field should be surfaced to consumers as having unvalidated license metadata.

---

## 5. References

- [SPDX License List](https://spdx.org/licenses/)
- [SPDX Expression Grammar (SPDX 2.3)](https://spdx.github.io/spdx-spec/v2.3/SPDX-license-expressions/)
- [REUSE Specification](https://reuse.software/spec/)
- [Go Modules Reference](https://go.dev/ref/mod)
- [pkg.go.dev License Policy](https://pkg.go.dev/license-policy)
- [go-licenses](https://github.com/google/go-licenses)
- [licensecheck](https://pkg.go.dev/golang.org/x/license)
- [License Metadata Recommendations](../../../attribute_analysis/drafts/license_recommendations.md) — general recommendations across all ecosystems
- [go-license-analysis.md](go-license-analysis.md) — current-state analysis for Go modules
