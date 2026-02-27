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

    # Required canonical surfaces (repository + published web surfaces)
    required_files = [
        "README.md",
        "definition.md",
        "links.json",
        "public/links.json",
        "public/index.html",
        "public/definition/index.html",
        "public/context/index.html",
        "public/fr/index.html",
        "public/fr/definition/index.html",
        "public/fr/context/index.html",
        "public/humans.txt",
        "public/ai-manifest.json",
        "public/.well-known/ai-governance.json",
        "public/llms-full.txt",
        "public/llms.txt",
        "interpretive-seo.jsonld",
        "public/interpretive-seo.jsonld",
        "public/_redirects",
        "public/robots.txt",
        "public/sitemap.xml",
        "public/_headers",
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
        "public/definition/index.html": version_v,
        "public/context/index.html": version_v,
        "public/fr/index.html": version,
        "public/fr/definition/index.html": version_v,
        "public/fr/context/index.html": version_v,
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

    # Quick sanity: Q-Layer must be present in the public definition surface
    if "Q-Layer" not in read_text(ROOT / "public/definition/index.html"):
        errors.append("public/definition/index.html must mention Q-Layer (response legitimacy).")

    # P0: hreflang must not lie (FR pages must exist and be French)
    fr_pages = [
        "public/fr/index.html",
        "public/fr/definition/index.html",
        "public/fr/context/index.html",
    ]
    fr_markers = ["SEO interprétatif", "Définition", "Contexte", "Accueil"]
    for rel in fr_pages:
        txt = read_text(ROOT / rel)
        if 'lang="fr-CA"' not in txt:
            errors.append(f"{rel} must declare lang=\"fr-CA\"")
        if not any(m in txt for m in fr_markers):
            errors.append(f"{rel} appears non-FR (missing FR markers).")

    # P1: hreflang must exist on key pages (home, definition, context)
    pairs = [
        ("public/index.html", "https://interpretive-seo.org/fr/"),
        ("public/definition/index.html", "https://interpretive-seo.org/fr/definition/"),
        ("public/context/index.html", "https://interpretive-seo.org/fr/context/"),
        ("public/fr/index.html", "https://interpretive-seo.org/"),
        ("public/fr/definition/index.html", "https://interpretive-seo.org/definition/"),
        ("public/fr/context/index.html", "https://interpretive-seo.org/context/"),
    ]
    for rel, expected_href in pairs:
        txt = read_text(ROOT / rel)
        if "hreflang" not in txt:
            errors.append(f"{rel} is missing hreflang alternates.")
        if expected_href not in txt:
            errors.append(f"{rel} missing alternate href: {expected_href}")

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
