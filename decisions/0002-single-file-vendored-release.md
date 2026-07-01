---
id: 0002
title: Distribute FCP as a single hashable file, vendored and pinned by adopters
status: accepted
date: 2026-06-30
editor: kevint@gmail.com
---

# 0002 - Distribute FCP as a single hashable file, vendored and pinned by adopters

## Context

Adopters (a personal root, a domain repo, an organisation's context repository) need to know the rules of the FCP version they target, at read time, often inside isolated or offline mounts. Two questions: what artefact do we ship, and do adopters reference it or copy it in?

## Decision

1. **Compile each released version to a single file** `fcp-<MAJOR.MINOR.PATCH>.md` containing the full normative spec with the event schema embedded as a normative appendix. The single file is the unit of integrity: one SHA-256 over it pins exactly the rules in force. Releases are immutable.
2. **Adopters declare and vendor a pinned copy.** The binding fact is a version declaration (`fcp: "0.1.0"`). Adopters SHOULD also vendor the compiled file into `.fcp/` with a `lock.json` recording version, source, `sha256`, and `adopted_at`. The vendored file is a hash-validated cache, not a second source of truth.
3. **Pin, never track latest.** Upgrading is a deliberate re-vendor + reconcile. Tooling may surface that a newer version exists but must not auto-upgrade.

## Consequences

- The rules travel with the repo (offline, isolated mounts) - consistent with the protocol's own "crossing only by copy" - and conformance becomes reproducible and auditable.
- A SHA-256 mismatch is a tamper/drift signal that must be surfaced (the "divergence surfaced" principle applied to the protocol itself).
- The protocol distributes itself the way it asks capabilities to be promoted: published upstream, pulled and adopted downstream when ready.
- Vendoring an immutable, pinned version does not violate "point at systems of record, don't copy" - that rule governs *mutable* data; a frozen release cannot drift.

## Alternatives considered

- **Reference-only (link to canonical URL).** Rejected: fragile for offline/isolated agents, breaks downstream independence if upstream changes/disappears, and is not reproducible.
- **Multi-file release bundle.** Rejected for the integrity anchor: a single file gives one clean hash. Templates and tooling remain in source and are not part of the vendored artefact.
