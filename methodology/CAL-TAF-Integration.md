# CAL and TAF Framework Integration in RDX

This document describes how ISO/SAE PAS 8475 Cybersecurity Assurance Levels (CAL) and Targeted Attack Feasibility (TAF) frameworks are integrated into the RDX format.

## Overview

ISO/SAE PAS 8475 provides enhanced frameworks for cybersecurity assessment in automotive systems:

- **CAL (Cybersecurity Assurance Levels)**: Defines structured assurance requirements for cybersecurity measures
- **TAF (Targeted Attack Feasibility)**: Provides enhanced attack feasibility assessment considering attacker profiles and motivations

## CAL Framework Integration

### Cybersecurity Assurance Levels

CAL defines four levels of cybersecurity assurance (CAL1-CAL4), with increasing rigor:

- **CAL1**: Basic assurance with standard verification activities
- **CAL2**: Systematic assurance with structured testing and review  
- **CAL3**: High assurance with independent assessment and vulnerability testing
- **CAL4**: Very high assurance with formal verification and mathematical proof

### RDX CAL Objects

#### calAssuranceLevels
Defines the specific assurance level requirements and activities.

```json
{
  "calAssuranceLevels": [
    {
      "id": "CAL-3",
      "level": "CAL3",
      "title": "Cybersecurity Assurance Level 3",
      "objectives": [
        "Systematic verification of cybersecurity measures",
        "Independent assessment of implementation"
      ],
      "assuranceActivities": [
        "Code review by independent team",
        "Penetration testing by certified team"
      ]
    }
  ]
}
```

#### calAssessments
Records the assessment of controls against CAL requirements.

```json
{
  "calAssessments": [
    {
      "id": "CAL-ASSESS-001",
      "controlId": "CTRL-AUTH-001",
      "targetCalLevel": "CAL3",
      "assessmentResult": "sufficient",
      "achievedCalLevel": "CAL3",
      "assessor": "Independent Security Assessment Team"
    }
  ]
}
```

#### Enhanced controls
Controls can now specify required and achieved CAL levels:

```json
{
  "controls": [
    {
      "id": "CTRL-AUTH-001", 
      "title": "Multi-factor Authentication",
      "requiredCalLevel": "CAL3",
      "achievedCalLevel": "CAL2"
    }
  ]
}
```

## TAF Framework Integration

### Targeted Attack Feasibility

TAF enhances traditional attack feasibility assessment by considering:

- **Attacker Profile**: Nation-state, organized crime, hacktivist, insider, opportunist
- **Attack Motivation**: Financial, espionage, disruption, reputation, other
- **Target Value**: Assessment of asset value to different attacker types
- **Access Requirements**: Remote, adjacent, physical, or insider access needed

### RDX TAF Objects

#### tafAssessments
Provides targeted attack feasibility assessment with contextual factors.

```json
{
  "tafAssessments": [
    {
      "id": "TAF-AP-001",
      "attackPathId": "AP-V2X-1", 
      "methodId": "iso-pas-8475-taf-v1",
      "targetContext": {
        "attackerProfile": "nation-state",
        "attackMotivation": "disruption",
        "targetValue": "very-high",
        "accessRequirement": "adjacent"
      },
      "tafScore": "4.2",
      "tafBand": "high",
      "rationale": "Nation-state actor with high resources targeting critical infrastructure"
    }
  ]
}
```

## Usage Patterns

### CAL Integration Workflow

1. **Define Assurance Levels**: Create `calAssuranceLevels` objects for relevant CAL levels
2. **Specify Requirements**: Set `requiredCalLevel` on security controls  
3. **Conduct Assessments**: Perform CAL assessments and record in `calAssessments`
4. **Track Achievement**: Update `achievedCalLevel` on controls based on assessments
5. **Establish Relationships**: Use `requires_cal` and `achieves_cal` relationship types

### TAF Integration Workflow

1. **Context Analysis**: Identify likely attacker profiles and motivations for each threat
2. **TAF Assessment**: Conduct targeted feasibility assessment using `tafAssessments`
3. **Comparative Analysis**: Compare standard AFR with TAF results for different threat actors
4. **Risk Treatment**: Adjust risk treatment decisions based on targeted threat analysis

## Integration with ISO/SAE 21434

The CAL and TAF frameworks complement existing ISO/SAE 21434 processes:

- **CAL** enhances control assurance beyond basic implementation verification
- **TAF** provides context-aware feasibility assessment for more accurate risk calculation
- **Traceability** maintained through existing relationship and reference mechanisms
- **Backward Compatibility** ensured - all existing RDX objects remain valid

## Examples

See `examples/rdx-cal-taf-example.json` for a comprehensive example demonstrating:
- Autonomous vehicle control unit risk assessment
- CAL3/CAL4 assurance level definitions and assessments  
- TAF assessments for nation-state and organized crime threat actors
- Integration of CAL requirements with security controls
- Enhanced relationships showing assurance level dependencies

## Benefits

1. **Enhanced Assurance**: Structured approach to cybersecurity assurance levels
2. **Targeted Risk Assessment**: Context-aware attack feasibility considering realistic threat actors
3. **Regulatory Alignment**: Support for emerging automotive cybersecurity regulations
4. **Tool Interoperability**: Standardized exchange of assurance and feasibility data
5. **Decision Support**: Better informed risk treatment decisions based on threat context