# ISO/SAE Standards Mapping (informational)

## ISO/SAE 21434 Mapping
| Work Product | Clause | RDX Object | Notes |
|---|---|---|---|
| Item definition | 9.2 / WP-09-01 | `riskSet.itemDefinition` | Boundary, functions, architecture, environment |
| Cybersecurity goals | 9.3 / WP-09-02 | `riskSet.cybersecurityGoals[]` | Goals linked to threat/damage scenarios and risk values |
| Cybersecurity concept | 9.4 / WP-09-03 | `riskSet.cybersecurityConcept[]` | Design decisions and architectural choices per goal |
| Cybersecurity requirements | 9.4 / WP-09-03 | `riskSet.cybersecurityRequirements[]` | Requirements derived from goals with allocation and verification |
| Cybersecurity claims | 9.3–9.4 | `riskSet.cybersecurityClaims[]` | Assertions that security properties are achieved (with evidence) |
| Damage scenarios | 15.5 / WP-15-01 | `riskSet.damageScenarios[]` | Adverse consequences |
| Assets (CIA) | 15.4 / WP-15-02 | `riskSet.assets[]` | CIA properties + linkage |
| Threat scenarios | 15.5 / WP-15-03 | `riskSet.threatScenarios[]` | Targeted assets + properties + cause |
| Attack paths | 15.6 / WP-15-05 | `riskSet.attackPaths[]` | Steps referencing components/services |
| AFR | 15.7 / WP-15-06 | `riskSet.attackFeasibilityRatings[]` | Method IDs + factors |
| Impact rating | 15.5 / WP-15-04 | `riskSet.impactRatings[]` | Categories + rationale |
| Risk values | 15.8 / WP-15-07 | `riskSet.riskValues[]` | AFR + Impact linkage |
| Treatment decisions | 15.9 / WP-15-08 | `riskSet.riskTreatmentDecisions[]` | Decision + controls + justification |

## ISO/SAE PAS 8475 Mapping  
| Framework Component | RDX Object | Notes |
|---|---|---|
| Cybersecurity Assurance Levels (CAL) | `riskSet.calAssuranceLevels[]` | CAL1-CAL4 definitions with objectives and activities |
| CAL Assessment Evidence | `riskSet.calAssessments[]` | Assessment results and achieved assurance levels |
| Enhanced Controls | `riskSet.controls[]` | Extended with requiredCalLevel and achievedCalLevel |
| Targeted Attack Feasibility (TAF) | `riskSet.tafAssessments[]` | Context-aware feasibility with attacker profiling |
| CAL Relationships | `riskSet.relationships[]` | requires_cal and achieves_cal relationship types |
