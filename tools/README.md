# RDX to OpenXSAM Converter

A Python command-line tool that converts Risk Data Exchange (RDX) format to OpenXSAM format for automotive cybersecurity threat assessment and risk analysis (TARA) data exchange.

## Overview

This converter transforms RDX data (both standalone and CycloneDX-embedded formats) into OpenXSAM XML format, enabling interoperability between different TARA tools and workflows.

## Features

- **Multi-format input support**: 
  - Standalone RDX JSON files
  - CycloneDX BOMs with embedded RDX data
- **Comprehensive mapping**: Converts all major RDX components to OpenXSAM equivalents
- **Standards-compliant**: Generates OpenXSAM XML following typical OSAM structure patterns
- **Command-line interface**: Easy integration into automation workflows

## Installation

No additional dependencies required - uses Python standard library only.

Requirements:
- Python 3.7 or higher

## Usage

### Basic Usage

```bash
# Convert standalone RDX file
python rdx_to_openxsam.py rdx-example.json

# Convert CycloneDX with embedded RDX
python rdx_to_openxsam.py cyclonedx-embedded.json

# Specify output file
python rdx_to_openxsam.py input.json output.openxsam.xml
```

### Command Options

```bash
python rdx_to_openxsam.py [-h] [--validate] [--verbose] input_file [output_file]

positional arguments:
  input_file     Input RDX or CycloneDX file
  output_file    Output OpenXSAM file (optional)

optional arguments:
  -h, --help     Show help message
  --validate     Validate input file format before conversion
  --verbose, -v  Enable verbose output
```

### Examples

```bash
# Validate and convert with verbose output
python rdx_to_openxsam.py rdx-example.json --validate --verbose

# Convert CycloneDX embedded format
python rdx_to_openxsam.py cyclonedx-embedded.json tara-export.openxsam.xml

# Quick validation
python rdx_to_openxsam.py my-tara.json --validate
```

## Format Mapping

The converter maps RDX components to OpenXSAM elements as follows:

| RDX Component | OpenXSAM Element | Description |
|---------------|------------------|-------------|
| `documentId` | `Header/DocumentInformation/DocumentId` | Document identifier |
| `created` | `Header/DocumentInformation/DocumentDate` | Creation timestamp |
| `createdBy` | `Header/DocumentInformation/CreatedBy` | Creator information |
| `itemDefinition` | `ItemDefinition` | System/component being assessed |
| `assets` | `Assets/Asset` | Things to protect (CIA properties) |
| `damageScenarios` | `DamageScenarios/DamageScenario` | Potential harm scenarios |
| `threatScenarios` | `ThreatScenarios/ThreatScenario` | Security threats |
| `attackPaths` | `AttackPaths/AttackPath` | Attack realization methods |
| `attackFeasibilityRatings` | `RiskAssessments/RiskAssessment` | Likelihood assessments |
| `impactRatings` | `RiskAssessments/RiskAssessment` | Consequence assessments |
| `riskValues` | `RiskAssessments/RiskAssessment` | Combined risk scores |
| `controls` | `SecurityControls/SecurityControl` | Security measures |
| `riskTreatmentDecisions` | `RiskTreatment/TreatmentDecision` | Risk handling decisions |

## Input Formats

### Standalone RDX JSON
```json
{
  "schemaVersion": "0.1.0",
  "documentId": "uuid",
  "riskSet": {
    "itemDefinition": { ... },
    "assets": [ ... ],
    "threatScenarios": [ ... ]
  }
}
```

### CycloneDX Embedded RDX
```json
{
  "bomFormat": "CycloneDX",
  "metadata": {
    "properties": [
      {
        "name": "https://asrg.io/ns/rdx#document",
        "value": "{\"schemaVersion\":\"0.1.0\", ...}"
      }
    ]
  }
}
```

## Output Format

The converter generates OpenXSAM XML with the following structure:

```xml
<OpenXSAM xmlns="http://www.itemis.com/openxsam/v1.0" version="1.0">
  <Header>
    <DocumentInformation>...</DocumentInformation>
    <ToolInformation>...</ToolInformation>
  </Header>
  <ItemDefinition id="...">...</ItemDefinition>
  <Assets>...</Assets>
  <DamageScenarios>...</DamageScenarios>
  <ThreatScenarios>...</ThreatScenarios>
  <AttackPaths>...</AttackPaths>
  <RiskAssessments>...</RiskAssessments>
  <SecurityControls>...</SecurityControls>
  <RiskTreatment>...</RiskTreatment>
</OpenXSAM>
```

## Error Handling

The converter includes comprehensive error handling:

- **File validation**: Checks for file existence and readability
- **Format detection**: Automatically detects RDX vs CycloneDX input
- **Schema validation**: Validates required RDX fields
- **Error reporting**: Clear error messages with context

Common error scenarios:
- Missing input file
- Invalid JSON format
- Missing RDX data in CycloneDX
- Unrecognized input format

## Testing

Test the converter with provided examples:

```bash
# Test with example files
python test_converter.py

# Manual testing
python rdx_to_openxsam.py ../examples/rdx-example.json
python rdx_to_openxsam.py ../examples/cyclonedx-embedded.json
```

## Integration

The converter can be integrated into CI/CD pipelines and automation workflows:

```bash
# Example automation script
for rdx_file in *.json; do
    python rdx_to_openxsam.py "$rdx_file" --validate --verbose
done
```

## Limitations

- OpenXSAM specification interpretation based on typical OSAM patterns
- Limited to fields defined in RDX schema v0.1.0
- XML namespace assumes Itemis OpenXSAM v1.0 structure

## Contributing

This converter is part of the RDX project. See the main project documentation for contribution guidelines.

## License

Same as the RDX project license.