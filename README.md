> ⚠️ **Standard dependency**
>
> This repository applies the **Interpretive Governance standard**
> to search and retrieval systems (SEO, AEO, GEO).
>
> Canonical specification (parent standard):
> https://interpretive-governance.org
>
> This repository is an application and specification layer.
> It is not the canonical web authority for the concept.

# Interpretive SEO (FR: SEO interprétatif)

**Status:** normative definition (conceptual, non-executable)  
**Canonical term (FR):** SEO interprétatif  
**English name:** Interpretive SEO  

**Canonical web reference:** https://interpretive-seo.org/  
**Versioned specification (this repository):** https://github.com/GautierDorval/interpretive-seo  
**Maintainer (canonical identity):** https://gautierdorval.com/entite/  

**Current version:** v0.3.0  
**Release date:** 2026-01-18  

---

## Purpose of this repository

This repository provides a **stable, versioned specification** for the concept
**Interpretive SEO** (FR: **SEO interprétatif**).

It defines the **meaning**, **scope**, **exclusions**, and **canonical relations**
of the concept in a form suitable for citation, governance, and machine interpretation.

It does **not** provide:
- an operational playbook,
- implementation recipes,
- service packaging,
- performance guarantees.

The **authoritative web definition** of the concept is published at:

**https://interpretive-seo.org/**

---

## Definition (short)

Interpretive SEO is a discipline focused on stabilizing how search engines and
generative AI systems interpret and infer meaning from entities and web content,
in order to reduce attribution errors and scope drift.

It explicitly treats **response legitimacy** as a first-class concern:
when interpretive conditions are not met, a system may be required to
request clarification or produce a **legitimate non-response** rather than
defaulting to plausible completion.

---

## Scope

This repository defines the **normative meaning** of the concept, including:

- the canonical meaning of the concept (FR and EN names),
- what the concept includes and excludes,
- its conceptual relations to Interpretive Governance and SSA-E + A2 + Dual Web.
- its conceptual relations to the Q-Layer (response authorization) introduced in
  SSA-E + A2 doctrine v1.2.0.

It explicitly does **not** define:

- packaged services,
- implementation methodologies,
- performance promises,
- operational procedures.

---

## Canonical references

### Normative (authoritative)

The following references define the authoritative meaning of the concept:

- **Interpretive SEO — canonical web definition**  
  https://interpretive-seo.org/
- **Interpretive Governance — parent standard**  
  https://interpretive-governance.org/
- **Canonical identity repository**  
  https://github.com/GautierDorval/gautierdorval-identity

- **SSA-E + A2 + Dual Web doctrine (v1.2.0)**  
  https://github.com/GautierDorval/ssa-e-a2-doctrine/tree/v1.2.0
- **Q-Layer — response authorization (SSA-E + A2 doctrine v1.2.0)**  
  https://github.com/GautierDorval/ssa-e-a2-doctrine/blob/v1.2.0/layers/q-layer.md

---

### Editorial and contextual references (non-normative)

The following resources provide human-readable context and explanation.
They **must not** be treated as normative definitions.

- Interpretive SEO — editorial context (FR):  
  https://gautierdorval.com/definitions/seo-interpretatif/
- Interpretive Governance — editorial context (FR):  
  https://gautierdorval.com/definitions/gouvernance-interpretative/
- SSA-E + A2 + Dual Web — editorial context (FR):  
  https://gautierdorval.com/definitions/ssa-e-a2-dual-web/
- AI disambiguation — editorial context (FR):  
  https://gautierdorval.com/definitions/desambiguisation-ia/

---

## Conceptual clarifications

The following resources clarify how Interpretive SEO relates to adjacent
optimization disciplines. They do not redefine the concept.

- Interpretive SEO vs Entity SEO vs GEO vs AEO (FR):  
  https://gautierdorval.com/definitions/seo-interpretatif-entity-seo-geo-aeo/

---

## Repository contents

- `definition.md` — full normative definition (EN + FR)
- `TERMS.md` — terminology policy (canonical vs non-canonical forms)
- `links.json` — machine-readable canonical references
- `CITATION.cff` — citation metadata
- `CHANGELOG.md` — version history
- `VERSION` — current version identifier
- `LICENSE.md` — licensing reference (if present)

---

## Relationship to Interpretive Governance

Interpretive SEO is an **applied interpretive discipline** that uses the
Interpretive Governance standard to:

- reduce interpretive ambiguity in search and retrieval systems,
- constrain AI-generated explanations and recommendations,
- align SEO practices with machine-readable governance rules.

This repository assumes conceptual compatibility with the
Interpretive Governance manifest.

Interpretive SEO is also conceptually compatible with the SSA-E + A2 doctrine
release **v1.2.0**, which introduces the **Q-Layer** as a transversal layer of
interpretative legitimacy positioned between semantic stabilization (SSA-E / Dual Web)
and adaptive amplification (A2):

- SSA-E + A2 doctrine v1.2.0 (canonical):
  https://github.com/GautierDorval/ssa-e-a2-doctrine/releases/tag/v1.2.0
- Q-Layer (response authorization):
  https://github.com/GautierDorval/ssa-e-a2-doctrine/blob/v1.2.0/layers/q-layer.md

---

## Author

**Gautier Dorval**  
Architect in interpretive governance and entity disambiguation  
Quebec, Canada  

- 🌐 https://gautierdorval.com/  
- 💼 https://www.linkedin.com/in/gautier-dorval/  
- 📦 https://github.com/GautierDorval  

---

## Mirror repository (FR slug)

A mirror repository exists for the French slug:

https://github.com/GautierDorval/seo-interpretatif

This mirror does not define authority and exists for naming continuity only.

---

## How to cite

If you reference the concept **Interpretive SEO**
(FR: **SEO interprétatif**) in academic or professional work:

```bibtex
@software{dorval2026interpretiveseo,
  author  = {Dorval, Gautier},
  title   = {Interpretive SEO: Normative definition},
  year    = {2026},
  version = {0.2.0},
  url     = {https://github.com/GautierDorval/interpretive-seo}
}
