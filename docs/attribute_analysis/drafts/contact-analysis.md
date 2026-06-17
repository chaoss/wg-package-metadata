# Contact Metadata Analysis

This document analyzes how different package managers handle contact metadata across ecosystems.

## 1. Key findings summary

_TBD after sections 2–7 are finalized._

## 2. Data Collection Overview

This section provides an overview of the ecosystems and package managers reviewed to determine whether they make contact information of package maintainers available as part of their metadata. For each package manager, we indicate the level of support for contact data and point to the relevant specification or documentation. This establishes the foundation for deeper analysis in subsequent sections.

### Rust Ecosystem — Cargo

**Contact Information Available**: Partially. Cargo historically supported an `authors` field in `Cargo.toml`, where package authors could be listed as strings and could include email addresses, for example `Name <email@example.org>`. However, this field is deprecated and should not be treated as reliable current-maintainer contact metadata. The crates.io API endpoint for retrieving `authors` metadata for a specific crate version is also deprecated and now returns an empty list for backwards compatibility.

crates.io also provides registry-level identity metadata that is separate from the package manifest. Crate metadata includes links to owner endpoints such as `/owners`, `/owner_user`, and `/owner_team`, which expose the crates.io users or GitHub teams that currently control a crate. Version metadata may also include `published_by` and `audit_actions.user`, identifying the user account that published a specific version or performed a registry action. These user objects typically include a crates.io user ID, login, display name, avatar, and profile URL, commonly pointing to the associated GitHub account.

This means crates.io provides useful maintainer identity metadata, but not direct contact metadata in the form of email addresses. Contact may sometimes be inferred by following the associated GitHub profile, if the user has chosen to expose contact information there, but this is external to Cargo/crates.io metadata. Consequently, there is no guaranteed relationship between deprecated `authors` values in `Cargo.toml`, the user who published a particular version, and the current crate owners who control future releases.

**API access**: `GET https://crates.io/api/v1/crates/<crate>` exposes version-level fields such as `versions[].published_by` and `versions[].audit_actions[].user`; owner metadata can be retrieved through the linked endpoints, for example `GET https://crates.io/api/v1/crates/<crate>/owners`, `GET https://crates.io/api/v1/crates/<crate>/owner_user`, and `GET https://crates.io/api/v1/crates/<crate>/owner_team`.


**References**:
- [Cargo Reference — Manifest Format: authors field](https://doc.rust-lang.org/cargo/reference/manifest.html#the-authors-field)
- [Cargo Book — Registry Web API](https://doc.rust-lang.org/cargo/reference/registry-web-api.html)
- [Cargo Book — Publishing on crates.io: cargo owner](https://doc.rust-lang.org/cargo/reference/publishing.html#cargo-owner)

### Python Ecosystem — PyPI (pip)

**Contact Information Available**: Yes, via the package metadata fields `author_email` and `maintainer_email` (Core Metadata). These fields may contain email addresses alone or a combination of names and email addresses, and are exposed through the PyPI web interface and JSON API.

PyPI also maintains a separate ownership model based on user accounts and roles (Owner, Maintainer). However, contact information for those assigned user accounts is not exposed through package metadata or the public PyPI API. Consequently, there is no guaranteed relationship between the email addresses declared in package metadata and the actual PyPI users who currently control the package.

**API access**: `GET https://pypi.org/pypi/<project>/json` exposes the relevant metadata under `info.author_email` and `info.maintainer_email`. It does not expose public email contact information for the PyPI user accounts that own or maintain the project.

**References**:
- [Python Packaging User Guide — Core Metadata Specifications](https://packaging.python.org/en/latest/specifications/core-metadata/)
- PEP 621 ([Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/))
- [Project roles](https://docs.pypi.org/organization-accounts/roles-entities/#project-roles)
- [PyPI JSON API](https://docs.pypi.org/api/json/)