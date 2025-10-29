# Risk Data Exchange (RDX) — CycloneDX-based format for ISO/SAE 21434 TARA data

RDX is an open, vendor-neutral format for exchanging automotive cybersecurity risk data (TARA) across tools and organizations.
It is **based on CycloneDX** for packaging and transport and provides **JSON** and **XML** schemas for structured risk data.

## Goals

- Cover core ISO/SAE 21434 risk work products (Clause 15) and related lifecycle outputs
- Support ISO/SAE PAS 8475 CAL (Cybersecurity Assurance Levels) and TAF (Targeted Attack Feasibility) frameworks
- Interoperate with existing SBOM/BOM ecosystems (CycloneDX JSON & XML)
- Strict schemas, versioning, and conformance levels
- First-class **data quality & governance** (identity, provenance, validation, traceability)

## Dual Encoding

1. **JSON**: `spec/json/rdx.schema.json` — JSON Schema Draft 2020-12, embeddable in CycloneDX using `metadata.properties`
2. **XML**: `spec/xml/rdx.xsd` — XML Schema Definition, embeddable in CycloneDX via `rdx:` namespace

## Key Features

### Core Risk Objects
- **Item Definition**: System/component being assessed with boundary, functions, architecture
- **Assets**: Protected assets with CIA (Confidentiality, Integrity, Availability) properties
- **Damage Scenarios**: Potential harm scenarios with impact assessment
- **Threat Scenarios**: Security threats targeting specific assets
- **Attack Paths**: Detailed attack step sequences
- **Risk Ratings**: Attack feasibility, impact, and combined risk values
- **Controls**: Security measures with implementation status
- **Risk Treatment Decisions**: Documented risk handling (treat/avoid/accept/share)

### Advanced Features (v0.1.0+)
- **Explicit Relationships**: Machine-readable links between risk artifacts (causes, mitigates, implements, etc.)
- **CAL Framework**: ISO/SAE PAS 8475 Cybersecurity Assurance Levels (CAL1-4) with assessment tracking
- **TAF Framework**: Targeted Attack Feasibility assessments with attacker profiling
- **Methods**: Support for multiple rating methodologies
- **Country of Origin**: Supply chain transparency for item definitions
- **Traceability**: All objects require unique IDs with support for external references

## Quick Start

### Prerequisites
```bash
npm install -g ajv-cli  # For JSON validation
# xmllint typically pre-installed on macOS/Linux
```

### Validation
Run all validations:
```bash
./tools/validate.sh
```

Validate individual examples:
```bash
ajv -s spec/json/rdx.schema.json -d examples/rdx-example.json --strict=false
```

**Note**: The schema uses JSON Schema Draft 2020-12. Current `ajv-cli` versions support up to Draft 2019-09, which may cause schema reference warnings. All examples are valid JSON and conform to required fields.

## Examples

- **`rdx-example.json`**: Basic standalone RDX document
- **`rdx-relationships-example.json`**: Explicit relationships between risk objects
- **`rdx-multiple-threats-example.json`**: Multiple threat scenarios
- **`rdx-mitigation-relationships-example.json`**: Controls mitigating threats
- **`rdx-cal-taf-example.json`**: CAL and TAF framework integration
- **`headlight-tara-iso21434.json`**: Complete ISO 21434 TARA for Adaptive Front-lighting System
- **`cyclonedx-embedded.json/.xml`**: RDX embedded within CycloneDX BOMs

## Documentation

- **[Methodology](methodology/Methodology.md)**: Design principles, object model, encoding patterns
- **[ISO 21434 Mapping](methodology/ISO21434-Mapping.md)**: Clause mappings to ISO/SAE 21434
- **[CAL/TAF Integration](methodology/CAL-TAF-Integration.md)**: ISO/SAE PAS 8475 framework details
- **[Use Cases](methodology/UseCases.md)**: Usage scenarios and examples
- **[Requirements](REQUIREMENTS.md)**: Formal requirements tracking (RDX-XXX format)
- **[Contributing](CONTRIBUTING.md)**: Contribution process and requirements
- **[Versioning](VERSIONING.md)**: Semantic versioning policy

## Claude GitHub Workflows

This repository uses three Anthropic Claude-powered GitHub Actions to automate reviews and issue handling. Each workflow runs independently to avoid overlap and race conditions.

### `.github/workflows/claude-issues.yml`
Handles issue management. When a new issue is created or updated, Claude reviews the content, refines titles/descriptions, adds labels, and suggests next steps — ensuring consistent structure and clarity across all tasks.

**Triggers**: `issues` (opened/edited/reopened/assigned), `issue_comment`

### `.github/workflows/claude-pr-review.yml`
Performs automatic PR reviews. Claude reviews every pull request when opened or updated, providing concise feedback on code quality, potential risks, and alignment with project standards including ISO/SAE 21434 compliance.

**Triggers**: `pull_request` (opened/synchronize/reopened/ready_for_review)

### `.github/workflows/claude-pr-apply.yml`
Supports manual application of AI-suggested fixes. When a maintainer comments `@claude apply` or adds the `claude-apply` label, Claude safely implements targeted code updates based on review feedback.

**Triggers**: `issue_comment`, `pull_request` (labeled), `workflow_dispatch`

Each workflow automatically skips actions triggered by bots (e.g., `claude[bot]`) to prevent feedback loops and runs under isolated concurrency groups to ensure predictable, conflict-free automation.

## Project Status

**Current Version**: v0.1.0
**Status**: Active Development
**Schema Specification**: JSON Schema Draft 2020-12

Recent enhancements:
- ✅ Explicit relationship support (Issues #1, #4)
- ✅ Country of origin tracking (Issue #10)
- ✅ ISO/SAE PAS 8475 CAL/TAF framework integration (Issue #9)
- ✅ Complete headlight TARA example (Issue #12)

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development workflow and requirements process
- GitHub issue requirements (all changes must have associated issues)
- Code standards and testing requirements
- How to interact with Claude AI automation

## Community & Support

- **Issues**: [GitHub Issues](https://github.com/ASRG/rdx/issues)
- **Discussions**: Use issue comments or create new issues for questions
- **AI Assistance**: Mention `@claude` in issues or PRs for automated help

## License

Please refer to the repository license file for licensing information.
