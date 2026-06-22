# RDX Requirements

This document consolidates all requirements for the Risk Data Exchange (RDX) format based on the project's documentation, schemas, and use cases.

## 1. Core Objectives

### 1.1 Primary Goals
- **RDX-001**: Cover core ISO/SAE 21434 risk work products (Clause 15) and related lifecycle outputs
- **RDX-002**: Interoperate with existing SBOM/BOM ecosystems (CycloneDX JSON & XML)
- **RDX-003**: Provide strict schemas, versioning, and conformance levels
- **RDX-004**: Enable first-class data quality & governance (identity, provenance, validation, traceability)
- **RDX-005**: Support vendor-neutral format for exchanging automotive cybersecurity risk data (TARA) across tools and organizations

### 1.2 Design Principles
- **RDX-006**: Base format on CycloneDX for transport, signing, linking/BOM-Link, and tooling
- **RDX-007**: Ensure compatibility with non-invasive integration to CycloneDX consumers
- **RDX-008**: Maintain open governance with public repository, SemVer, deprecations, and CI validation
- **RDX-009**: Support profiles for producers/consumers

## 2. Data Model Requirements

### 2.1 Required Core Objects
Each object must include minimum required fields (marked in **bold**):

#### Item Definition
- **RDX-010**: Must include **id** and **title** fields (required)
- **RDX-011**: Should support boundary, functions, architecture, interfaces, environment, assumptions fields

#### Assets
- **RDX-012**: Must include **id** and **title** fields (required)
- **RDX-013**: Must specify CIA properties (Confidentiality, Integrity, Availability)
- **RDX-014**: Should support linkedDamageScenarioIds and externalIds

#### Damage Scenarios
- **RDX-015**: Must include **id** and **title** fields (required)
- **RDX-016**: Should support description, impactedFunctions, affectedRoadUsers, references

#### Threat Scenarios
- **RDX-017**: Must include **id**, **title**, and **targetedAssetIds[]** fields (required)
- **RDX-018**: Should support compromisedProperties[], cause, references

#### Attack Paths
- **RDX-019**: Must include **id**, **title**, and **threatScenarioId** fields (required)
- **RDX-020**: Should support steps[] and references

#### Attack Feasibility Ratings
- **RDX-021**: Must include **id**, **attackPathId**, **methodId**, and **score** fields (required)
- **RDX-022**: Should support inputFactors, band, rationale

#### Impact Ratings
- **RDX-023**: Must include **id**, **damageScenarioId**, **methodId**, and **score** fields (required)
- **RDX-024**: Should support categories and rationale

#### Risk Values
- **RDX-025**: Must include **id**, **threatScenarioId**, **afrRef**, **impactRef**, **methodId**, and **score** fields (required)
- **RDX-026**: Should support band and rationale

#### Controls
- **RDX-027**: Must include **id** and **title** fields (required)
- **RDX-028**: Should support catalog, controlId, implementationStatus, references

#### Risk Treatment Decisions
- **RDX-029**: Must include **id**, **riskValueId**, and **decision** fields (required)
- **RDX-030**: Decision must be one of: reduce, avoid, accept, share
- **RDX-031**: Should support controls[] and justification

### 2.2 Document Structure
- **RDX-032**: Must include schemaVersion, documentId, and riskSet as required top-level fields
- **RDX-033**: schemaVersion must match pattern "^0\.1\.0$" (current version)
- **RDX-034**: documentId must be a valid UUID
- **RDX-035**: Should support optional created (date-time), createdBy, sources[], bomRefRef fields

## 3. Encoding Requirements

### 3.1 Dual Encoding Support
- **RDX-036**: Must support JSON encoding with `rdx.schema.json`
- **RDX-037**: Must support XML encoding with `rdx.xsd`
- **RDX-038**: JSON must be embeddable in CycloneDX using `metadata.properties`
- **RDX-039**: XML must be embeddable in CycloneDX via `rdx:` namespace

### 3.2 Encoding Patterns
- **RDX-040**: CycloneDX JSON: embed minified RDX JSON in `metadata.properties`
- **RDX-041**: CycloneDX XML: embed `<rdx:...>` under `<bom>`
- **RDX-042**: Support standalone RDX JSON or XML documents

## 4. ISO/SAE 21434 Compliance

### 4.1 Work Product Mapping
- **RDX-043**: Item definition maps to Clause 9.3 / WP-09-01
- **RDX-044**: Damage scenarios map to Clause 15.5 / WP-15-01
- **RDX-045**: Assets (CIA) map to Clause 15.4 / WP-15-02
- **RDX-046**: Threat scenarios map to Clause 15.5 / WP-15-03
- **RDX-047**: Attack paths map to Clause 15.6 / WP-15-05
- **RDX-048**: AFR maps to Clause 15.7 / WP-15-06
- **RDX-049**: Impact rating maps to Clause 15.5 / WP-15-04
- **RDX-050**: Risk values map to Clause 15.8 / WP-15-07
- **RDX-051**: Treatment decisions map to Clause 15.9 / WP-15-08

## 5. Validation Requirements

### 5.1 Schema Validation
- **RDX-052**: JSON documents must validate against `spec/json/rdx.schema.json`
- **RDX-053**: XML documents must validate against `spec/xml/rdx.xsd`
- **RDX-054**: Support validation via ajv-cli for JSON (`ajv -s spec/json/rdx.schema.json -d <file> --strict=false`)
- **RDX-055**: Support validation via xmllint for XML (`xmllint --noout --schema spec/xml/rdx.xsd <file>`)
- **RDX-056**: Provide validation script at `tools/validate.sh`

### 5.2 Data Quality
- **RDX-057**: Enforce required minimums for all objects
- **RDX-058**: Support controlled vocabularies where applicable
- **RDX-059**: Enable CI validation
- **RDX-060**: Support provenance tracking
- **RDX-061**: Enable integrity/signing mechanisms
- **RDX-062**: All objects must use unique IDs for traceability

## 6. Versioning Requirements

### 6.1 Version Management
- **RDX-063**: Use Semantic Versioning (MAJOR.MINOR.PATCH)
- **RDX-064**: Maintain compatibility within same MAJOR version for MINOR/PATCH changes
- **RDX-065**: Announce deprecations one MINOR version before removal
- **RDX-066**: schemaVersion MUST match published schema version

## 7. Use Case Requirements

### 7.1 Risk Information Sharing (V1.0)
- **RDX-067**: Enable sharing of product (item) definition metadata (UC_001_1)
- **RDX-068**: Support sharing of threat exposure information (UC_001_2)
- **RDX-069**: Allow sharing of impact and damage information (UC_001_3)

### 7.2 Security Testing Integration (V1.0)
- **RDX-070**: Enable use of risk information for test plan authoring (UC_002_1)
- **RDX-071**: Support correlation between security test reports and risk information (UC_002_2)

### 7.3 Managed Detection and Response (V1.0)
- **RDX-072**: Support log ingestion based on risk information (UC_003_1)
- **RDX-073**: Enable detection engineering using risk data (UC_003_2)
- **RDX-074**: Support behavioral analytics model development (UC_003_3)

### 7.4 Risk Management (V1.0)
- **RDX-075**: Enable whole vehicle TARA by combining existing TARAs (UC_004_1)
- **RDX-076**: Support standardized terms and formats for TARA integration

### 7.5 Future Enhancements (Open/V2.x)
- **RDX-077**: Consider persistent item definition visualization information
- **RDX-078**: Consider technology version enhancements (major/minor/patch)
- **RDX-079**: Consider data object enhancements (firmware/software flags, R/W capabilities)
- **RDX-080**: Consider assumption enhancements (responsible parties, risk split percentages)
- **RDX-081**: Consider control cost estimation fields
- **RDX-082**: Consider risk object enhancements (embedded impact/AFR levels)

## 8. Security Requirements

### 8.1 Security Policy
- **RDX-083**: Provide security vulnerability reporting mechanism
- **RDX-084**: Support email contact (security@asrg.io) or GitHub private advisory

## 9. Contribution Requirements

### 9.1 Development Workflow
- **RDX-085**: Support fork and feature branch workflow
- **RDX-086**: Require schema updates with corresponding examples
- **RDX-087**: Require validation before pull request submission
- **RDX-088**: Require clear PR descriptions with rationale

## 10. Implementation Requirements

### 10.1 Examples and Templates
- **RDX-089**: Provide example RDX documents in `examples/` directory
- **RDX-090**: Provide templates for RDX documents in `templates/` directory
- **RDX-091**: Include CycloneDX-embedded examples

### 10.2 Documentation
- **RDX-092**: Maintain methodology documentation
- **RDX-093**: Provide ISO/SAE 21434 mapping documentation
- **RDX-094**: Document use cases and stakeholder needs
- **RDX-095**: Maintain versioning and compatibility documentation

## 11. Tooling Requirements

### 11.1 Validation Tools
- **RDX-096**: Provide validation script for both JSON and XML formats
- **RDX-097**: Support ajv-cli for JSON Schema validation
- **RDX-098**: Support xmllint for XSD validation

## 12. Interoperability Requirements

### 12.1 CycloneDX Integration
- **RDX-099**: Ensure non-invasive integration with existing CycloneDX tooling
- **RDX-100**: Support embedding within CycloneDX BOMs without breaking compatibility

## 13. Requirements from Technical Committee Meetings

The following requirements were identified through ASRG TC: Risk Data Exchange meeting transcripts (2025-2026).

### 13.1 Tooling & Accessibility

- **RDX-101**: The RDX ecosystem MUST provide a freely accessible web-based viewer/reader application for RDX documents that allows stakeholders to inspect TARA data without requiring editing capabilities or tool licenses
- **RDX-102**: The RDX format MUST support linkage to SBOM (Software Bill of Materials) and HBOM (Hardware Bill of Materials) data to enable full supply chain traceability from component to risk assessment

### 13.2 Interoperability & Migration

- **RDX-103**: The RDX toolchain MUST provide bidirectional conversion support between RDX and legacy formats including OpenXSAM and Open Exam XML to enable migration of existing TARA data
- **RDX-104**: The RDX toolchain SHOULD support conversion from third-party TARA tool formats (e.g., ThreatGuard, Itemis) to RDX to reduce adoption friction for organizations with existing tooling
- **RDX-105**: The RDX format SHOULD support country of origin tracking for hardware and software components to enable compliance with regulatory requirements such as US Executive Orders on supply chain security

### 13.3 Regulatory & Standards Alignment

- **RDX-106**: The RDX format MUST define a future compatibility pathway for alignment with ISO 21482 and UNECE WP.29 R155/R156 cybersecurity regulations, to be addressed in a post-v1.0 release

### 13.4 Schema & Data Model Enhancements

- **RDX-107**: The RDX format MUST support a risk threshold matrix with configurable risk tolerance levels and threshold bands, enabling organizations to define acceptable vs. unacceptable risk levels per project or regulatory context (see GitHub issue #29)
- **RDX-108**: Attack path steps in RDX MUST be modelled as structured schema elements with dedicated fields (id, type, description, prerequisites) rather than plain strings, to enable machine-readable attack chain analysis (see GitHub issue #16)
- **RDX-109**: The RDX item definition MUST support system architecture information including hierarchical component structures, interfaces, communication channels, and trust boundaries to provide full item context within TARA documents (see GitHub issue #17)
- **RDX-110**: The RDX format MUST support SHA-512 hash values and digital signature capabilities for document integrity verification and non-repudiation of risk assessment data (see GitHub issue #8)
- **RDX-111**: The RDX JSON schema MUST set `additionalProperties: true` to allow tool-specific and organization-specific extensions without breaking schema validation, enabling ecosystem-wide extensibility (see GitHub issue #27)
- **RDX-112**: The RDX format MUST support Cybersecurity Management work products as defined in ISO/SAE 21434 Clause 9, including governance structures, organizational interfaces, and cybersecurity policy references within the TARA document context (see GitHub issue #28)
- **RDX-113**: The RDX format MUST support configurable risk level definitions within rating methodologies, allowing organizations to define their own named risk tiers (e.g., 3-level: Low/Medium/High, or 5-level: Very Low/Low/Medium/High/Very High, or any custom scale). Each level definition MUST include a unique identifier, human-readable label, and ordinal rank. Optional fields SHOULD include description, color code for visualization, score range mapping, and treatment guidance. Risk level definitions MUST be declared within the `methods` object (`riskLevels` array) so that the `band` fields in `riskValues`, `attackFeasibilityRatings`, and `impactRatings` can be interpreted against a formally declared scale (see GitHub issue #34)
