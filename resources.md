# Resources

This file contains references and external resources that inform our analyses.

## Related Standards
- [SPDX Specification](https://spdx.dev/specifications/)  
- [CycloneDX Specification](https://cyclonedx.org/specification/overview)
- [Package URL (purl) specification](https://github.com/package-url/purl-spec)

## Package Metadata analyses and tools
- [CodeMeta crosswalks (specs for ~42 package managers)](https://github.com/codemeta/codemeta/tree/master/crosswalks/)
- [ClearlyDefined](https://clearlydefined.io/)
- [ecosyste.ms](http://ecosyste.ms/)  
- [libraries.io](http://libraries.io/)
- [CPAN Security Group: Roles and metadata in Open Source supply-chains](https://security.metacpan.org/docs/supplychain-sbom.html) 

## Security and Integrity Frameworks
- [The Update Framework (TUF)](https://theupdateframework.io/)

## Software Preservation
- [Software Heritage Project](https://www.softwareheritage.org/)

## Binary Dependencies

### General
- [_The C-Shaped Hole in Package Management_][c-shaped] by Andrew Nesbitt, a great post about the problem of binary
  dependencies.
- [_Dependency Resolution in Python: Beware The Phantom Dependency_][phantom] by Anand Sawant is where the term _phantom
  dependency_ was originally coined.
- [Issue #1261][ecosystems-packages-1261] on the [ecosyste.ms](https://ecosyste.ms) _packages_ repo collects more
  information on strategies for tracking binary dependencies across multiple package managers.
- [_ESSTRA_][esstra] is a tool developed at Sony that aims to improve supply chain transparency by embedding metadata
  into binaries.
- [UAPI specification 8][uapi-8] provides a section within ELF binaries for recording the provenance of a dynamic
  library, including the name of the system package it originated from. See also Fedora's page about [_Package
  information on ELF objects_][fedora-package-info].
- [UAPI specification 12][uapi-12] provides a section within ELF binaries for recording the names of libraries loaded
  with `dlopen()`. This would hypothetically allow us to keep track of libraries opened with
  [_libffi_][libffi]/[_cffi_][cffi]. However, I'm not sure how these records would be filled in, since it's possible for
  the names of libraries opened with `dlopen()` to not be known until runtime.
- The [_PURL registry_][purl-registry] is a registry of packages, mainly C/C++ packages, that do not otherwise have a
  [PURL][purl] because they are not clearly identified in package registries. Such a registry could be used for
  assigning reliable identities to binary dependencies.

### Python
- [_auditwheel_][auditwheel], a widely-used Python package that can identify a wheel's required dynamic libraries, but
  does not yet have accurate human-readable output, or an API for researchers and developers to use.
- [_elfdeps_][elfdeps], a lesser-known Python package that can identify a wheel's required dynamic libraries and _does
  have_ a public API.
- [PEP 770][pep-770], in which author Seth Larson [introduces][seth-pep-770] SBOMs to Python packages. See also his [PR
  #577][auditwheel-577] to [_auditwheel_][auditwheel], which enables users to discover binary dependencies, and include
  them in a package's SBOM.
- [PEP 725][pep-725], which specifies a way to record binary dependencies in `pyproject.toml`. This interoperable record
  of binary dependencies could allow many tools to, for example, flag security issues that were previously invisible.
- [PEP 804][pep-804], which specifies a system for mapping binary dependency names to packages in non-Python registries.
- [_Fromager_][fromager] is a tool that aims, among other things, to provide a way for Python packages to be built
  completely from source, which includes building all their binary dependencies from source. I am not sure whether this
  is actually implemented yet.
- In a paper titled [_Insight: Exploring Cross-Ecosystem Vulnerability Impacts_][insight], Xu et al describe a system
  for identifying when Python code calls into parts of C-based dynamic libraries that are known to have security
  vulnerabilities. According to their research, 24.0% of PyPI projects “transitively invoke vulnerable APIs from C
  libraries”. Note, however, that Xu et al analyse Python code that calls into binary dependencies _using `dlopen()`_,
  which is a notable caveat, since these kinds of FFI calls are not the most common way to call into binary
  dependencies. See my [post on how binary dependencies work][how-bindeps-work] for more information.

## Node.js
- [_How to publish binaries on npm_][npm-bin-pub] by Luca Forstner tells us that it's possible, but tricky, to publish
  binary packages on _npm_.

## Related communities
- [OpenChain](https://www.openchainproject.org/)  
- [OpenSSF (Open Source Security Foundation)](https://openssf.org/)  
- [TODO Group](https://todogroup.org/)

[auditwheel-577]: https://github.com/pypa/auditwheel/pull/577
[auditwheel]: https://github.com/pypa/auditwheel
[c-shaped]: https://nesbitt.io/2026/01/27/the-c-shaped-hole-in-package-management.html
[cffi]: https://cffi.readthedocs.io/en/stable/
[ecosystems-packages-1261]: https://github.com/ecosyste-ms/packages/issues/1261
[elfdeps]: https://github.com/python-wheel-build/elfdeps/
[esstra]: https://github.com/sony/esstra
[fedora-package-info]: https://fedoraproject.org/wiki/Changes/Package_information_on_ELF_objects
[fromager]: https://github.com/python-wheel-build/fromager
[how-bindeps-work]: https://vlad.website/how-binary-dependencies-work/
[insight]: https://dl.acm.org/doi/pdf/10.1145/3551349.3556921
[libffi]: https://github.com/libffi/libffi
[npm-bin-pub]: https://sentry.engineering/blog/publishing-binaries-on-npm
[pep-725]: https://peps.python.org/pep-0725/
[pep-770]: https://peps.python.org/pep-0770/
[pep-804]: https://peps.python.org/pep-0804/
[phantom]: https://www.endorlabs.com/learn/dependency-resolution-in-python-beware-the-phantom-dependency
[purl-registry]: https://github.com/package-url/purl-registry
[purl]: https://github.com/package-url/purl-spec
[seth-pep-770]: https://sethmlarson.dev/pep-770-sbom-data-from-pypi-fedora-and-redhat
[uapi-12]: https://uapi-group.org/specifications/specs/elf_dlopen_metadata/
[uapi-8]: https://uapi-group.org/specifications/specs/package_metadata_for_executable_files/