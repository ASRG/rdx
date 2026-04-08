# RDX Methodology
RDX provides interoperable objects for Threat Analysis and Risk Assessment (TARA) aligned to ISO/SAE 21434 and enhanced with ISO/SAE PAS 8475 CAL and TAF frameworks.
RDX can travel inside a CycloneDX BOM or as a standalone document.

## Design principles
- Based on CycloneDX (transport, signing, linking/BOM-Link, tooling)
- Data quality & governance: identities, provenance, validation, vocabularies
- Compatibility: non-invasive to CycloneDX consumers; profiles for producers/consumers
- Open governance: public repo, SemVer, deprecations, CI validation

## Object model (minimums in **bold**)

### Core Risk Assessment Objects
- **itemDefinition** (**id**, **title**, boundary, functions, architecture, interfaces, environment, assumptions)
- **assets**: (**id**, **title**, properties[C|I|A], linkedDamageScenarioIds, externalIds?)
- **damageScenarios**: (**id**, **title**, description, impactedFunctions, affectedRoadUsers, references)
- **threatScenarios**: (**id**, **title**, targetedAssetIds[], compromisedProperties[], cause, references)
- **attackPaths**: (**id**, **title**, threatScenarioId, steps[], references)
- **attackSteps**: (**id**, **title**, description?, attackFeasibilityRatings[], controlIds[], references?) — steps with embedded feasibility ratings
- **attackFeasibilityRatings** (embedded in attackStep): (methodId, inputFactors{elapsedTime, expertise, knowledge, windowOfOpportunity, equipment}, score, band?, rationale?) — no id required
- **attackFeasibilityRatings** (top-level, path-level): (**id**, **attackPathId**, **methodId**, **score**, inputFactors, band?, rationale?) — used for riskValues.afrRef
- **impactRatings**: (**id**, damageScenarioId, methodId, categories, score, rationale?)
- **riskValues**: (**id**, threatScenarioId, afrRef, impactRef, methodId, score, band?, rationale?)
- **controls**: (**id**, title, catalog?, controlId?, implementationStatus?, requiredCalLevel?, achievedCalLevel?, references?)
- **riskTreatmentDecisions**: (**id**, riskValueId, decision[treat|avoid|accept|share], controls[], justification)

### Relationships
- **relationships**: (**id**, **relationshipType**, **sourceRef**, **targetRef**, confidence?, justification?)
  - Standard types: causes, mitigates, implements, assesses, contains, targets, threatens, protects, related_to
  - CAL-specific types: requires_cal (control requires CAL level), achieves_cal (assessment achieves CAL level)

### CAL (Cybersecurity Assurance Levels) Framework - ISO/SAE PAS 8475
- **calAssuranceLevels**: (**id**, **level**[CAL1-4], **objectives**[], title?, description?, assuranceActivities?, references?)
- **calAssessments**: (**id**, **controlId**, **targetCalLevel**, **assessmentResult**[sufficient|insufficient|pending], achievedCalLevel?, evidenceRef?, assessmentDate?, assessor?, rationale?)

### TAF (Targeted Attack Feasibility) Framework - ISO/SAE PAS 8475  
- **tafAssessments**: (**id**, **attackPathId**, **methodId**, **tafScore**, targetContext?, tafBand?, factorRatings?, rationale?, assessmentDate?)

## Encoding patterns
- CycloneDX JSON: embed minified RDX JSON in `metadata.properties`
- CycloneDX XML: embed `<rdx:...>` under `<bom>`
- Standalone RDX: JSON or XML media types (proposed)

## Data quality & governance
- Required minimums; controlled vocabularies; validation & CI; provenance; integrity/signing; versioning.
