# FCP Conformance

Conformance is defined by the **principles** in SPEC §3 — the properties, not the mechanisms. A federation conforms if it upholds them by any means. Implementing the canonical conventions (SPEC §4) is a separate claim: it is what lets two federations **interoperate**.

## 1. Conformant — uphold every principle (any mechanism)

Test whether each is *true*, not whether you used a particular tool.

- [ ] **Audience isolation** — every unit has a declared audience, enforced by access control; no unit is readable outside it.
- [ ] **Maximal owner reasoning** — the owner can reason across the union of all their context in one activity, without de-isolating it.
- [ ] **Locality of truth** — contexts may disagree; nothing forces global consistency; cross-context reasoning stays frame-aware.
- [ ] **One-way dependency** — upstream never depends on downstream; any downstream unit can be removed without breaking upstream; exactly one root.
- [ ] **Crossing only by gated projection** — context crosses audiences only as an owner-authored, gated artefact; no automatic propagation.
- [ ] **Single-writer authority** — every unit has exactly one authoritative writer.
- [ ] **Faithful, non-authoritative views** — every view is derivable from tracked sources, regenerable, marked derived, and not a source of truth.
- [ ] **Provenance & curation state preserved** — every assertion carries origin and curation state, and these survive projection.
- [ ] **Divergence surfaced** — conflicts and drift are detectable and surfaced to owners; nothing is auto-reconciled across an ownership boundary.
- [ ] **Capabilities & models first-class and promotable** — models/skills are owned, scoped, and promoted only by gated publish-and-adopt.
- [ ] **Safe-by-default disclosure** — new content defaults to unshared; widening audience is an explicit act.
- [ ] **Stable identity** — unit identity is stable across vantage points; orientation needs no rename/copy/restructure.
- [ ] **Declared version** — the federation declares its target FCP version.

## 2. Canonical profile — the conventions (for interoperability)

Check these only when interoperating with other federations or using the reference tooling (SPEC §4): repos as units; root/spine/constituent topology; `.`/`_`/unprefixed layering and naming; `purpose.md`/`README.md`/`properties.json`/`context-map.json` split; mount orientation on one flat layout; the seam rule; namespaced projection files; event streams (`events.jsonl` + folded `state.md`); the `stewarded/proxy/inferred/unowned` curation marker; `.mental-models/`/`.skills/` with gated promotion; divergence/reconciliation events; default-deny commit policy; lateral federation; access modes and intents.

## 3. Interoperability levels

- **Read-only exchange** — consume another federation's published views. Needs namespaced projections (and event streams if views are folded).
- **Stream exchange** — exchange `events.jsonl` for local folding. Needs event streams + schema agreement.
- **Shared-space collaboration** — co-own a shared unit (mentoring, family, a friend circle). Needs repos-as-units, the seam rule, namespaced projections, and lateral federation.

A federation that is conformant but not canonical is safe and well-formed, but cannot be assumed to interoperate without adopting the relevant conventions.
