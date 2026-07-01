#!/usr/bin/env python3
"""
build-release.py — compile FCP source into a single, hashable release file.

The repo is the source; a release is one immutable file per version,
`dist/fcp-<version>.md`, containing the full normative spec (SPEC.md) with the
event schema embedded as a normative appendix. A SHA-256 sidecar
(`dist/fcp-<version>.md.sha256`) is the integrity anchor adopters pin against.

Usage:
    tools/build-release.py            # build dist/fcp-<VERSION>.md (+ .sha256)
    tools/build-release.py --verify   # rebuild in memory, compare to the sidecar
"""
from __future__ import annotations
import hashlib, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANONICAL_SOURCE = "https://github.com/KevinT/federatedcontextprotocol"  # canonical repo


def build() -> tuple[str, str]:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    spec = (ROOT / "SPEC.md").read_text(encoding="utf-8")
    schema = (ROOT / "schema" / "event.schema.json").read_text(encoding="utf-8").rstrip()

    built = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    header = (
        f"<!-- FCP compiled release — DO NOT EDIT. Built from source.\n"
        f"     version: {version}\n"
        f"     source:  {CANONICAL_SOURCE}\n"
        f"     built:   {built}\n"
        f"     integrity: SHA-256 of this file is recorded in the .sha256 sidecar. -->\n\n"
    )
    appendix = (
        "\n\n---\n\n"
        "## Appendix A — Event envelope schema (normative)\n\n"
        "The canonical JSON Schema for `events.jsonl` lines (SPEC §4.7). This is embedded here so the\n"
        "release file is self-contained and the hash covers the schema too.\n\n"
        "```json\n" + schema + "\n```\n"
    )
    # The spec references schema/event.schema.json by path; in the compiled file that
    # reference resolves to Appendix A below.
    document = header + spec + appendix
    return version, document


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    verify = "--verify" in sys.argv[1:]
    version, document = build()
    digest = sha256(document)
    dist = ROOT / "dist"
    out = dist / f"fcp-{version}.md"
    sidecar = dist / f"fcp-{version}.md.sha256"

    if verify:
        if not out.exists() or not sidecar.exists():
            sys.stderr.write(f"verify: release not built yet ({out.name} / .sha256 missing)\n")
            return 1
        recorded = sidecar.read_text(encoding="utf-8").split()[0].strip()
        on_disk = sha256(out.read_text(encoding="utf-8"))
        rebuilt = digest
        ok = recorded == on_disk == rebuilt
        print(f"recorded:  {recorded}")
        print(f"on-disk:   {on_disk}")
        print(f"rebuilt:   {rebuilt}")
        print("OK — integrity verified" if ok else "MISMATCH — file/sidecar/source disagree")
        return 0 if ok else 2

    dist.mkdir(exist_ok=True)
    out.write_text(document, encoding="utf-8")
    sidecar.write_text(f"{digest}  fcp-{version}.md\n", encoding="utf-8")
    print(f"built {out.relative_to(ROOT)}  ({len(document)} bytes)")
    print(f"sha256 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
