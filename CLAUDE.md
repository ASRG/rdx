# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RDX (Risk Data Exchange) is an open format for exchanging automotive cybersecurity risk data (TARA) that is based on CycloneDX and aligned with ISO/SAE 21434. The project provides both JSON and XML schemas for structured risk data that can be embedded within CycloneDX BOMs or used standalone.

## Common Development Tasks

### Validation
- **JSON validation**: Requires `ajv-cli` (install with `npm i -g ajv-cli`)
  ```bash
  ajv -s spec/json/rdx.schema.json -d examples/rdx-example.json --strict=false
  ```
- **XML validation**: Requires `xmllint`
  ```bash
  xmllint --noout --schema spec/xml/rdx.xsd examples/cyclonedx-embedded.xml
  ```
- **Run all validations**: `./tools/validate.sh` (currently has commands commented out)

## Architecture

### Core Components
- **Schema definitions**: `spec/json/rdx.schema.json` (JSON Schema) and `spec/xml/rdx.xsd` (XSD)
- **Examples**: `examples/` contains sample RDX documents and CycloneDX-embedded examples
- **Templates**: `templates/` provides starting points for RDX documents

### RDX Object Model
The schema defines these core risk assessment objects:
- **itemDefinition**: The system/component being assessed (required)
- **assets**: Things to protect with CIA properties
- **damageScenarios**: Potential harm scenarios
- **threatScenarios**: Security threats targeting assets
- **attackPaths**: How threats could be realized
- **attackFeasibilityRatings**: Likelihood assessments
- **impactRatings**: Consequence assessments  
- **riskValues**: Combined risk scores
- **controls**: Security measures
- **riskTreatmentDecisions**: How risks are handled (treat/avoid/accept/share)

### Embedding Patterns
- **CycloneDX JSON**: RDX data goes in `metadata.properties` as minified JSON
- **CycloneDX XML**: RDX elements use `rdx:` namespace under `<bom>`
- **Standalone**: Direct RDX JSON/XML documents

## Key Design Principles
- Strict schema validation with required minimums for data quality
- Versioning follows SemVer (currently v0.1.0)
- All objects require unique IDs for traceability
- Non-invasive to existing CycloneDX tooling