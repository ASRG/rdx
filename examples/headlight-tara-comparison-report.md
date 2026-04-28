# RDX Element Comparison Report: Mandatory vs Optional

**Reference TARA:** ISO/SAE 21434 Annex H – Adaptive Front-lighting System (AFS)  
**RDX Version:** 0.1.0  
**Report Date:** 2026-04-28  
**Methodology:** Two-example comparison — `headlight-tara-comprehensive.json` (all schema elements) vs `headlight-tara-minimal.json` (schema-required fields only)

---

## Methodology

Two RDX documents were created for the same AFS headlight TARA scenario from ISO/SAE 21434 Annex H:

| Example | File | Scope |
|---|---|---|
| **Comprehensive** | `headlight-tara-comprehensive.json` | Every field defined in `rdx.schema.json` populated |
| **Minimal** | `headlight-tara-minimal.json` | Only fields listed in `required` arrays in the schema |

An element present in **both** examples is considered **mandatory** for a viable TARA.  
An element present **only in the comprehensive** example is considered **optional** (an extended capability).

---

## Top-Level Document Fields

| Field | Minimal | Comprehensive | Status | Notes |
|---|:---:|:---:|---|---|
| `schemaVersion` | ✅ | ✅ | **Mandatory** | Schema-required |
| `documentId` | ✅ | ✅ | **Mandatory** | Schema-required; UUID format |
| `riskSet` | ✅ | ✅ | **Mandatory** | Schema-required container |
| `created` | — | ✅ | Optional | ISO 8601 timestamp |
| `createdBy` | — | ✅ | Optional | Tool or analyst name |
| `sources` | — | ✅ | Optional | Reference documents / URNs |
| `bomRefRef` | — | ✅ | Optional | CycloneDX BOM reference link |

---

## `riskSet` — Arrays

| Array | Minimal | Comprehensive | Status | Notes |
|---|:---:|:---:|---|---|
| `itemDefinition` | ✅ | ✅ | **Mandatory** | Schema-required; sole required field in riskSet |
| `assets` | ✅ | ✅ | **Mandatory** | Needed to identify what is at risk |
| `damageScenarios` | ✅ | ✅ | **Mandatory** | Needed to define safety/privacy/security impacts |
| `threatScenarios` | ✅ | ✅ | **Mandatory** | Needed to identify and scope threats |
| `attackPaths` | ✅ | ✅ | **Mandatory** | Needed to describe how threats are realized |
| `methods` | ✅ | ✅ | **Mandatory** | Needed to interpret ratings |
| `attackFeasibilityRatings` | ✅ | ✅ | **Mandatory** | Needed for risk determination |
| `impactRatings` | ✅ | ✅ | **Mandatory** | Needed for risk determination |
| `riskValues` | ✅ | ✅ | **Mandatory** | Needed to express risk level |
| `controls` | ✅ | ✅ | **Mandatory** | Needed for risk treatment |
| `riskTreatmentDecisions` | ✅ | ✅ | **Mandatory** | Needed to record treatment decisions |
| `attackSteps` | — | ✅ | Optional | Granular step-level attack modelling |
| `calAssuranceLevels` | — | ✅ | Optional | ISO/SAE PAS 8475 CAL framework |
| `calAssessments` | — | ✅ | Optional | CAL conformance assessments per control |
| `tafAssessments` | — | ✅ | Optional | Targeted Attack Feasibility (TAF) analysis |
| `relationships` | — | ✅ | Optional | Explicit cross-object traceability links |

---

## `itemDefinition` Fields

| Field | Minimal | Comprehensive | Status |
|---|:---:|:---:|---|
| `id` | ✅ | ✅ | **Mandatory** |
| `title` | ✅ | ✅ | **Mandatory** |
| `boundary` | — | ✅ | Optional |
| `functions` | — | ✅ | Optional |
| `architecture` (string) | — | — | Optional (deprecated form) |
| `architecture` (structured object) | — | ✅ | Optional |
| `architecture.components` | — | ✅ | Optional |
| `architecture.dataFlows` | — | ✅ | Optional |
| `architecture.diagramUrl` | — | ✅ | Optional |
| `interfaces` | — | ✅ | Optional |
| `environment` | — | ✅ | Optional |
| `assumptions` | — | ✅ | Optional |
| `countryOfOrigin` | — | ✅ | Optional |
| `hashes` | — | ✅ | Optional |

---

## `assets[]` Item Fields

| Field | Minimal | Comprehensive | Status |
|---|:---:|:---:|---|
| `id` | ✅ | ✅ | **Mandatory** |
| `title` | ✅ | ✅ | **Mandatory** |
| `properties` | — | ✅ | Optional |
| `linkedDamageScenarioIds` | — | ✅ | Optional |
| `externalIds` | — | ✅ | Optional |
| `hashes` | — | ✅ | Optional |
| `componentIds` | — | ✅ | Optional |

---

## `damageScenarios[]` Item Fields

| Field | Minimal | Comprehensive | Status |
|---|:---:|:---:|---|
| `id` | ✅ | ✅ | **Mandatory** |
| `title` | ✅ | ✅ | **Mandatory** |
| `description` | — | ✅ | Optional |
| `impactedFunctions` | — | ✅ | Optional |
| `affectedRoadUsers` | — | ✅ | Optional |
| `references` | — | ✅ | Optional |

---

## `threatScenarios[]` Item Fields

| Field | Minimal | Comprehensive | Status |
|---|:---:|:---:|---|
| `id` | ✅ | ✅ | **Mandatory** |
| `title` | ✅ | ✅ | **Mandatory** |
| `targetedAssetIds` | ✅ | ✅ | **Mandatory** |
| `compromisedProperties` | — | ✅ | Optional |
| `cause` | — | ✅ | Optional |
| `references` | — | ✅ | Optional |
| `componentIds` | — | ✅ | Optional |

---

## `attackSteps[]` Item Fields (all optional — entire section is optional)

| Field | Minimal | Comprehensive | Status |
|---|:---:|:---:|---|
| `id` | — | ✅ | Optional (required if section used) |
| `title` | — | ✅ | Optional (required if section used) |
| `description` | — | ✅ | Optional |
| `attackFeasibilityRatingIds` | — | ✅ | Optional |
| `controlIds` | — | ✅ | Optional |
| `references` | — | ✅ | Optional |

---

## `attackPaths[]` Item Fields

| Field | Minimal | Comprehensive | Status |
|---|:---:|:---:|---|
| `id` | ✅ | ✅ | **Mandatory** |
| `title` | ✅ | ✅ | **Mandatory** |
| `threatScenarioId` | ✅ | ✅ | **Mandatory** |
| `stepIds` | — | ✅ | Optional (preferred over deprecated `steps`) |
| `steps` | — | — | Deprecated |
| `references` | — | ✅ | Optional |

---

## `methods[]` Item Fields

| Field | Minimal | Comprehensive | Status |
|---|:---:|:---:|---|
| `id` | ✅ | ✅ | **Mandatory** |
| `name` | ✅ | ✅ | **Mandatory** |
| `version` | ✅ | ✅ | **Mandatory** |
| `factors` | — | ✅ | Optional |
| `riskThresholdMatrix` | — | ✅ | Optional |
| `riskThresholdMatrix[].band` | — | ✅ | Optional (required if section used) |
| `riskThresholdMatrix[].allowedTreatments` | — | ✅ | Optional (required if section used) |
| `riskThresholdMatrix[].scoreRange` | — | ✅ | Optional |
| `riskThresholdMatrix[].escalationRequired` | — | ✅ | Optional |
| `riskThresholdMatrix[].rationale` | — | ✅ | Optional |
| `riskThresholdMatrix[].references` | — | ✅ | Optional |

---

## `attackFeasibilityRatings[]` Item Fields

| Field | Minimal | Comprehensive | Status |
|---|:---:|:---:|---|
| `id` | ✅ | ✅ | **Mandatory** |
| `attackPathId` OR `attackStepId` | ✅ | ✅ | **Mandatory** (one required) |
| `methodId` | ✅ | ✅ | **Mandatory** |
| `score` | ✅ | ✅ | **Mandatory** |
| `inputFactors` | — | ✅ | Optional |
| `band` | — | ✅ | Optional |
| `rationale` | — | ✅ | Optional |

---

## `impactRatings[]` Item Fields

| Field | Minimal | Comprehensive | Status |
|---|:---:|:---:|---|
| `id` | ✅ | ✅ | **Mandatory** |
| `damageScenarioId` | ✅ | ✅ | **Mandatory** |
| `methodId` | ✅ | ✅ | **Mandatory** |
| `score` | ✅ | ✅ | **Mandatory** |
| `categories` | — | ✅ | Optional |
| `rationale` | — | ✅ | Optional |

---

## `riskValues[]` Item Fields

| Field | Minimal | Comprehensive | Status |
|---|:---:|:---:|---|
| `id` | ✅ | ✅ | **Mandatory** |
| `threatScenarioId` | ✅ | ✅ | **Mandatory** |
| `afrRef` | ✅ | ✅ | **Mandatory** |
| `impactRef` | ✅ | ✅ | **Mandatory** |
| `methodId` | ✅ | ✅ | **Mandatory** |
| `score` | ✅ | ✅ | **Mandatory** |
| `band` | — | ✅ | Optional |
| `rationale` | — | ✅ | Optional |

---

## `controls[]` Item Fields

| Field | Minimal | Comprehensive | Status |
|---|:---:|:---:|---|
| `id` | ✅ | ✅ | **Mandatory** |
| `title` | ✅ | ✅ | **Mandatory** |
| `catalog` | — | ✅ | Optional |
| `controlId` | — | ✅ | Optional |
| `implementationStatus` | — | ✅ | Optional |
| `requiredCalLevel` | — | ✅ | Optional |
| `achievedCalLevel` | — | ✅ | Optional |
| `references` | — | ✅ | Optional |
| `hashes` | — | ✅ | Optional |

---

## `riskTreatmentDecisions[]` Item Fields

| Field | Minimal | Comprehensive | Status |
|---|:---:|:---:|---|
| `id` | ✅ | ✅ | **Mandatory** |
| `riskValueId` | ✅ | ✅ | **Mandatory** |
| `decision` | ✅ | ✅ | **Mandatory** (`reduce`/`avoid`/`accept`/`share`) |
| `controls` | — | ✅ | Optional |
| `justification` | — | ✅ | Optional |

---

## Extended Sections (all optional)

### `calAssuranceLevels[]` Item Fields

| Field | Status |
|---|---|
| `id` | Required if section used |
| `level` (CAL1–CAL4) | Required if section used |
| `objectives` | Required if section used |
| `title` | Optional |
| `description` | Optional |
| `assuranceActivities` | Optional |
| `references` | Optional |

### `calAssessments[]` Item Fields

| Field | Status |
|---|---|
| `id` | Required if section used |
| `controlId` | Required if section used |
| `targetCalLevel` | Required if section used |
| `assessmentResult` | Required if section used |
| `achievedCalLevel` | Optional |
| `evidenceRef` | Optional |
| `assessmentDate` | Optional |
| `assessor` | Optional |
| `rationale` | Optional |

### `tafAssessments[]` Item Fields

| Field | Status |
|---|---|
| `id` | Required if section used |
| `attackPathId` | Required if section used |
| `methodId` | Required if section used |
| `tafScore` | Required if section used |
| `targetContext` | Optional |
| `tafBand` | Optional |
| `factorRatings` | Optional |
| `rationale` | Optional |
| `assessmentDate` | Optional |

### `relationships[]` Item Fields

| Field | Status |
|---|---|
| `id` | Required if section used |
| `relationshipType` | Required if section used |
| `sourceRef` | Required if section used |
| `targetRef` | Required if section used |
| `confidence` | Optional |
| `justification` | Optional |

---

## Schema Change Recommendations

Based on this comparison, the following schema changes were applied to `spec/json/rdx.schema.json`:

### 1. Fix schema syntax error
A stray `d` character at the end of the `properties` closing brace and a duplicate `additionalProperties` block made the schema invalid JSON. Fixed in this PR.

### 2. Expand `riskSet.required` to include core TARA arrays
The schema previously only required `itemDefinition` within `riskSet`. Adding the ten arrays that appear in both the minimal and comprehensive examples formalizes what constitutes a minimum viable TARA:

```json
"required": [
  "itemDefinition",
  "assets",
  "damageScenarios",
  "threatScenarios",
  "attackPaths",
  "methods",
  "attackFeasibilityRatings",
  "impactRatings",
  "riskValues",
  "controls",
  "riskTreatmentDecisions"
]
```

Arrays **not** added to required (remain optional extended elements): `attackSteps`, `calAssuranceLevels`, `calAssessments`, `tafAssessments`, `relationships`.

### 3. Add `description` annotations marking optional fields
Optional top-level fields (`created`, `createdBy`, `sources`, `bomRefRef`) and optional per-object fields (`boundary`, `functions`, `categories`, `rationale`, `band`, `inputFactors`, etc.) have been annotated with `"Optional."` in their `description` to make tool-assisted authoring easier.

---

## Summary

| Category | Mandatory Count | Optional Count |
|---|:---:|:---:|
| Top-level document fields | 3 | 4 |
| riskSet arrays | 11 | 5 |
| itemDefinition fields | 2 | 8 |
| assets[] item fields | 2 | 5 |
| damageScenarios[] item fields | 2 | 4 |
| threatScenarios[] item fields | 3 | 4 |
| attackSteps[] item fields | 0 (whole section optional) | 6 |
| attackPaths[] item fields | 3 | 2 |
| methods[] item fields | 3 | 6 |
| attackFeasibilityRatings[] item fields | 4 | 3 |
| impactRatings[] item fields | 4 | 2 |
| riskValues[] item fields | 6 | 2 |
| controls[] item fields | 2 | 7 |
| riskTreatmentDecisions[] item fields | 3 | 2 |
| calAssuranceLevels[] (whole section) | 0 (optional) | — |
| calAssessments[] (whole section) | 0 (optional) | — |
| tafAssessments[] (whole section) | 0 (optional) | — |
| relationships[] (whole section) | 0 (optional) | — |

---

*Generated from: `examples/headlight-tara-comprehensive.json` and `examples/headlight-tara-minimal.json`*  
*RDX Schema Version: 0.1.0*
