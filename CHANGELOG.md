# Changelog

All notable changes to RDX are documented in this file. The format is based on
[Keep a Changelog](https://keepachangelog.com/), and the project follows
[Semantic Versioning](VERSIONING.md).

## v0.1.0 — Initial release

First public release of the RDX (Risk Data Exchange) format.

### Schemas
- JSON Schema (`spec/json/rdx.schema.json`, Draft 2020-12) — normative reference for v0.1.0.
- XML Schema (`spec/xml/rdx.xsd`) — at field-level parity with the JSON Schema,
  including structured `architecture`/`dataFlows`, cryptographic `hashes`, `riskLevels`,
  `riskThresholdMatrix`, AFR `inputFactors`, impact `categories`, and `componentIds`.

### Core risk model
- `itemDefinition`, `assets`, `damageScenarios`, `threatScenarios`, `attackSteps`,
  `attackPaths`, `methods`, `attackFeasibilityRatings`, `impactRatings`, `riskValues`,
  `controls`, and `riskTreatmentDecisions`.
- Risk treatment decisions use `reduce | avoid | accept | share` (aligned with
  ISO/SAE 21434 risk treatment options).

### Frameworks and extensions
- Explicit machine-readable `relationships` between risk objects.
- ISO/SAE PAS 8475 **CAL** (Cybersecurity Assurance Levels) and **TAF** (Targeted
  Attack Feasibility) objects: `calAssuranceLevels`, `calAssessments`, `tafAssessments`.
- Configurable per-methodology `riskLevels` (named bands with ordinal rank, optional
  score range, and treatment guidance).
- `riskThresholdMatrix` on methods to codify allowed treatments per risk band.
- Cryptographic `hashes` for integrity verification.
- Structured system architecture (`architecture` components and `dataFlows`).
- `countryOfOrigin` for supply-chain transparency.
- Vendor-specific fields permitted via `additionalProperties` (JSON) and
  `##other`-namespace extensibility (XML).

### CycloneDX integration
- Embed RDX in CycloneDX JSON via `metadata.properties`.
- Embed RDX in CycloneDX XML via the `rdx:` namespace.

### Tooling and examples
- `tools/validate.sh` validates all JSON documents against the schema and checks
  XML well-formedness / standalone XML against the XSD.
- `tools/rdx_to_openxsam.py` converts RDX JSON to OpenXSAM (XML or JSON).
- Standalone and embedded examples under `examples/`, plus `templates/`.
- GitHub Actions workflow runs validation on every push and pull request.

### Known limitations
- The JSON Schema is the normative reference for v0.1.0. The XSD is kept at
  field-level parity with it; where the JSON document carries metadata as siblings
  of `riskSet` (`created`, `createdBy`, `sources`, `bomRefRef`), the XSD represents
  these as attributes / a leading `sources` element on the `riskSet` root.
- `xmllint` validates standalone RDX XML against the XSD; CycloneDX-embedded XML is
  checked for well-formedness only (its root is the CycloneDX `bom` element).
