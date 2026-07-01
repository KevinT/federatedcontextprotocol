# Changelog

All notable changes to the Federated Context Protocol are recorded here. The spec follows [Semantic Versioning](https://semver.org): MAJOR for breaking changes to Part A requirements or any interoperability format, MINOR for backward-compatible additions, PATCH for clarifications.

## [0.1] - 2026-06-30
### Added
- Initial draft: model (root/spine/constituent, one-way dependency, seam), orientation-by-mount, projection-not-reference boundary crossing, event streams (`events.jsonl` + folded `state.md`), event envelope + JSON Schema, default-deny commit policy.
- ADR 0001 establishing v0.1 and the protocol's home as a standalone public repo.
- Distribution model (§8): each version compiles to a single hashable file (`dist/fcp-<version>.md`, schema embedded) with a SHA-256 sidecar; `tools/build-release.py` builds and verifies it; adopters declare + vendor a pinned copy in `.fcp/` with a `lock.json` (`templates/fcp-lock.json`). ADR 0002 records the decision.

### Changed
- Consolidated into a single readable spec: **§3 Principles** (named, normative, tool-agnostic - these define conformance) and **§4 Canonical implementation** (recommended, substitutable conventions grounded in a reference implementation). Dropped the R/C code cross-referencing in favour of named principles.
- Elevated §1 Purpose to the real problem: building digital intelligence across overlapping, subjective, possibly-disagreeing contexts - with an explicit "what FCP does not do" (it is a substrate, not a solver).
- Added principles for **locality of truth**, **provenance & curation state**, **divergence surfaced not silently resolved**, and **capabilities & models first-class and promotable**; and conventions for the `stewarded/proxy/inferred/unowned` curation marker, `.mental-models/`/`.skills/` promotion, divergence/reconciliation events, the `purpose.md`/`README.md`/`properties.json`/`context-map.json` split, validity periods, systems-of-record, access modes & intents, single flat layout & mount orientation, the seam rule, namespaced projections, and lateral peer federation.
- Realigned `CONFORMANCE.md` to test §3 principles, with §4 as the canonical interoperability profile.
