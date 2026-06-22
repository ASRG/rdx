#!/usr/bin/env bash
set -euo pipefail

# RDX validation
# - JSON Schema validation requires 'ajv' + 'ajv-formats' (npm i -g ajv-cli ajv-formats)
# - XML validation requires 'xmllint' (typically pre-installed on macOS/Linux)
#
# The RDX JSON Schema uses JSON Schema Draft 2020-12, so ajv must be invoked
# with --spec=draft2020 and the ajv-formats plugin (-c ajv-formats).

cd "$(dirname "$0")/.."

SCHEMA="spec/json/rdx.schema.json"
XSD="spec/xml/rdx.xsd"
AJV_FLAGS="--spec=draft2020 -c ajv-formats --strict=false"

# Standalone RDX JSON documents (root = RDX document). Each must validate
# against the schema. The cyclonedx-embedded.* files are CycloneDX BOMs that
# *embed* RDX and are checked separately (well-formedness only).
JSON_DOCS=(
  examples/rdx-example.json
  examples/rdx-relationships-example.json
  examples/rdx-multiple-threats-example.json
  examples/rdx-mitigation-relationships-example.json
  examples/rdx-cal-taf-example.json
  examples/rdx-risk-threshold-example.json
  examples/rdx-infotainment-comprehensive-example.json
  examples/headlight-tara-iso21434.json
  templates/rdx-template.json
)

echo "==> Validating JSON documents against $SCHEMA"
for doc in "${JSON_DOCS[@]}"; do
  echo "  - $doc"
  # shellcheck disable=SC2086
  ajv validate -s "$SCHEMA" -d "$doc" $AJV_FLAGS
done

echo "==> Checking CycloneDX-embedded JSON is well-formed"
node -e "JSON.parse(require('fs').readFileSync('examples/cyclonedx-embedded.json','utf8'))" \
  && echo "  - examples/cyclonedx-embedded.json: well-formed"

echo "==> Validating standalone XML against $XSD"
xmllint --noout --schema "$XSD" templates/rdx-template.xml

echo "==> Checking CycloneDX-embedded XML is well-formed"
# NOTE: cyclonedx-embedded.xml is a CycloneDX BOM (root element <bom>) with
# embedded rdx: elements; it is not a standalone RDX document, so it is not
# validated against rdx.xsd (only checked for well-formedness here).
xmllint --noout examples/cyclonedx-embedded.xml \
  && echo "  - examples/cyclonedx-embedded.xml: well-formed"

echo "All validations passed."
