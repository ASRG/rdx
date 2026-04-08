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

Validate individual JSON examples:
```bash
ajv -s spec/json/rdx.schema.json -d examples/rdx-example.json --strict=false
ajv -s spec/json/rdx.schema.json -d examples/rdx-relationships-example.json --strict=false
ajv -s spec/json/rdx.schema.json -d examples/rdx-multiple-threats-example.json --strict=false
ajv -s spec/json/rdx.schema.json -d examples/rdx-mitigation-relationships-example.json --strict=false
ajv -s spec/json/rdx.schema.json -d examples/rdx-cal-taf-example.json --strict=false
ajv -s spec/json/rdx.schema.json -d examples/headlight-tara-iso21434.json --strict=false
```

**Note**: The schema uses JSON Schema Draft 2020-12. If `ajv-cli` reports issues with the schema version, the examples are still valid JSON and conform to required fields.

Validate XML (currently commented out in validate.sh):
```bash
xmllint --noout --schema spec/xml/rdx.xsd examples/cyclonedx-embedded.xml
```

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
- **attackSteps** (**id**, **title**, description, **attackFeasibilityRatings[]**, controlIds[], references) — steps with embedded feasibility ratings
- **methods** (**id**, **name**, **version**, factors[]) — rating methodologies used; standard ISO/SAE 21434 factors: elapsedTime, expertise, knowledge, windowOfOpportunity, equipment
- **attackFeasibilityRatings** (**id**, **attackPathId**, **methodId**, **score**, inputFactors, band, rationale) — top-level path-level ratings referenced by riskValues.afrRef; prefer embedding ratings directly in attackSteps
- **impactRatings** (**id**, **damageScenarioId**, **methodId**, **score**, categories, rationale)
- **riskValues** (**id**, **threatScenarioId**, **afrRef**, **impactRef**, **methodId**, **score**, band, rationale)
- **controls** (**id**, **title**, catalog, controlId, implementationStatus, requiredCalLevel, achievedCalLevel, references)
- **riskTreatmentDecisions** (**id**, **riskValueId**, **decision**[treat|avoid|accept|share], controls[], justification)

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
- `headlight-tara-iso21434.json`: Complete ISO 21434 TARA example for Adaptive Front-lighting System
- `headlight-tara-analysis.md`: Human-readable analysis document for the headlight TARA
- `cyclonedx-embedded.json` / `.xml`: Demonstrates embedding RDX within CycloneDX BOMs

### Key Documentation
- `methodology/Methodology.md`: Design principles, object model, encoding patterns
- `methodology/ISO21434-Mapping.md`: ISO/SAE 21434 clause mappings
- `methodology/CAL-TAF-Integration.md`: ISO/SAE PAS 8475 CAL and TAF framework integration
- `methodology/UseCases.md`: Usage scenarios and examples
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