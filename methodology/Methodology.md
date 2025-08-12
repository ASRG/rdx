# RDX Methodology
RDX provides interoperable objects for Threat Analysis and Risk Assessment (TARA) aligned to ISO/SAE 21434.
RDX can travel inside a CycloneDX BOM or as a standalone document.

## Design principles
- Based on CycloneDX (transport, signing, linking/BOM-Link, tooling)
- Data quality & governance: identities, provenance, validation, vocabularies
- Compatibility: non-invasive to CycloneDX consumers; profiles for producers/consumers
- Open governance: public repo, SemVer, deprecations, CI validation

## Object model (minimums in **bold**)
- **itemDefinition** (**id**, **title**, boundary, functions, architecture, interfaces, environment, assumptions)
- **assets**: (**id**, **title**, properties[C|I|A], linkedDamageScenarioIds, externalIds?)
- **damageScenarios**: (**id**, **title**, description, impactedFunctions, affectedRoadUsers, references)
- **threatScenarios**: (**id**, **title**, targetedAssetIds[], compromisedProperties[], cause, references)
- **attackPaths**: (**id**, **title**, threatScenarioId, steps[], references)
- **attackFeasibilityRatings**: (**id**, attackPathId, methodId, inputFactors, score, band?, rationale?)
- **impactRatings**: (**id**, damageScenarioId, methodId, categories, score, rationale?)
- **riskValues**: (**id**, threatScenarioId, afrRef, impactRef, methodId, score, band?, rationale?)
- **controls**: (**id**, title, catalog?, controlId?, implementationStatus?, references?)
- **riskTreatmentDecisions**: (**id**, riskValueId, decision[treat|avoid|accept|share], controls[], justification)

## Encoding patterns
- CycloneDX JSON: embed minified RDX JSON in `metadata.properties`
- CycloneDX XML: embed `<rdx:...>` under `<bom>`
- Standalone RDX: JSON or XML media types (proposed)

## Data quality & governance
- Required minimums; controlled vocabularies; validation & CI; provenance; integrity/signing; versioning.
