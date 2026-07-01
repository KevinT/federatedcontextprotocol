# Purpose - Root

This repository is the **apex (root)** of my federation. It is private to me and almost never mounted: I open it only for integrative reflection across all my parts.

It holds:

- my deepest, cross-cutting goals and values (`.meta/objectives.md`);
- the master manifest of which domain repos exist and where (`meta.json`);
- the integrative `journal/` and the syntheses produced when reasoning across domains;
- the `publish/` source from which gated projections are pushed down to domains.

It does **not** hold any domain's content. Each domain (Work, Mentorship, Family, …) is its own repository, cloned in as a downstream constituent. Per the **one-way dependency** principle, this root never depends on anything in those domains; they may reference it.
