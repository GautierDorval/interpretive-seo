#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://interpretive-seo.org'

GOV_FILES = [
    'ai-governance.json',
    'interpretation-policy.json',
    'response-legitimacy.json',
    'anti-plausibility.json',
    'output-constraints.json',
    'qlayer.json',
    'links.json',
    'ai-manifest.json',
    'interpretive-seo.jsonld',
    'entity-graph.jsonld',
    'datasets.jsonld',
    'llm-policy.json',
]

GENERATED_FILES = [
    'doctrine-index.json',
    'governance-fingerprint.json',
]

HUMAN_FILES = [
    '/', '/definition/', '/context/', '/source-precedence/', '/response-legitimacy/', '/anti-plausibility/', '/output-constraints/',
    '/fr/', '/fr/definition/', '/fr/context/', '/fr/precedence-des-sources/', '/fr/legitimite-de-reponse/', '/fr/anti-plausibilite/', '/fr/contraintes-de-sortie/'
]

# Served root files that are copied verbatim under public/ (in addition to
# GOV_FILES, GENERATED_FILES, the HUMAN_FILES pages and assets/).
PUBLIC_STATIC_FILES = [
    'llms.txt',
    'llms-full.txt',
    'humans.txt',
    'robots.txt',
    'sitemap.xml',
    '_headers',
    '_redirects',
    'definition.html',
    'favicon.svg',
    'styles.css',
]


def read_bytes(rel: str) -> bytes:
    return (ROOT / rel).read_bytes()


def read_version() -> str:
    """Doctrine version, read from the VERSION file (single source)."""
    raw = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
    return raw[1:] if raw.startswith('v') else raw


def read_release_date(version: str) -> str:
    """Release date of `version`, read from its CHANGELOG.md heading."""
    changelog = (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8')
    match = re.search(rf'^## v{re.escape(version)} \S+ (\d{{4}}-\d{{2}}-\d{{2}})\s*$', changelog, re.MULTILINE)
    if not match:
        raise SystemExit(f'CHANGELOG.md has no dated heading for v{version}')
    return match.group(1)


def write_json(rel: str, data: dict) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def copy_file(rel: str, target: str) -> None:
    path = ROOT / target
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(read_bytes(rel))


def page_file(route: str) -> str:
    stripped = route.strip('/')
    return f'{stripped}/index.html' if stripped else 'index.html'


def public_mirror_files() -> list[str]:
    assets = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / 'assets').rglob('*') if p.is_file())
    return PUBLIC_STATIC_FILES + [page_file(route) for route in HUMAN_FILES] + assets


def sync_mirrors() -> None:
    for rel in GOV_FILES + GENERATED_FILES:
        for target in [
            f'.well-known/{rel}',
            f'well-known/{rel}',
            f'public/{rel}',
            f'public/.well-known/{rel}',
            f'public/well-known/{rel}',
        ]:
            copy_file(rel, target)
    for rel in public_mirror_files():
        copy_file(rel, f'public/{rel}')


def build_doctrine_index(version: str, generated: str) -> dict:
    return {
        'site': SITE,
        'generatedAt': generated,
        'version': version,
        'humanSurfaces': HUMAN_FILES,
        'machineSurfaces': [f'/{x}' for x in GOV_FILES] + ['/llms.txt', '/llms-full.txt', '/humans.txt', '/doctrine-index.json', '/governance-fingerprint.json'],
    }


def build_fingerprint(version: str, generated: str) -> dict:
    h = hashlib.sha256()
    for rel in GOV_FILES + ['llms.txt', 'llms-full.txt', 'humans.txt']:
        h.update(read_bytes(rel))
    return {
        'site': SITE,
        'generatedAt': generated,
        'version': version,
        'sha256': h.hexdigest(),
        'inputs': GOV_FILES + ['llms.txt', 'llms-full.txt', 'humans.txt'],
    }


def main() -> None:
    version = read_version()
    generated = read_release_date(version)
    write_json('doctrine-index.json', build_doctrine_index(version, generated))
    write_json('governance-fingerprint.json', build_fingerprint(version, generated))
    sync_mirrors()


if __name__ == '__main__':
    main()
