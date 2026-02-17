# Changelog — Interpretive SEO (FR: SEO interprétatif)

## Unreleased

- No changes.

## v0.3.2 — 2026-02-16

### Added
- Linked the gautierdorval.com framework registry and the interpretive fidelity framework page (citations vs inference). (2026-02-11)
- Added a machine-first JSON-LD `DefinedTerm` artifact (`interpretive-seo.jsonld`) and a served copy under `public/`.
- Added a minimal drift-control workflow and local verification script to prevent inconsistencies between repo and canonical web surfaces.

### Fixed
- Synchronized `public/definition.html` and `public/humans.txt` with the repository version (including the Q-Layer / response legitimacy section).
- Corrected `CITATION.cff` type (dataset, not software).
- Added a `LICENSE` file (SPDX identifier + canonical links) to improve license detection by tooling.

## v0.3.0 — 2026-01-18

### Added
- Explicit positioning of **response legitimacy** as a first-class concern.
- Conceptual integration of the **Q-Layer (response authorization)** as introduced in
  SSA-E + A2 doctrine v1.2.0.

### Changed
- Updated normative definition (EN + FR) to include legitimate non-response as a
  valid interpretive outcome when conditions are not met.
- Expanded canonical references to include SSA-E + A2 doctrine v1.2.0 and the
  Q-Layer canonical document.

## v0.2.0 — 2026-01-09

### Added
- Author section in README to explicitly declare canonical authorship.
- How to cite section with BibTeX entry for academic and professional attribution.
- Terminology policy enrichment to prevent dilution and misuse of the concept.
- Machine-readable keywords to improve automated classification and discoverability.

### Changed
- Improved README wording to reinforce normative scope and non-operational intent.
- Minor refinements to metadata for consistency across FR and EN terminology.

### Fixed
- Clarified canonical vs non-canonical terminology to avoid confusion with adjacent concepts (AI SEO, GEO, AEO).

## v0.1.0 — 2026-01-09

- Initial publication of the normative definition (EN + FR).
- Added terminology policy and machine-readable canonical links.
- Added citation metadata for attribution.
