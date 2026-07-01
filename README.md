# Federated Context Protocol (FCP)

> A protocol for federated context management - letting a person (or an AI agent acting for
> them) reason across **all** of their context while sharing **only** what each audience should see.

**Status:** v0.1 (draft) · **License:** see [LICENSE.md](LICENSE.md) · **Spec:** [SPEC.md](SPEC.md)

> The name *Federated Context Protocol* is a working title. If you prefer *Context Federation
> Protocol (CFP)* or *Personal Context Federation (PCF)*, rename with a find-replace before first release.

## What problem this solves

You may be many things - a leader, an employee, a parent, a friend, a volunteer. Each of those contexts you exist in need **different ways of thinking** and have **different ways of interacting**. You want an intelligent system to help you reason over as much of these contexts as possible, but you cannot pour everything into one shared place: your friends can't see company IP, your employer must not see your private journal, your friends shouldn't necissarily be part of your close family logistics.

FCP resolves this with a simple design, implemented as a standard protocol:

- **Knowledge is tracked in version controlled repos** - repos contain all the ontological maps, mental models and skills required to reason and interact in a particular context
- **Sharing happens at the repository boundary** - many small repos, each scoped to exactly one audience. The repo boundary *is* the sharing boundary, because access control is per-repo.
- **Reasoning happens at the workspace boundary** - an agent mounts several repos at once and reasons over their union. Maximum reach for you; nothing leaks between audiences.

The result is a **hub-and-spoke of repos, federated at read time**: a private *root* you never share, which put you at the center of all digital-intelligence driven outcomes. Collaborative *domain* repos for each long-running context (work, mentorship, family, …), and *constituent* repos beneath them - some yours, some shared, some foreign.

> **Principles vs. conventions.** [SPEC.md](SPEC.md) §3 states the **principles** that define
> conformance (audience isolation, maximal owner reasoning, locality of truth, gated projection,
> provenance, …) with no reference to tools. §4 is the **canonical implementation** - the
> recommended, substitutable mechanisms (git repos, the `_`-prefix, mount orientation, event
> streams). Everything in this README is canonical convention; the principles it serves are in §3.

## The model in one minute

- **Root** - your private apex. The only vantage point with read-access to everything. Holds your deepest goals and the integrative view. Almost never mounted, and if so only by you.
- **Spine** - root plus the *domains* you orient by (Work, Mentorship, Family, …). Unprefixed.
- **Constituents** - repos that compose a domain (your individual slice, teams, solutions, foreign orgs). Underscore-prefixed (`_personal`, `_team-x`) unless foreign (kept as their own name).
- **One-way dependency** - root is upstream of domains, which are upstream of constituents. Upstream **never** depends on downstream. A downstream repo can vanish without breaking anything above it.
- **Orientation = what you mount.** Mount a domain alone → bounded session, can't see siblings or root (the boundary enforces itself). Mount root → integrator session, sees everything.
- **Context crosses boundaries only by published projection**, never by reference. Nothing leaves a sovereign repo except a deliberately gated copy. See [SPEC.md](SPEC.md) §3.5 and §4.6.
- **Locality of truth, with provenance.** Contexts may disagree; and that is treated as signal not noise. The map stays frame-aware and every part carries how it's maintained - *stewarded, proxy, inferred,* or *unowned*. See §3.3, §3.8, §4.8.

## Context as event streams

*(A canonical convention - SPEC §4.7 - not a principle. A federation may satisfy the "faithful views" principle with static, hand-maintained views and never adopt event sourcing.)*

Each context source - a person or a system - owns an append-only **event log**, paired with a folded, human-readable **view**:

```
event-stream/
  kevint@gmail.com/
    events.jsonl   # append-only log - the data, source of truth of what happened
    state.md       # folded view - derived current state, the read/share surface
  whatsapp/
    events.jsonl   # a system feed (re-pulled from its system of record)
  jira/
    events.jsonl   # a system feed (re-pulled from its system of record)
```

One writer per stream (no merge conflicts), global ID as the folder name, and a **default-deny** `.gitignore` so raw data stays local until you explicitly promote a view to a committed "map movement." See [SPEC.md](SPEC.md) §4.7–§4.11.

## Adopt it

1. Read [SPEC.md](SPEC.md) and [CONFORMANCE.md](CONFORMANCE.md).
2. Copy [`templates/root-skeleton/`](templates/root-skeleton/) to a new private repo - that's your root.
3. **Pin the protocol:** download the compiled release for the version you're adopting from [GitHub Releases](https://github.com/KevinT/federatedcontextprotocol/releases) (`fcp-<version>.md` + `.sha256`), verify the hash, and vendor the file into your root's `.fcp/`. Add a `.fcp/lock.json` (see [`templates/fcp-lock.json`](templates/fcp-lock.json)) with the version + SHA-256, and declare `fcp: "<version>"` in your root manifest. Pin a version; never track latest. See [Consuming the spec](#consuming-the-spec) for the exact commands.
4. Create a domain repo per audience. Add the [`templates/gitignore.template`](templates/gitignore.template).
5. Use [`tools/fold.py`](tools/fold.py) to fold `events.jsonl` → `state.md`.
6. Share a domain by adding collaborators to that repo - never by moving files.

## Consuming the spec

The compiled spec is **not tracked in this repo** - it's a build artifact published to
[GitHub Releases](https://github.com/KevinT/federatedcontextprotocol/releases). Each release
carries two immutable, version-pinned assets: `fcp-<version>.md` (the self-contained spec) and
`fcp-<version>.md.sha256` (its integrity anchor). Pull the exact version you're adopting, verify
it, then vendor it into your repo:

```sh
VER=0.1.0
BASE="https://github.com/KevinT/federatedcontextprotocol/releases/download/v${VER}"

curl -fLO "${BASE}/fcp-${VER}.md"
curl -fLO "${BASE}/fcp-${VER}.md.sha256"

# Verify integrity before trusting the file
shasum -a 256 -c "fcp-${VER}.md.sha256"   # macOS
# sha256sum -c "fcp-${VER}.md.sha256"      # Linux

# Vendor the verified file into your root, then pin it in .fcp/lock.json
mkdir -p .fcp && cp "fcp-${VER}.md" .fcp/
```

Always pin a specific version - do the gap review against a fixed file, then commit that file into
your repo. Don't fetch a mutable "latest"; upgrading is a deliberate step (bump `VER`, re-verify,
re-review).

## Releasing (maintainers)

Releases are built and published automatically. Bump [`VERSION`](VERSION), commit, then push a
matching tag:

```sh
git tag v$(cat VERSION)
git push origin v$(cat VERSION)
```

The [`release`](.github/workflows/release.yml) workflow checks the tag against `VERSION`, runs
[`tools/build-release.py`](tools/build-release.py) (compiles the single file + SHA-256 sidecar,
which are consistent by construction), and uploads both assets to the GitHub Release. To build
locally for inspection, run `tools/build-release.py` (output lands in the git-ignored `dist/`).
