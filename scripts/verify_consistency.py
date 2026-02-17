#!/usr/bin/env python3
"""
verify_consistency.py

Minimal drift-control checks for Interpretive SEO.

This script is intentionally small and dependency-free.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import List, Tuple


ROOT = Path(__file__).resolve().parents[1]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fail(errors: List[str]) -> int:
    for e in errors:
        print(f"[FAIL] {e}")
    return 1


def ok(msg: str) -> None:
    print(f"[OK] {msg}")


def extract_version() -> Tuple[str, str]:
    v = read_text(ROOT / "VERSION").strip()
    if not v.startswith("v"):
        raise ValueError("VERSION must start with 'v' (e.g., v0.3.2).")
    return v, v[1:]


def parse_json(path: Path) -> None:
    try:
        json.loads(read_text(path))
    except Exception as e:
        raise ValueError(f"Invalid JSON: {path} ({e})")


def main() -> int:
    errors: List[str] = []

    try:
        version_v, version = extract_version()
    except Exception as e:
        return fail([str(e)])

    required_files = [
        "README.md",
        "definition.md",
        "links.json",
        "public/links.json",
        "public/index.html",
        "public/definition.html",
        "public/humans.txt",
        "public/ai-manifest.json",
        "public/.well-known/ai-governance.json",
        "public/llms-full.txt",
        "interpretive-seo.jsonld",
        "public/interpretive-seo.jsonld",
        "CITATION.cff",
        "LICENSE",
    ]
    for rel in required_files:
        if not (ROOT / rel).exists():
            errors.append(f"Missing required file: {rel}")

    if errors:
        return fail(errors)

    # JSON validity
    for rel in [
        "links.json",
        "public/links.json",
        "public/ai-manifest.json",
        "public/.well-known/ai-governance.json",
        "interpretive-seo.jsonld",
        "public/interpretive-seo.jsonld",
    ]:
        try:
            parse_json(ROOT / rel)
        except Exception as e:
            errors.append(str(e))

    # links.json must be identical across root and public/
    try:
        a = read_text(ROOT / "links.json")
        b = read_text(ROOT / "public/links.json")
        if a != b:
            errors.append("links.json drift: root and public/links.json differ (they must be identical).")
    except Exception as e:
        errors.append(f"links.json check failed: {e}")

    # Version string must appear in key human-facing surfaces
    checks = {
        "README.md": version_v,
        "definition.md": version_v,
        "public/index.html": version,
        "public/definition.html": version_v,
        "public/humans.txt": version,
        "public/ai-manifest.json": version,
        "public/.well-known/ai-governance.json": version,
        "public/llms-full.txt": version,
        "CITATION.cff": version,
    }
    for rel, needle in checks.items():
        txt = read_text(ROOT / rel)
        if needle not in txt:
            errors.append(f"Version drift: '{needle}' not found in {rel}")

    # Quick sanity: Q-Layer must be present in public definition surface
    if "Q-Layer" not in read_text(ROOT / "public/definition.html"):
        errors.append("public/definition.html must mention Q-Layer (response legitimacy).")

    # CITATION type should not be software
    if "type: software" in read_text(ROOT / "CITATION.cff"):
        errors.append("CITATION.cff must not declare type: software (use dataset or omit).")

    # License SPDX identifier present
    if "SPDX-License-Identifier: CC-BY-NC-SA-4.0" not in read_text(ROOT / "LICENSE"):
        errors.append("LICENSE must include SPDX-License-Identifier: CC-BY-NC-SA-4.0")

    if errors:
        return fail(errors)

    ok(f"Consistency checks passed for {version_v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
