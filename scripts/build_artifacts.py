#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://interpretive-seo.org'
VERSION = '0.4.0'
GENERATED = '2026-03-15'

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

HUMAN_FILES = [
    '/', '/definition/', '/context/', '/source-precedence/', '/response-legitimacy/', '/anti-plausibility/', '/output-constraints/',
    '/fr/', '/fr/definition/', '/fr/context/', '/fr/precedence-des-sources/', '/fr/legitimite-de-reponse/', '/fr/anti-plausibilite/', '/fr/contraintes-de-sortie/'
]


def read_bytes(rel: str) -> bytes:
    return (ROOT / rel).read_bytes()


def write_json(rel: str, data: dict) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def sync_mirrors() -> None:
    for rel in GOV_FILES:
        data = read_bytes(rel)
        for target in [
            f'.well-known/{rel}',
            f'well-known/{rel}',
            f'public/{rel}',
            f'public/.well-known/{rel}',
            f'public/well-known/{rel}',
        ]:
            path = ROOT / target
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)


def build_doctrine_index() -> dict:
    return {
        'site': SITE,
        'generatedAt': GENERATED,
        'version': VERSION,
        'humanSurfaces': HUMAN_FILES,
        'machineSurfaces': [f'/{x}' for x in GOV_FILES] + ['/llms.txt', '/llms-full.txt', '/humans.txt', '/doctrine-index.json', '/governance-fingerprint.json'],
    }


def build_fingerprint() -> dict:
    h = hashlib.sha256()
    for rel in GOV_FILES + ['llms.txt', 'llms-full.txt', 'humans.txt']:
        h.update(read_bytes(rel))
    return {
        'site': SITE,
        'generatedAt': GENERATED,
        'version': VERSION,
        'sha256': h.hexdigest(),
        'inputs': GOV_FILES + ['llms.txt', 'llms-full.txt', 'humans.txt'],
    }


def main() -> None:
    sync_mirrors()
    doctrine = build_doctrine_index()
    fingerprint = build_fingerprint()
    for rel in [
        'doctrine-index.json',
        'public/doctrine-index.json',
        '.well-known/doctrine-index.json',
        'well-known/doctrine-index.json',
        'public/.well-known/doctrine-index.json',
        'public/well-known/doctrine-index.json',
    ]:
        write_json(rel, doctrine)
    for rel in [
        'governance-fingerprint.json',
        'public/governance-fingerprint.json',
        '.well-known/governance-fingerprint.json',
        'well-known/governance-fingerprint.json',
        'public/.well-known/governance-fingerprint.json',
        'public/well-known/governance-fingerprint.json',
    ]:
        write_json(rel, fingerprint)


if __name__ == '__main__':
    main()
