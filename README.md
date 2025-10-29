# Risk Data Exchange (RDX) — CycloneDX-based format for ISO/SAE 21434 TARA data

RDX is an open, vendor-neutral format for exchanging automotive cybersecurity risk data (TARA) across tools and organizations.
It is **based on CycloneDX** for packaging and transport and provides **JSON** and **XML** schemas for structured risk data.

- **Goals**
  - Cover core ISO/SAE 21434 risk work products (Clause 15) and related lifecycle outputs
  - Interoperate with existing SBOM/BOM ecosystems (CycloneDX JSON & XML)
  - Strict schemas, versioning, and conformance levels
  - First-class **data quality & governance** (identity, provenance, validation, traceability)

- **Dual encoding**
  1. **JSON**: `rdx.schema.json` — embeddable in CycloneDX using `metadata.properties`
  2. **XML**: `rdx.xsd` — embeddable in CycloneDX via `rdx:` namespace

See `methodology/Methodology.md` for design, ISO mapping, versioning, and governance.

##Claude GitHub Workflows

This repository uses three Anthropic Claude-powered GitHub Actions to automate reviews and issue handling.
Each workflow runs independently to avoid overlap and race conditions.

###.github/workflows/claude-issues.yml	
Handles issue management. When a new issue (task) is created or updated, Claude reviews the content, refines titles/descriptions, adds labels, and suggests next steps — ensuring consistent structure and clarity across all tasks.	
Trigger: issues (opened / edited / reopened / assigned) and issue_comment

###.github/workflows/claude-pr-review.yml	
Performs automatic PR reviews. Claude reviews every pull request when opened or updated, providing concise feedback on code quality, potential risks, and alignment with project standards.	
Trigger: pull_request (opened / synchronize / reopened / ready_for_review)

###.github/workflows/claude-pr-apply.yml	
Supports manual application of AI-suggested fixes. When a maintainer comments @claude apply or adds the claude-apply label, Claude safely implements targeted code updates based on review feedback.	
Trigger: issue_comment, pull_request (labeled), or workflow_dispatch

Each workflow automatically skips actions triggered by bots (e.g., claude[bot]) to prevent feedback loops and runs under isolated concurrency groups to ensure predictable, conflict-free automation.
