#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    'README.md','CHANGELOG.md','CITATION.cff','TERMS.md','links.json','ai-manifest.json','llms.txt','llms-full.txt','humans.txt',
    'ai-governance.json','interpretation-policy.json','response-legitimacy.json','anti-plausibility.json','output-constraints.json','qlayer.json',
    'interpretive-seo.jsonld','entity-graph.jsonld','datasets.jsonld','llm-policy.json','readme.llm.txt','llm-guidelines.md','dualweb-index.md',
    'index.html','definition/index.html','context/index.html','source-precedence/index.html','response-legitimacy/index.html','anti-plausibility/index.html','output-constraints/index.html',
    'fr/index.html','fr/definition/index.html','fr/context/index.html','fr/precedence-des-sources/index.html','fr/legitimite-de-reponse/index.html','fr/anti-plausibilite/index.html','fr/contraintes-de-sortie/index.html',
    '.well-known/ai-governance.json','well-known/ai-governance.json','public/.well-known/ai-governance.json','public/well-known/ai-governance.json',
    'doctrine-index.json','governance-fingerprint.json','public/doctrine-index.json','public/governance-fingerprint.json','public/_headers','public/_redirects','_headers','_redirects'
]
JSON_FILES = [
    'links.json','ai-manifest.json','ai-governance.json','interpretation-policy.json','response-legitimacy.json','anti-plausibility.json','output-constraints.json','qlayer.json',
    'interpretive-seo.jsonld','entity-graph.jsonld','datasets.jsonld','llm-policy.json','doctrine-index.json','governance-fingerprint.json',
    '.well-known/ai-governance.json','well-known/ai-governance.json','public/.well-known/ai-governance.json','public/well-known/ai-governance.json'
]

def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding='utf-8')


def fail(errors: List[str]) -> int:
    for e in errors:
        print(f'[FAIL] {e}')
    return 1


def main() -> int:
    errors: List[str] = []
    version_v = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
    version = version_v[1:] if version_v.startswith('v') else version_v
    for rel in REQUIRED:
        if not (ROOT / rel).exists():
            errors.append(f'Missing required file: {rel}')
    for rel in JSON_FILES:
        try:
            json.loads(read(rel))
        except Exception as e:
            errors.append(f'Invalid JSON in {rel}: {e}')
    if errors:
        return fail(errors)
    for rel in ['links.json','ai-manifest.json','ai-governance.json','interpretation-policy.json','response-legitimacy.json','anti-plausibility.json','output-constraints.json','qlayer.json']:
        root_text = read(rel)
        for mirror in [f'public/{rel}', f'.well-known/{rel}', f'well-known/{rel}', f'public/.well-known/{rel}', f'public/well-known/{rel}']:
            if read(mirror) != root_text:
                errors.append(f'Drift detected between {rel} and {mirror}')
    version_checks = ['README.md','CHANGELOG.md','CITATION.cff','links.json','ai-manifest.json','llms.txt','llms-full.txt','humans.txt','ai-governance.json','public/index.html','public/fr/index.html']
    for rel in version_checks:
        txt = read(rel)
        if version not in txt and version_v not in txt:
            errors.append(f'Version {version} / {version_v} missing from {rel}')
    for rel in ['index.html','definition/index.html','context/index.html','source-precedence/index.html','response-legitimacy/index.html','anti-plausibility/index.html','output-constraints/index.html','fr/index.html','fr/definition/index.html','fr/context/index.html','fr/precedence-des-sources/index.html','fr/legitimite-de-reponse/index.html','fr/anti-plausibilite/index.html','fr/contraintes-de-sortie/index.html']:
        txt = read(rel)
        if 'interpretive-governance.org' not in txt:
            errors.append(f'{rel} must mention interpretive-governance.org')
        if 'inferenslab.org' not in txt:
            errors.append(f'{rel} must mention inferenslab.org')
    if 'plausibility is not authorization' not in read('anti-plausibility.json'):
        errors.append('anti-plausibility.json missing core rule')
    if errors:
        return fail(errors)
    print(f'[OK] Consistency checks passed for {version_v}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
