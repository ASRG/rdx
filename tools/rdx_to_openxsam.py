#!/usr/bin/env python3
"""
rdx_to_openxsam.py - Convert Risk Data Exchange (RDX) format to OpenXSAM format

Usage:
    python rdx_to_openxsam.py --input <rdx_file.json> --output <output_file.xml>
    python rdx_to_openxsam.py --input <rdx_file.json> --output <output_file.json> --format json

Arguments:
    --input     Path to the input RDX JSON file
    --output    Path for the output OpenXSAM file
    --format    Output format: 'xml' (default) or 'json'
    --pretty    Pretty-print the output (default: true)
    --help      Show this help message

Example:
    python rdx_to_openxsam.py --input examples/rdx-example.json --output output/analysis.xml
    python rdx_to_openxsam.py --input examples/rdx-example.json --output output/analysis.json --format json
"""

import json
import argparse
import sys
import uuid
from datetime import datetime, timezone
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom


# ─────────────────────────────────────────────
# Mapping helpers
# ─────────────────────────────────────────────

STRIDE_MAP = {
    "confidentiality": "Information Disclosure",
    "integrity": "Tampering",
    "availability": "Denial of Service",
}


def to_xsam_id(rdx_id: str) -> str:
    """Normalise an RDX identifier to a valid OpenXSAM id."""
    return rdx_id.replace(" ", "_").replace("/", "-")


def iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ─────────────────────────────────────────────
# RDX → OpenXSAM element converters
# ─────────────────────────────────────────────

def convert_item_definition(item_def: dict, root: Element) -> None:
    """Map RDX itemDefinition to OpenXSAM System."""
    system = SubElement(root, "System")
    system.set("id", to_xsam_id(item_def.get("id", "SYSTEM-001")))
    SubElement(system, "Name").text = item_def.get("title", "Unknown System")
    SubElement(system, "Description").text = item_def.get("boundary", "")
    SubElement(system, "Architecture").text = item_def.get("architecture", "")
    SubElement(system, "Environment").text = item_def.get("environment", "")
    if item_def.get("countryOfOrigin"):
        SubElement(system, "CountryOfOrigin").text = item_def["countryOfOrigin"]

    # Functions
    functions = item_def.get("functions", [])
    if functions:
        funcs_el = SubElement(system, "Functions")
        for f in functions:
            SubElement(funcs_el, "Function").text = f

    # Interfaces
    interfaces = item_def.get("interfaces", [])
    if interfaces:
        ifaces_el = SubElement(system, "Interfaces")
        for iface in interfaces:
            iface_el = SubElement(ifaces_el, "Interface")
            iface_el.set("id", to_xsam_id(str(iface)))
            SubElement(iface_el, "Name").text = str(iface)

    # Assumptions
    assumptions = item_def.get("assumptions", [])
    if assumptions:
        assum_el = SubElement(system, "Assumptions")
        for a in assumptions:
            SubElement(assum_el, "Assumption").text = a


def convert_assets(assets: list, root: Element) -> None:
    """Map RDX assets to OpenXSAM Assets."""
    if not assets:
        return
    assets_el = SubElement(root, "Assets")
    for asset in assets:
        a_el = SubElement(assets_el, "Asset")
        a_el.set("id", to_xsam_id(asset.get("id", str(uuid.uuid4())[:8])))
        SubElement(a_el, "Name").text = asset.get("title", "Unknown Asset")
        SubElement(a_el, "Description").text = asset.get("description", "")

        # CIA → STRIDE mapping. RDX asset `properties` is an array of CIA
        # property labels (e.g. ["confidentiality", "integrity"]).
        props = asset.get("properties", []) or []
        if props:
            stride_el = SubElement(a_el, "SecurityProperties")
            for cia_prop, stride_label in STRIDE_MAP.items():
                if cia_prop in props:
                    prop_el = SubElement(stride_el, "SecurityProperty")
                    SubElement(prop_el, "Category").text = stride_label

        # Hashes (if present)
        hashes = asset.get("hashes", [])
        if hashes:
            hashes_el = SubElement(a_el, "Hashes")
            for h in hashes:
                hash_el = SubElement(hashes_el, "Hash")
                hash_el.set("algorithm", h.get("alg", "SHA-256"))
                hash_el.text = h.get("content", "")


def convert_damage_scenarios(damage_scenarios: list, root: Element) -> None:
    """Map RDX damageScenarios to OpenXSAM DamageScenarios."""
    if not damage_scenarios:
        return
    ds_el = SubElement(root, "DamageScenarios")
    for ds in damage_scenarios:
        d_el = SubElement(ds_el, "DamageScenario")
        d_el.set("id", to_xsam_id(ds.get("id", "")))
        SubElement(d_el, "Title").text = ds.get("title", "")
        SubElement(d_el, "Description").text = ds.get("description", "")
        if ds.get("assetId"):
            SubElement(d_el, "AssetRef").text = to_xsam_id(ds["assetId"])
        if ds.get("impactCategories"):
            cats_el = SubElement(d_el, "ImpactCategories")
            for cat, val in ds["impactCategories"].items():
                cat_el = SubElement(cats_el, "ImpactCategory")
                cat_el.set("type", cat)
                cat_el.text = str(val)


def convert_threat_scenarios(threat_scenarios: list, root: Element) -> None:
    """Map RDX threatScenarios to OpenXSAM Threats."""
    if not threat_scenarios:
        return
    threats_el = SubElement(root, "Threats")
    for ts in threat_scenarios:
        t_el = SubElement(threats_el, "Threat")
        t_el.set("id", to_xsam_id(ts.get("id", "")))
        SubElement(t_el, "Title").text = ts.get("title", "")
        SubElement(t_el, "Description").text = ts.get("description", "")
        if ts.get("assetId"):
            SubElement(t_el, "AssetRef").text = to_xsam_id(ts["assetId"])
        if ts.get("damageScenarioId"):
            SubElement(t_el, "DamageScenarioRef").text = to_xsam_id(ts["damageScenarioId"])
        if ts.get("attackPathIds"):
            refs_el = SubElement(t_el, "AttackPathRefs")
            for ap_id in ts["attackPathIds"]:
                SubElement(refs_el, "AttackPathRef").text = to_xsam_id(ap_id)


def convert_attack_steps(attack_steps: list, root: Element) -> None:
    """Map RDX attackSteps to OpenXSAM AttackSteps."""
    if not attack_steps:
        return
    steps_el = SubElement(root, "AttackSteps")
    for step in attack_steps:
        s_el = SubElement(steps_el, "AttackStep")
        s_el.set("id", to_xsam_id(step.get("id", "")))
        SubElement(s_el, "Title").text = step.get("title", "")
        SubElement(s_el, "Description").text = step.get("description", "")
        if step.get("attackFeasibilityRatingIds"):
            refs_el = SubElement(s_el, "FeasibilityRatingRefs")
            for afr_id in step["attackFeasibilityRatingIds"]:
                SubElement(refs_el, "FeasibilityRatingRef").text = to_xsam_id(afr_id)
        if step.get("controlIds"):
            ctrl_el = SubElement(s_el, "ControlRefs")
            for ctrl_id in step["controlIds"]:
                SubElement(ctrl_el, "ControlRef").text = to_xsam_id(ctrl_id)


def convert_attack_paths(attack_paths: list, root: Element) -> None:
    """Map RDX attackPaths to OpenXSAM AttackPaths."""
    if not attack_paths:
        return
    paths_el = SubElement(root, "AttackPaths")
    for ap in attack_paths:
        p_el = SubElement(paths_el, "AttackPath")
        p_el.set("id", to_xsam_id(ap.get("id", "")))
        SubElement(p_el, "Title").text = ap.get("title", "")
        if ap.get("threatScenarioId"):
            SubElement(p_el, "ThreatRef").text = to_xsam_id(ap["threatScenarioId"])
        steps_el = SubElement(p_el, "Steps")
        for step_id in ap.get("stepIds", []):
            SubElement(steps_el, "StepRef").text = to_xsam_id(step_id)


def convert_feasibility_ratings(afrs: list, root: Element) -> None:
    """Map RDX attackFeasibilityRatings to OpenXSAM FeasibilityRatings."""
    if not afrs:
        return
    ratings_el = SubElement(root, "FeasibilityRatings")
    for afr in afrs:
        r_el = SubElement(ratings_el, "FeasibilityRating")
        r_el.set("id", to_xsam_id(afr.get("id", "")))
        SubElement(r_el, "Score").text = str(afr.get("score", ""))
        SubElement(r_el, "Band").text = afr.get("band", "")
        SubElement(r_el, "Rationale").text = afr.get("rationale", "")
        factors = afr.get("factors", {})
        if factors:
            factors_el = SubElement(r_el, "Factors")
            for factor, value in factors.items():
                f_el = SubElement(factors_el, "Factor")
                f_el.set("name", factor)
                f_el.text = str(value)


def convert_risk_values(risk_values: list, root: Element) -> None:
    """Map RDX riskValues to OpenXSAM RiskValues."""
    if not risk_values:
        return
    rv_el = SubElement(root, "RiskValues")
    for rv in risk_values:
        r_el = SubElement(rv_el, "RiskValue")
        r_el.set("id", to_xsam_id(rv.get("id", "")))
        SubElement(r_el, "Score").text = str(rv.get("score", ""))
        SubElement(r_el, "Band").text = rv.get("band", "")
        SubElement(r_el, "Rationale").text = rv.get("rationale", "")
        if rv.get("threatScenarioId"):
            SubElement(r_el, "ThreatRef").text = to_xsam_id(rv["threatScenarioId"])
        if rv.get("afrRef"):
            SubElement(r_el, "FeasibilityRef").text = to_xsam_id(rv["afrRef"])
        if rv.get("impactRef"):
            SubElement(r_el, "ImpactRef").text = to_xsam_id(rv["impactRef"])


def convert_controls(controls: list, root: Element) -> None:
    """Map RDX controls to OpenXSAM Controls."""
    if not controls:
        return
    ctrl_el = SubElement(root, "Controls")
    for ctrl in controls:
        c_el = SubElement(ctrl_el, "Control")
        c_el.set("id", to_xsam_id(ctrl.get("id", "")))
        SubElement(c_el, "Title").text = ctrl.get("title", "")
        if ctrl.get("catalog"):
            SubElement(c_el, "Catalog").text = ctrl["catalog"]
        if ctrl.get("controlId"):
            SubElement(c_el, "CatalogControlId").text = ctrl["controlId"]
        if ctrl.get("description"):
            SubElement(c_el, "Description").text = ctrl["description"]
        if ctrl.get("status"):
            SubElement(c_el, "Status").text = ctrl["status"]


def convert_cal_assurance_levels(cal_levels: list, root: Element) -> None:
    """Map RDX calAssuranceLevels to OpenXSAM CybersecurityAssuranceLevels."""
    if not cal_levels:
        return
    cal_el = SubElement(root, "CybersecurityAssuranceLevels")
    for cal in cal_levels:
        c_el = SubElement(cal_el, "CAL")
        c_el.set("id", to_xsam_id(cal.get("id", "")))
        SubElement(c_el, "Level").text = str(cal.get("level", ""))
        SubElement(c_el, "Rationale").text = cal.get("rationale", "")
        objectives = cal.get("objectives", [])
        if objectives:
            obj_el = SubElement(c_el, "Objectives")
            for obj in objectives:
                SubElement(obj_el, "Objective").text = obj


# ─────────────────────────────────────────────
# Top-level conversion
# ─────────────────────────────────────────────

def rdx_to_openxsam_xml(rdx: dict) -> str:
    """Convert an RDX dict to an OpenXSAM XML string."""
    root = Element("OpenXSAM")
    root.set("xmlns", "https://openxsam.org/ns/1.1")
    root.set("version", "1.1")
    root.set("created", iso_now())
    root.set("rdxDocumentId", rdx.get("documentId", ""))
    root.set("rdxSchemaVersion", rdx.get("schemaVersion", "0.1.0"))

    risk_set = rdx.get("riskSet", {})
    convert_item_definition(risk_set.get("itemDefinition", {}), root)
    convert_assets(risk_set.get("assets", []), root)
    convert_damage_scenarios(risk_set.get("damageScenarios", []), root)
    convert_threat_scenarios(risk_set.get("threatScenarios", []), root)
    convert_attack_steps(risk_set.get("attackSteps", []), root)
    convert_attack_paths(risk_set.get("attackPaths", []), root)
    convert_feasibility_ratings(risk_set.get("attackFeasibilityRatings", []), root)
    convert_risk_values(risk_set.get("riskValues", []), root)
    convert_controls(risk_set.get("controls", []), root)
    convert_cal_assurance_levels(risk_set.get("calAssuranceLevels", []), root)

    raw = tostring(root, encoding="unicode")
    pretty = minidom.parseString(raw).toprettyxml(indent="  ")
    # Remove the auto-added XML declaration line since we add our own
    lines = pretty.split("\n")
    if lines[0].startswith("<?xml"):
        lines[0] = '<?xml version="1.0" encoding="UTF-8"?>'
    return "\n".join(lines)


def rdx_to_openxsam_json(rdx: dict) -> dict:
    """Convert an RDX dict to an OpenXSAM-structured JSON dict."""
    risk_set = rdx.get("riskSet", {})
    item_def = risk_set.get("itemDefinition", {})

    return {
        "openxsam": {
            "version": "1.1",
            "created": iso_now(),
            "rdxDocumentId": rdx.get("documentId", ""),
            "rdxSchemaVersion": rdx.get("schemaVersion", "0.1.0"),
            "system": {
                "id": to_xsam_id(item_def.get("id", "SYSTEM-001")),
                "name": item_def.get("title", ""),
                "description": item_def.get("boundary", ""),
                "architecture": item_def.get("architecture", ""),
                "environment": item_def.get("environment", ""),
                "countryOfOrigin": item_def.get("countryOfOrigin", ""),
                "functions": item_def.get("functions", []),
                "interfaces": item_def.get("interfaces", []),
                "assumptions": item_def.get("assumptions", []),
            },
            "assets": [
                {
                    "id": to_xsam_id(a.get("id", "")),
                    "name": a.get("title", ""),
                    "description": a.get("description", ""),
                    "securityProperties": a.get("properties", {}),
                    "hashes": a.get("hashes", []),
                }
                for a in risk_set.get("assets", [])
            ],
            "damageScenarios": [
                {
                    "id": to_xsam_id(ds.get("id", "")),
                    "title": ds.get("title", ""),
                    "description": ds.get("description", ""),
                    "assetRef": to_xsam_id(ds.get("assetId", "")),
                    "impactCategories": ds.get("impactCategories", {}),
                }
                for ds in risk_set.get("damageScenarios", [])
            ],
            "threats": [
                {
                    "id": to_xsam_id(ts.get("id", "")),
                    "title": ts.get("title", ""),
                    "description": ts.get("description", ""),
                    "assetRef": to_xsam_id(ts.get("assetId", "")),
                    "damageScenarioRef": to_xsam_id(ts.get("damageScenarioId", "")),
                    "attackPathRefs": [to_xsam_id(i) for i in ts.get("attackPathIds", [])],
                }
                for ts in risk_set.get("threatScenarios", [])
            ],
            "attackSteps": [
                {
                    "id": to_xsam_id(s.get("id", "")),
                    "title": s.get("title", ""),
                    "description": s.get("description", ""),
                    "feasibilityRatingRefs": [to_xsam_id(i) for i in s.get("attackFeasibilityRatingIds", [])],
                    "controlRefs": [to_xsam_id(i) for i in s.get("controlIds", [])],
                }
                for s in risk_set.get("attackSteps", [])
            ],
            "attackPaths": [
                {
                    "id": to_xsam_id(ap.get("id", "")),
                    "title": ap.get("title", ""),
                    "threatRef": to_xsam_id(ap.get("threatScenarioId", "")),
                    "steps": [to_xsam_id(i) for i in ap.get("stepIds", [])],
                }
                for ap in risk_set.get("attackPaths", [])
            ],
            "feasibilityRatings": [
                {
                    "id": to_xsam_id(afr.get("id", "")),
                    "score": afr.get("score", ""),
                    "band": afr.get("band", ""),
                    "rationale": afr.get("rationale", ""),
                    "factors": afr.get("factors", {}),
                }
                for afr in risk_set.get("attackFeasibilityRatings", [])
            ],
            "riskValues": [
                {
                    "id": to_xsam_id(rv.get("id", "")),
                    "score": rv.get("score", ""),
                    "band": rv.get("band", ""),
                    "rationale": rv.get("rationale", ""),
                    "threatRef": to_xsam_id(rv.get("threatScenarioId", "")),
                    "feasibilityRef": to_xsam_id(rv.get("afrRef", "")),
                    "impactRef": to_xsam_id(rv.get("impactRef", "")),
                }
                for rv in risk_set.get("riskValues", [])
            ],
            "controls": [
                {
                    "id": to_xsam_id(c.get("id", "")),
                    "title": c.get("title", ""),
                    "catalog": c.get("catalog", ""),
                    "catalogControlId": c.get("controlId", ""),
                    "description": c.get("description", ""),
                    "status": c.get("status", "proposed"),
                }
                for c in risk_set.get("controls", [])
            ],
            "cybersecurityAssuranceLevels": [
                {
                    "id": to_xsam_id(cal.get("id", "")),
                    "level": cal.get("level", ""),
                    "rationale": cal.get("rationale", ""),
                    "objectives": cal.get("objectives", []),
                }
                for cal in risk_set.get("calAssuranceLevels", [])
            ],
        }
    }


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert Risk Data Exchange (RDX) JSON to OpenXSAM format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--input", "-i", required=True, help="Path to input RDX JSON file")
    parser.add_argument("--output", "-o", required=True, help="Path for output OpenXSAM file")
    parser.add_argument(
        "--format", "-f", choices=["xml", "json"], default="xml",
        help="Output format: 'xml' (default) or 'json'"
    )
    parser.add_argument(
        "--pretty", action="store_true", default=True,
        help="Pretty-print the output (default: true)"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Load RDX input
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            rdx = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate minimal RDX structure
    if "riskSet" not in rdx:
        print("Error: Input file does not appear to be a valid RDX document (missing 'riskSet').", file=sys.stderr)
        sys.exit(1)

    # Convert
    try:
        if args.format == "xml":
            output_str = rdx_to_openxsam_xml(rdx)
        else:
            output_dict = rdx_to_openxsam_json(rdx)
            output_str = json.dumps(output_dict, indent=2 if args.pretty else None, ensure_ascii=False)
    except Exception as e:
        print(f"Error during conversion: {e}", file=sys.stderr)
        sys.exit(1)

    # Write output
    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_str)
        print(f"Successfully converted '{args.input}' to OpenXSAM {args.format.upper()} at '{args.output}'")
    except IOError as e:
        print(f"Error: Failed to write output file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
