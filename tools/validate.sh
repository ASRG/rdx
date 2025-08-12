#!/usr/bin/env bash
set -euo pipefail
echo "JSON Schema validation requires 'ajv' (npm i -g ajv-cli)"
echo "XML validation requires 'xmllint'"
# ajv -s spec/json/rdx.schema.json -d examples/rdx-example.json --strict=false
# xmllint --noout --schema spec/xml/rdx.xsd examples/cyclonedx-embedded.xml
