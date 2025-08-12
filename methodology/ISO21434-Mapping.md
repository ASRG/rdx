# ISO/SAE 21434 Mapping (informational)
| Work Product | Clause | RDX Object | Notes |
|---|---|---|---|
| Item definition | 9.3 / WP-09-01 | `riskSet.itemDefinition` | Boundary, functions, architecture, environment |
| Damage scenarios | 15.5 / WP-15-01 | `riskSet.damageScenarios[]` | Adverse consequences |
| Assets (CIA) | 15.4 / WP-15-02 | `riskSet.assets[]` | CIA properties + linkage |
| Threat scenarios | 15.5 / WP-15-03 | `riskSet.threatScenarios[]` | Targeted assets + properties + cause |
| Attack paths | 15.6 / WP-15-05 | `riskSet.attackPaths[]` | Steps referencing components/services |
| AFR | 15.7 / WP-15-06 | `riskSet.attackFeasibilityRatings[]` | Method IDs + factors |
| Impact rating | 15.5 / WP-15-04 | `riskSet.impactRatings[]` | Categories + rationale |
| Risk values | 15.8 / WP-15-07 | `riskSet.riskValues[]` | AFR + Impact linkage |
| Treatment decisions | 15.9 / WP-15-08 | `riskSet.riskTreatmentDecisions[]` | Decision + controls + justification |
