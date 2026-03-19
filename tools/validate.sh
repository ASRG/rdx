#!/usr/bin/env bash
set -euo pipefail
echo "JSON Schema validation requires 'ajv' (npm i -g ajv-cli)"
echo "XML validation requires 'xmllint'"

echo "Validating JSON examples..."
ajv -s spec/json/rdx.schema.json -d examples/rdx-example.json --strict=false
ajv -s spec/json/rdx.schema.json -d examples/rdx-relationships-example.json --strict=false
ajv -s spec/json/rdx.schema.json -d examples/rdx-multiple-threats-example.json --strict=false
ajv -s spec/json/rdx.schema.json -d examples/rdx-mitigation-relationships-example.json --strict=false
ajv -s spec/json/rdx.schema.json -d examples/rdx-cal-taf-example.json --strict=false
ajv -s spec/json/rdx.schema.json -d examples/rdx-risk-threshold-example.json --strict=false

echo "Validating XML examples..."
# xmllint --noout --schema spec/xml/rdx.xsd examples/cyclonedx-embedded.xml
