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
