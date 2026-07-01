<!-- FCP compiled release — DO NOT EDIT. Built from source.
     version: 0.1.0
     source:  https://github.com/<owner>/federated-context-protocol
     built:   2026-07-01T08:24:29Z
     integrity: SHA-256 of this file is recorded in the .sha256 sidecar. -->

# Federated Context Protocol (FCP) — Specification

**Version:** 0.1 (draft) · **Editor:** Kevin Trethewey · **Status:** working draft for review

The key words MUST, MUST NOT, SHOULD, SHOULD NOT, MAY are used as in RFC 2119.

This document has two layers. The **Principles** (§3) are what the protocol guarantees; conformance is defined by them alone, and they are written without reference to any tool or file format. The **Canonical implementation** (§4) is the recommended way to satisfy the principles — the one used by the reference implementation and the bundled tooling. You can conform to FCP with different mechanisms; you adopt §4 in order to *interoperate* with others.

---

## 1. Purpose — the problem FCP exists to solve

A person lives inside many contexts at once — employee, mentee, parent, friend, volunteer — and so do teams and organisations. These contexts **overlap, disagree, and are not always aligned with the world or with each other.** Context is subjective and local: a thing can be true in one context and false, unknown, or differently-shaped in another. There is no global truth to appeal to.

FCP is the substrate for building **digital intelligence across that reality**. It lets a person (or an agent acting for them) reason over the widest possible span of their context while sharing each part only with the audience it belongs to. Concretely, it is designed to make four hard things tractable:

1. **Codifying mental models at the right level** — capturing *how to think* about a domain where it is true, and no wider.
2. **Building repeatable, shareable capabilities** — skills and artefacts that can be promoted from one context to many.
3. **Keeping the map alive** — detecting where contexts have drifted out of agreement (with each other or with reality) and surfacing it for resolution, without forcing false consensus.
4. **Retaining the signal of how the map came to be** — every part of the map carries who asserted it and how it is maintained (actively stewarded, by proxy, inferred, or unowned).

**What FCP does not do.** FCP provides the substrate; it does not author good mental models for you, and it does not resolve genuine disagreements. It makes provenance visible, keeps contexts isolated yet jointly reasonable-over, detects divergence, and moves capabilities around safely. The judgement stays human.

---

## 2. Vocabulary

- **Context unit** — an addressable body of context with exactly one owner and one declared audience. (In the canonical implementation, a git repository — but the principles do not assume that.)
- **Federation** — all the context units belonging to one person, plus the shared units they take part in.
- **Owner** — the single party with authority to write a unit.
- **Audience** — the set of parties permitted to read a unit.
- **Root** — the private context unit at the apex of a federation. The only vantage point able to read across everything the person owns. Holds their deepest goals and the integrative view.
- **Spine** — the root plus the **domains** a person orients by (e.g. Work, Mentorship, Family).
- **Domain** — a long-running context on the spine.
- **Constituent** — a unit that composes a domain: the owner's individual slice, a team, a shared project, or a foreign unit.
- **Seam** — a unit that legitimately belongs to two frames at once (e.g. a personal work slice that is both the owner's individual context and a downstream child of an employer's unit).
- **Projection / view** — a derived, read-oriented artefact folded from one or more sources. Never a source of truth.
- **Curation state** — the signal of how a piece of the map is maintained: *stewarded*, *proxy*, *inferred*, or *unowned* (see §4.8).
- **System of record** — the authoritative external source for some mutable data (an HR system, a calendar). The map points at it; it does not copy it.

---

## 3. Principles (normative — these define conformance)

A federation conforms to FCP if it upholds all of the following, by any means.

**3.1 Audience isolation.** Every context unit has a declared audience, and its content is not readable outside that audience. Isolation is enforced by an access-control mechanism — not by naming, obscurity, or trusting readers to look away.

**3.2 Maximal owner reasoning.** The owner (or their agent) can reason over the union of everything they own or are entitled to, in a single activity, without first de-isolating it. Sharing is narrow; reasoning is wide. These two principles are the poles the whole protocol balances.

**3.3 Locality of truth.** Context is local and subjective. A unit's assertions are true *within* that unit, not globally. FCP does not require contexts to agree, and reasoning across them must stay frame-aware — it composes local truths, it does not flatten them into one merged truth.

**3.4 One-way dependency.** Units form an order from upstream (more foundational, more private) to downstream (more specific, more contextual). Nothing upstream may depend on, reference, or require anything downstream, and any downstream unit may be removed without breaking what is above it. Each federation has exactly one maximal upstream unit: its root.

**3.5 Crossing only by gated projection.** Context crosses from one audience to another only as an artefact the source owner deliberately authored or approved, gated to the destination audience. There is no automatic or transitive propagation: a fact held by one unit does not reach another audience until its owner publishes it there. (Because the reader on the far side of an isolation boundary cannot resolve a pointer, the crossing artefact must be a self-contained copy — and writing it is itself the act of disclosure.)

**3.6 Single-writer authority.** Every unit has exactly one authoritative writer: its owner. Where several parties share a space, each writes only the unit they own within it; none writes another's.

**3.7 Faithful, non-authoritative views.** A view contains only facts present in a tracked source, is regenerable from those sources, is marked as derived, and is never treated as the source of truth.

**3.8 Provenance and curation state are preserved.** Every assertion carries machine-readable provenance (who or what asserted it) and a curation state (how it is maintained). These signals survive projection and folding — a view may summarise the map but may not strip how each part came to be.

**3.9 Divergence is surfaced, never silently resolved.** When two contexts conflict, or a context drifts from a system of record or from the world, the divergence must be detectable and surfaced to the responsible owner(s). FCP must not auto-reconcile across an ownership or audience boundary; resolution is an owner's act, recorded as a new assertion rather than a silent overwrite.

**3.10 Capabilities and models are first-class and promotable.** Mental models and reusable capabilities (skills, artefacts) are context units like any other — owned, audience-scoped, provenance-tagged. A model or capability lives at the most upstream level at which it holds, and may be promoted to a wider scope only by the same gated-publish-and-adopt path as any other context, never by silent copy.

**3.11 Safe-by-default disclosure.** New content defaults to unshared. Widening an audience is an explicit, distinguishable act, because disclosure to a shared medium is generally irreversible.

**3.12 Stable identity across orientation.** A unit's identity is stable regardless of how, where, or alongside what it is accessed, and regardless of which unit is the focal point of a given activity. Changing vantage point requires no rename, copy, or restructure.

**3.13 Declared version and governed change.** A federation declares the FCP version it targets. The specification is versioned with semantic versioning; changes to these principles or to any interoperability format are breaking and increment the major version.

---

## 4. Canonical implementation (recommended conventions)

This is the concrete realisation the reference implementation uses. Each subsection notes the principle it serves and is substitutable. Adopting these is what lets two federations interoperate.

### 4.1 Units are repositories; the repo boundary is the audience boundary Use version-controlled repositories as context units, with the host's per-repository permissions as the isolation mechanism (*audience isolation*, *safe default*). A new audience means a new repository — never a subfolder, since access control is per-repo and a folder cannot be hidden from a collaborator. Do not use sparse-checkout or path filters for isolation; they control transfer, not authorisation.

### 4.2 Topology: root, spine, constituents A federation is a hub-and-spoke of repos (*maximal reasoning*, *one-way dependency*):

- the **root** is private, rarely mounted, and upstream of everything;
- **domains** sit on the spine (Work, Mentorship, Family, …);
- **constituents** compose each domain (the owner's slice, teams, shared projects, foreign units).

Dependency runs root → domain → constituent and never upward.

### 4.3 Layering and naming inside a unit Following the reference implementation, each unit separates three kinds of folder by prefix:

- **`.`-prefixed** — system/meta infrastructure that defines and governs the unit: `.meta/` (what this node *is*), `.mental-models/` (how to think here), `.skills/` (capabilities), decision records under `.meta/decision-records/`. These inherit downward to child folders unless overridden.
- **`_`-prefixed** — downstream contexts that consume the unit but are not part of it (e.g. `_personal`, `_team-*`). The unit must stay coherent with any `_` folder removed.
- **unprefixed** — the unit's own content.

Across a federation the same prefixing places units in the dependency order (*one-way dependency*, *stable identity*): the apex of each frame is unprefixed; owned downstream units are `_`-prefixed; foreign units keep their given names. Names follow the canonical, root-centred frame and are never changed to reflect a temporary vantage point.

Within a node, identity is split across small files so each stays trustworthy:

- **`.meta/purpose.md`** — the systemic question: what this node is and why it exists. Terse, slow-changing, owned by the node's steward.
- **`README.md`** — the operational question: what's inside and how to use it. Fast-changing.
- **`properties.json`** — intrinsic, slowly-changing facts (the structured complement to `purpose.md`). Keep minimal; do not restate the folder name.
- **`context-map.json`** — pointers to where related work and data live in external systems, each with provenance and a `valid_from`/`valid_to` validity period. No temporal or mutable state lives here; that belongs in the system of record the pointer names.

### 4.4 Orientation by mount, on one flat layout Keep one flat set of sibling clones per machine; do not maintain parallel trees for different modes. Choose your vantage point by **what you open** (*audience isolation*, *maximal reasoning*, *stable identity*): mounting a domain alone yields a bounded session that cannot reach sibling domains or the root — the mount scope enforces isolation directly; mounting the root (or a parent holding the federation) yields an integrator session that may read down into everything.

### 4.5 The seam A unit that belongs to two frames stays **where its tooling resolves it** — typically nested inside the foreign unit and gitignored by it — while remaining its own independently-owned repo. Do not relocate a seam at the moment of sharing: converting a folder into a shared repo at the disclosure boundary risks leaking private history (*safe default*). Create the boundary as its own repo before sharing is needed. Example: a personal work slice lives inside the employer's repo (gitignored), so it is never trapped in the employer's history; on leaving, it survives as a frozen archive.

### 4.6 Crossing boundaries: namespaced projection files Realise *gated projection* with written, gated artefacts. An upstream unit publishes a gated slice **down** into a downstream unit it owns. In a shared unit, each participant publishes a gated slice **in**, to a file **namespaced by the publisher** (e.g. `…/from-<publisher-id>.md`) — one file per publisher, so no shared file ever has two writers (*single-writer*), each stamped as derived (*faithful views*). Gating is decided by the publisher's root and applied per destination: the same source publishes different slices to different audiences.

### 4.7 Context as event streams (optional substrate) Represent each source as an append-only log paired with a folded view:

```
event-stream/<source-id>/
  events.jsonl   # append-only; one JSON object per line; never rewritten (single writer)
  state.md       # folded view; derived, stamped "do not edit", machine frontmatter + prose body
```

`<source-id>` is globally unique (an email, a stable system name). Events use the envelope in `schema/event.schema.json` (`ts`, `id`, `source`, `type`, `payload`, `v`, optional `audience`). Views are produced by folding the log; gating is applied during the fold via `audience`. Compact long logs by snapshotting. **This is optional** — a federation may satisfy *faithful views* with static, hand-maintained views and never adopt event sourcing.

### 4.8 Provenance and curation state Every node records how it is maintained (*provenance preserved*), using a four-value marker:

- **stewarded** — an accountable individual actively curates it;
- **proxy** — maintained on the owner's behalf by another party or an agent, with the owner's sanction;
- **inferred** — asserted by an agent and not yet verified by a human; treat as a hypothesis;
- **unowned** — no accountable owner; treat as low-trust and a candidate for stewardship.

Origin provenance comes for free from event `source`/`ts`; curation state is a property of the maintained node and is carried in its `properties.json` (or equivalent). Ownership of a node's narrative (`purpose.md`, objectives) belongs to its steward; anyone else proposes changes through the steward rather than writing directly.

### 4.9 Capabilities and mental models as carried, promotable artefacts Mental models live in `.mental-models/` and capabilities in `.skills/`, each at the most upstream unit where it holds, with its own provenance (*capabilities first-class*). Promotion is a gated-publish-and-adopt: propose the model/skill, publish it into the wider (upstream or shared) unit, and let adopters pull — never a silent copy. A capability proven in one domain is promoted upward only as it generalises.

### 4.10 Consistency: divergence detection and reconciliation events Run periodic checks that compare a context against its peers and against the systems of record it points to (e.g. resolving a person against the canonical roster rather than inferring from a handle). Emit a `divergence.detected` event and surface it to the responsible owner(s) (*divergence surfaced*). Any resolution is recorded as a **new** event, not an overwrite, so the history of how agreement was reached is preserved.

### 4.11 Commit policy: default-deny, data vs. map movements Distinguish **data** (local, often re-derivable, possibly sensitive) from **map movements** (durable, shareable changes). The split falls on file boundaries. Use a default-deny `.gitignore` (`*` then explicit `!` promotions) so a unit is local until deliberately promoted (*safe default*). Guideline: **commit what is otherwise homeless; keep local what has a system of record.** In a shared repo, keep raw `events.jsonl` local and commit only the gated `state.md`; in a private repo the owner may commit both.

### 4.12 Lateral federation between peers Two or more people, each running a sovereign root, share by means of a **shared unit cloned into each of their federations** at whatever slot fits each owner (same remote, different mount paths — identity is stable). No participant's root is upstream of another's; the only link between their worlds is the shared unit, into which each publishes a namespaced projection. This extends the root→domain model to a peer mesh while preserving every root's sovereignty and every audience's isolation.

### 4.13 Access modes and proposing changes you don't own A unit may be opened in **full** mode (the owner/steward may write directly) or **readonly** mode (a consumer who may not). In readonly mode, a change to a unit the user does not own is captured as an **intent** — a plain-English statement of the desired end-state — and routed to the steward, who materialises it. Writes confined to the user's own personal/downstream context are always permitted. This is how *single-writer authority* and *steward ownership* are upheld without blocking contribution.

---

## 5. Conformance and interoperability

- **Conformant** — upholds every principle in §3, by any mechanism. This is the safety guarantee.
- **Canonical profile** — additionally implements §4. This is the interoperability guarantee.

When two federations exchange context they must share the relevant conventions: consuming another's published views needs §4.6 (and §4.7 if views are folded); exchanging raw streams needs §4.7 plus schema agreement; co-owning a shared space (mentoring, family, a friend circle) needs §4.1, §4.5, §4.6, and §4.12. A federation that is conformant but not canonical is safe and well-formed but cannot be assumed to interoperate without adopting the relevant conventions. `CONFORMANCE.md` is the checklist.

## 6. Security and privacy considerations

Isolation is only as strong as the underlying access-control configuration; FCP delegates enforcement to it. The highest-risk operation is promotion into a shared unit; the default-deny posture exists to make it deliberate. Relocating a seam at the sharing boundary is the classic way private history leaks — create the boundary before it is needed.

## 7. Governance and relationship to implementations

Changes are recorded as decision records under `decisions/` and versioned semantically. The tooling in `tools/` and templates in `templates/` implement §4 and are not part of the normative specification. The protocol is upstream of every adopter, including its reference implementation, and therefore lives in its own repository — it cannot live inside an adopter without violating its own one-way dependency principle.

## 8. Distribution

This repository is the **source**. Each released version is **compiled to a single file**, `fcp-<MAJOR.MINOR.PATCH>.md`, containing the full normative specification with the event schema embedded as a normative appendix. The single file is the **unit of integrity**: a SHA-256 over it pins exactly the rules in force, so an adopter (or a reviewer, or an automated check) can verify that the rules they are operating under are authentic and unaltered. Releases are immutable — a published version is never edited; corrections ship as a new version.

An adopter:

- **MUST declare** the version it targets (the *declared version* principle), e.g. `fcp: "0.1.0"` in its root manifest;
- **SHOULD vendor** the pinned compiled file into a `.fcp/` folder, alongside a lock recording `version`, canonical `source`, `sha256`, and `adopted_at`. Vendoring keeps the rules available offline and inside isolated mounts — consistent with the protocol's own "crossing only by copy" — and makes conformance reproducible and auditable;
- **MUST pin** a specific version and **MUST NOT** track an unpinned "latest".

**Integrity.** The vendored file is a hash-validated cache, not a second source of truth. An adopter verifies it against the recorded SHA-256; a mismatch means tampering or drift and MUST be surfaced, never silently accepted.

**Upgrade.** Adopting a newer version is a deliberate act: re-vendor the new file, update the lock, and reconcile any breaking changes. Tooling MAY surface that a newer version exists (this is the *divergence surfaced* principle applied to the protocol itself) but MUST NOT auto-upgrade. In this way the protocol distributes itself exactly as it asks capabilities to be promoted: published upstream, pulled and adopted downstream when the adopter is ready.


---

## Appendix A — Event envelope schema (normative)

The canonical JSON Schema for `events.jsonl` lines (SPEC §4.7). This is embedded here so the
release file is self-contained and the hash covers the schema too.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://federated-context-protocol.org/schema/event.schema.json",
  "title": "FCP Event Envelope",
  "description": "One line of an events.jsonl stream. See SPEC.md §6.1.",
  "type": "object",
  "required": ["ts", "id", "source", "type", "payload", "v"],
  "additionalProperties": false,
  "properties": {
    "ts": {
      "type": "string",
      "format": "date-time",
      "description": "ISO-8601 UTC timestamp of when the event occurred."
    },
    "id": {
      "type": "string",
      "minLength": 1,
      "description": "Globally unique event ID, e.g. a ULID."
    },
    "source": {
      "type": "string",
      "minLength": 1,
      "description": "The <source-id> that emitted this event (email, DID, or stable system name)."
    },
    "type": {
      "type": "string",
      "pattern": "^[a-z0-9]+(\\.[a-z0-9]+)+$",
      "description": "Dotted event type, e.g. goal.set, role.changed, link.shared, lifeevent.recorded."
    },
    "audience": {
      "description": "Optional gating hint: which destination(s) this event may be folded into. A string, list of strings, or 'self' for owner-only.",
      "oneOf": [
        { "type": "string" },
        { "type": "array", "items": { "type": "string" }, "minItems": 1 }
      ]
    },
    "payload": {
      "type": "object",
      "description": "Type-specific body. Shape is defined per event type by the implementation."
    },
    "prov": {
      "type": "object",
      "description": "Optional provenance (e.g. tool, commit, upstream source).",
      "additionalProperties": true
    },
    "v": {
      "type": "integer",
      "minimum": 1,
      "description": "Envelope schema version."
    }
  }
}
```
