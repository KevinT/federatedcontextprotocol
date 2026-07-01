---
id: 0001
title: Establish FCP v0.1
status: accepted
date: 2026-06-30
editor: kevint@gmail.com
---

# 0001 — Establish FCP v0.1

## Context

Personal and team context for a single person is fragmented across many systems and several long-running relationships (employer, mentor, family, volunteering, friends). The person wants an agent to reason over as much of that context as possible, while ensuring each audience sees only what is intended. Existing structures (a single personal folder inside an employer's repository) hard-code one orientation and physically co-locate content with mismatched audiences.

Several patterns were worked out in design and are now stable enough to fix as a versioned protocol: hub-and-spoke repos with one-way dependency, orientation by mount, projection (not reference) across boundaries, event-sourced context streams with folded views, and a default-deny commit policy separating data from map movements.

## Decision

Adopt the structure, orientation, boundary-crossing, stream, view, and commit rules as specified in SPEC.md v0.1. Govern future changes via semantic versioning and decision records in this folder. The protocol lives in its own public repository, upstream of all adopters; any adopter's implementation is recognised as a reference implementation, not the protocol's home.

## Consequences

- The protocol cannot live inside any adopter, since the one-way rule it defines forbids the upstream spec from depending on a downstream adopter.
- Adopters declare a target version and can be checked against CONFORMANCE.md.
- Breaking changes to §3 (structure) or §6.1 (envelope) require a major version bump.

## Alternatives considered

- **Keep the patterns inside a single adopter's repository.** Rejected: couples a general protocol to one organisation's access model and lifecycle, excludes other adopters (family, friends), and inverts the dependency direction.
- **A personal notes document.** Rejected: not adoptable or versionable by others.
