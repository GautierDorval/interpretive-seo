# Changelog — Interpretive SEO (FR: SEO interprétatif)

## v0.4.0 — 2026-03-15

### Added
- Added a hard public governance layer: `ai-governance.json`, `interpretation-policy.json`, `response-legitimacy.json`, `anti-plausibility.json`, `output-constraints.json`, and `qlayer.json`.
- Added bilingual governance pages for source precedence, response legitimacy, anti-plausibility, and output constraints.
- Added `entity-graph.jsonld`, `datasets.jsonld`, `llm-policy.json`, `readme.llm.txt`, `llm-guidelines.md`, and `dualweb-index.md`.
- Added explicit public doctrinal association to `https://inferenslab.org/` while preserving `https://interpretive-governance.org/` as the parent standard.
- Added `doctrine-index.json` and `governance-fingerprint.json` generation.
- Added mirrors under `/.well-known/` and `/well-known/`.
- Added a GitHub workflow for consistency checks.

### Changed
- Upgraded version metadata from `v0.3.2` to `v0.4.0`.
- Strengthened `README.md`, `links.json`, `ai-manifest.json`, `llms.txt`, `llms-full.txt`, `humans.txt`, and `interpretive-seo.jsonld`.
- Expanded home, definition, and context pages to expose hard public governance and doctrinal associations.
- Tightened headers and redirects for governance artifacts.

## v0.3.2 — 2026-02-16

### Added
- Linked the gautierdorval.com framework registry and the interpretive fidelity framework page (citations vs inference).
- Added a machine-first JSON-LD `DefinedTerm` artifact (`interpretive-seo.jsonld`) and a served copy under `public/`.
- Added a minimal drift-control workflow and local verification script to prevent inconsistencies between repo and canonical web surfaces.
