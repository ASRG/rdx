# OpenXSAM v1.1 Gap Analysis vs. Risk Data Exchange (RDX)

## Overview

This document provides a gap analysis comparing the Risk Data Exchange (RDX) schema against the OpenXSAM (Open Extensible Security Architecture Model) v1.1 specification. OpenXSAM is an XML-based exchange format developed by Itemis for sharing TARA (Threat Analysis and Risk Assessment) artifacts aligned with ISO/SAE 21434.

## RDX Schema Summary

RDX is a JSON/XML-based format for exchanging cybersecurity risk data. Its core elements include:

| Element | Description |
|---|---|
| `itemDefinition` | The item under analysis (boundary, functions, architecture, interfaces) |
| `assets` | Security-relevant assets with CIA properties |
| `damageScenarios` | Adverse consequences if assets are compromised |
| `threatScenarios` | Threats to assets with damage scenario links |
| `attackSteps` | Individual steps in an attack chain |
| `attackPaths` | Ordered sequences of attack steps |
| `methods` | Feasibility and impact rating methods |
| `attackFeasibilityRatings` | Ratings per attack step/path |
| `impactRatings` | Damage scenario impact ratings |
| `riskValues` | Combined risk scores from feasibility and impact |
| `controls` | Security controls and countermeasures |
| `calAssuranceLevels` | Cybersecurity Assurance Level (CAL) ratings |
| `mitigationRelationships` | Relationships between controls and threats |

## OpenXSAM v1.1 Schema Summary

OpenXSAM structures a security analysis around these core elements:

| Element | Description |
|---|---|
| `System` | The system under analysis with properties and sub-systems |
| `Component` | Hardware/software components with type, interfaces, and parent/child hierarchy |
| `Asset` | Security assets with STRIDE-based property classification |
| `Threat` | Threats mapped to STRIDE categories |
| `AttackPath` | Detailed attack paths with prerequisite and likelihood fields |
| `DamageScenario` | Operational and safety damage with severity classification |
| `RiskValue` | Risk matrix combining likelihood and impact |
| `Control` | Mitigations including status (proposed/implemented/verified) |
| `SecurityGoal` | High-level cybersecurity goals derived from damage scenarios |
| `CybersecurityClaim` | Formal claim linking security goal to a control |
| `EvidenceReference` | References to external evidence documents |
| `AnalysisScope` | Scope boundary definitions for the analysis |
| `Assumption` | Documented assumptions for the analysis |
| `ExclusionReason` | Documented reasons for excluding elements from scope |
| `ReviewRecord` | Formal review and approval records |
| `VersionHistory` | Document version and change tracking |

## Gap Analysis

### Elements Present in OpenXSAM but Missing or Underdeveloped in RDX

| Gap | OpenXSAM Element | RDX Status | Priority |
|---|---|---|---|
| Structured component hierarchy | `Component` with type, parentId, interfaces | RDX has `architecture` as a plain string | High |
| Security goals | `SecurityGoal` linked to damage scenarios | Not present in RDX | High |
| Cybersecurity claims | `CybersecurityClaim` linking goals to controls | Not present in RDX | Medium |
| Control implementation status | `Control.status` (proposed/implemented/verified) | RDX controls lack status tracking | Medium |
| STRIDE classification | `Asset` STRIDE properties, `Threat` STRIDE category | RDX assets have CIA but not STRIDE | Medium |
| Hash/integrity support | `Component.hash`, `Asset.hash` | No hash fields in RDX | Medium |
| Evidence references | `EvidenceReference` | Not present in RDX | Low |
| Formal review records | `ReviewRecord` | Not present in RDX | Low |
| Version history | `VersionHistory` | Not present in RDX | Low |
| Analysis scope definition | `AnalysisScope` | RDX has `boundary` string but no formal scope | Low |
| Exclusion documentation | `ExclusionReason` | Not present in RDX | Low |

### Elements Present in RDX but Not in OpenXSAM

| RDX Element | Description | Benefit |
|---|---|---|
| `calAssuranceLevels` | ISO/SAE PAS 8475 CAL ratings | Formal assurance tracking not in OpenXSAM v1.1 |
| `attackFeasibilityRatings` | Granular AFR per attack step | More detailed than OpenXSAM likelihood field |
| `bomRefRef` | CycloneDX BOM reference | Links to software bill of materials |
| `methods` | Configurable rating methods | OpenXSAM uses fixed rating scales |

## Recommended Additions to RDX

### 1. Structured Component Hierarchy (High Priority)
Add a `components` array to `itemDefinition` supporting hierarchical elements:
```json
"components": [
  {
    "id": "COMP-001",
    "name": "Gateway ECU",
    "type": "hardware",
    "parentId": null,
    "description": "Main gateway processor"
  },
  {
    "id": "COMP-002",
    "name": "AutoSAR Runtime",
    "type": "software",
    "parentId": "COMP-001",
    "description": "AUTOSAR Classic OS"
  }
]
```
**Benefit:** Enables precise linking of threats, assets, and controls to specific components. Enables automated tool integration (e.g., model-based TARA).

### 2. Security Goals (High Priority)
Add a `securityGoals` array linking damage scenarios to formal objectives:
```json
"securityGoals": [
  {
    "id": "SG-001",
    "title": "Protect vehicle control integrity",
    "damageScenarioId": "DS-SAF-1",
    "description": "Prevent unauthorized modification of safety-critical actuator commands"
  }
]
```
**Benefit:** Aligns RDX with ISO/SAE 21434 clause 15 (cybersecurity goals) and enables traceability from risk to requirement.

### 3. Cybersecurity Claims (Medium Priority)
Add a `cybersecurityClaims` array linking security goals to controls:
```json
"cybersecurityClaims": [
  {
    "id": "CC-001",
    "securityGoalId": "SG-001",
    "controlId": "CTRL-MSG-1",
    "rationale": "Message authentication prevents spoofing attacks on CAN bus"
  }
]
```
**Benefit:** Provides a formal argumentation structure for cybersecurity cases and audits.

### 4. Control Implementation Status (Medium Priority)
Add `status` field to controls:
```json
{
  "id": "CTRL-MSG-1",
  "title": "CAN message authentication",
  "status": "implemented",
  "verificationMethod": "penetration-test",
  "verificationDate": "2025-11-01"
}
```
**Benefit:** Enables tracking of control lifecycle from proposal through verification; required for ISO/SAE 21434 clause 16 compliance.

### 5. STRIDE Classification (Medium Priority)
Add `stride` property to assets and threat scenarios:
```json
{
  "id": "AS-001",
  "title": "Vehicle Control Data",
  "stride": ["tampering", "repudiation"]
}
```
**Benefit:** Aligns with widely-used threat modeling methodology; enables automated threat generation from STRIDE analysis.

### 6. Hash/Integrity Support (Medium Priority)
Add `hashes` array to components and assets:
```json
"hashes": [
  {"alg": "SHA-256", "content": "a3f1..."},
  {"alg": "SHA-512", "content": "b7e2..."}
]
```
**Benefit:** Enables verification of artifact integrity; aligns with CycloneDX BOM format and supply chain security requirements.

## Conclusion

RDX and OpenXSAM address overlapping but complementary aspects of TARA exchange. The most impactful additions to RDX would be:

1. **Structured component hierarchy** — essential for tool interoperability and linking analysis elements to architectural elements
2. **Security goals and claims** — needed for ISO/SAE 21434 traceability requirements
3. **Control status tracking** — enables lifecycle management of security measures
4. **STRIDE classification** — improves interoperability with existing threat modeling tools
5. **Hash support** — addresses supply chain and data integrity requirements

These additions would significantly improve RDX's completeness as an automotive cybersecurity exchange format and bring it into closer alignment with both OpenXSAM and ISO/SAE 21434 requirements.

## References

- OpenXSAM Specification v1.1 (Itemis AG)
- ISO/SAE 21434:2021 — Road Vehicles: Cybersecurity Engineering
- ISO/SAE PAS 8475:2025 — Cybersecurity Assurance Levels
- CycloneDX v1.6 — Software Bill of Materials Standard
