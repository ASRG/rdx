# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RDX (Risk Data Exchange) is an open, vendor-neutral format for exchanging automotive cybersecurity risk data (TARA) that is aligned with ISO/SAE 21434 and based on CycloneDX. The project provides both JSON and XML schemas for structured risk data that can be embedded within CycloneDX BOMs or used standalone.

## Common Development Tasks

### Prerequisites
- **JSON validation**: Requires `ajv-cli` (`npm i -g ajv-cli`)
- **XML validation**: Requires `xmllint` (typically pre-installed on macOS/Linux)

### Validation Commands
Run all validations:
```bash
./tools/validate.sh
```

Validate a single JSON example. The schema is JSON Schema Draft 2020-12, so `ajv`
**must** be invoked with `--spec=draft2020` and the `ajv-formats` plugin
(`-c ajv-formats`) — without these it fails to resolve the meta-schema or `format` keywords:
```bash
ajv validate -s spec/json/rdx.schema.json -d examples/rdx-example.json \
  --spec=draft2020 -c ajv-formats --strict=false
```

`tools/validate.sh` runs this for every standalone JSON document (all `examples/rdx-*.json`,
`headlight-tara-iso21434.json`, and `templates/rdx-template.json`), checks the
CycloneDX-embedded JSON/XML for well-formedness, and validates the standalone XML
template against the XSD. The list of documents is hard-coded in the script — when
adding a new standalone example, add it to the `JSON_DOCS` array.

**Gotcha**: `ajv` prints "invalid" for failures but the word "valid" is a substring of
"invalid" — check the exit code (ajv exits non-zero on failure), not a grep for "valid".

XML validation (standalone documents only — CycloneDX-embedded XML has a `bom` root and
is checked for well-formedness only):
```bash
xmllint --noout --schema spec/xml/rdx.xsd templates/rdx-template.xml
```

CI: `.github/workflows/validate.yml` runs `tools/validate.sh` on every push and PR.
(`.github/workflows/claude.yml` is the separate `@claude` issue/PR bot.)

### AI Idea Scout
`.github/workflows/ai-idea-scout.yml` runs weekly (Mondays 09:00 UTC) and on
`workflow_dispatch`. It calls `tools/ai_idea_scout.py`, which uses the OpenAI
Responses API with the `web_search` tool to scout the OWASP CycloneDX / ISO 21434
/ PAS 8475 / UNECE R155 ecosystems and open one GitHub issue per net-new proposal
under the `ai-proposal` label. Requires repo secret `OPENAI_API_KEY`. Run locally
with `OPENAI_API_KEY=... python tools/ai_idea_scout.py --dry-run`.

**Schema parity**: The JSON Schema is the normative reference; the XSD is kept at
field-level parity with it (including `riskLevels`, `riskThresholdMatrix`, cryptographic
`hashes`, structured `architecture`/`dataFlows`, AFR `inputFactors`, impact `categories`,
`componentIds`). When you change one schema, change the other and update both an example
(`examples/rdx-*.json`) and the XML coverage example (`examples/rdx-xml-comprehensive.xml`).
XSD element order is significant — XML must follow the sequence declared in each `complexType`.

### OpenXSAM Conversion
`tools/rdx_to_openxsam.py` converts an RDX JSON document to OpenXSAM format (XML or JSON). No third-party dependencies (stdlib only):
```bash
python tools/rdx_to_openxsam.py --input examples/rdx-example.json --output output/analysis.xml
python tools/rdx_to_openxsam.py --input examples/rdx-example.json --output output/analysis.json --format json
```
See `methodology/XSAM-Gap-Analysis.md` for the RDX↔OpenXSAM mapping and known gaps.

### Development Workflow
1. Create/update schema in `spec/json/rdx.schema.json` or `spec/xml/rdx.xsd`
2. Add/update corresponding examples in `examples/`
3. Run `./tools/validate.sh` to ensure all examples validate
4. Update `REQUIREMENTS.md` if adding new capabilities
5. For all changes, create a GitHub issue first and reference it in commits/PRs

## Architecture

### Schema Files
- **JSON Schema**: `spec/json/rdx.schema.json` — JSON Schema Draft 2020-12 with strict validation
- **XSD**: `spec/xml/rdx.xsd` — XML Schema Definition for XML-based RDX documents

### RDX Object Model

#### Core Risk Assessment Objects
Minimum required fields in **bold**:
- **itemDefinition** (**id**, **title**, boundary, functions, architecture, interfaces, environment, assumptions, countryOfOrigin)
- **assets** (**id**, **title**, properties[C|I|A], linkedDamageScenarioIds, externalIds)
- **damageScenarios** (**id**, **title**, description, impactedFunctions, affectedRoadUsers, references)
- **threatScenarios** (**id**, **title**, **targetedAssetIds[]**, compromisedProperties[], cause, references)
- **attackPaths** (**id**, **title**, **threatScenarioId**, steps[], references)
- **methods** (**id**, **name**, **version**, factors[]) — rating methodologies used
- **attackFeasibilityRatings** (**id**, **attackPathId**, **methodId**, **score**, inputFactors, band, rationale)
- **impactRatings** (**id**, **damageScenarioId**, **methodId**, **score**, categories, rationale)
- **riskValues** (**id**, **threatScenarioId**, **afrRef**, **impactRef**, **methodId**, **score**, band, rationale)
- **controls** (**id**, **title**, catalog, controlId, implementationStatus, requiredCalLevel, achievedCalLevel, references)
- **riskTreatmentDecisions** (**id**, **riskValueId**, **decision**[reduce|avoid|accept|share], controls[], justification)

#### ISO/SAE PAS 8475 CAL & TAF Framework (v0.1.0+)
- **calAssuranceLevels** (**id**, **level**[CAL1-4], **objectives[]**, title, description, assuranceActivities[], references)
- **calAssessments** (**id**, **controlId**, **targetCalLevel**, **assessmentResult**[sufficient|insufficient|pending], achievedCalLevel, evidenceRef, assessmentDate, assessor, rationale)
- **tafAssessments** (**id**, **attackPathId**, **methodId**, **tafScore**, targetContext, tafBand, factorRatings, rationale, assessmentDate)

#### Relationships
- **relationships** (**id**, **relationshipType**, **sourceRef**, **targetRef**, confidence, justification)
  - Standard types: causes, mitigates, implements, assesses, contains, targets, threatens, protects, related_to
  - CAL-specific types: requires_cal, achieves_cal

### Document Structure
Every RDX document requires:
- `schemaVersion`: Currently "0.1.0" (must match exactly)
- `documentId`: UUID format
- `riskSet`: Container with required `itemDefinition` and optional risk objects

### Embedding Patterns
- **CycloneDX JSON**: Embed minified RDX JSON in `metadata.properties` array
- **CycloneDX XML**: Embed `<rdx:...>` elements under `<bom>` using rdx namespace
- **Standalone**: Direct RDX JSON or XML documents (see `examples/rdx-*.json`)

### Examples Structure
- `rdx-example.json`: Basic standalone RDX document
- `rdx-relationships-example.json`: Demonstrates explicit relationship support between risk objects
- `rdx-multiple-threats-example.json`: Shows multiple threat scenarios
- `rdx-mitigation-relationships-example.json`: Shows controls mitigating threats
- `rdx-cal-taf-example.json`: Demonstrates CAL (Cybersecurity Assurance Levels) and TAF (Targeted Attack Feasibility) framework integration
- `rdx-risk-threshold-example.json`: Demonstrates risk threshold / acceptance criteria handling
- `rdx-infotainment-comprehensive-example.json`: Large end-to-end example covering most object types
- `headlight-tara-iso21434.json`: Complete ISO 21434 TARA example for Adaptive Front-lighting System
- `headlight-tara-analysis.md`: Human-readable analysis document for the headlight TARA
- `cyclonedx-embedded.json` / `.xml`: Demonstrates embedding RDX within CycloneDX BOMs
- `rdx-xml-comprehensive.xml`: Standalone XML exercising the full feature set; the XSD coverage/test vector (validated against `spec/xml/rdx.xsd`)

### Templates
- `templates/rdx-template.json` / `rdx-template.xml`: Skeleton documents to start a new RDX file from scratch

### Key Documentation
- `methodology/Methodology.md`: Design principles, object model, encoding patterns
- `methodology/ISO21434-Mapping.md`: ISO/SAE 21434 clause mappings
- `methodology/CAL-TAF-Integration.md`: ISO/SAE PAS 8475 CAL and TAF framework integration
- `methodology/UseCases.md`: Usage scenarios and examples
- `methodology/XSAM-Gap-Analysis.md`: RDX↔OpenXSAM mapping and gap analysis (see `tools/rdx_to_openxsam.py`)
- `REQUIREMENTS.md`: Formal requirements tracking with RDX-XXX identifiers
- `VERSIONING.md`: Semantic versioning policy and compatibility rules
- `CONTRIBUTING.md`: Contribution process including GitHub issue requirements and automated AI review

## Design Principles
- **Strict validation**: Required minimums for data quality; `additionalProperties: false` on objects
- **Versioning**: Semantic versioning (MAJOR.MINOR.PATCH); currently v0.1.0
- **Traceability**: All objects require unique IDs; support for external references and issue tracking
- **CycloneDX compatibility**: Non-invasive to existing tooling; uses standard extension mechanisms
- **Open governance**: Public repo, CI validation, deprecation announcements

## Requirements Process
All new features/changes MUST:
1. Be tracked via GitHub issue with appropriate labels
2. Reference the issue number in commits and PRs
3. Update `REQUIREMENTS.md` with new requirement IDs (RDX-XXX format)
4. Include validation tests (examples that validate against schemas)