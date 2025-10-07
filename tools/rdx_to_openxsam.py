#!/usr/bin/env python3
"""
RDX to OpenXSAM Converter

Converts Risk Data Exchange (RDX) format to OpenXSAM format for automotive cybersecurity
threat assessment and risk analysis (TARA) data exchange.

Usage:
    python rdx_to_openxsam.py <input_file> [output_file]
    
Input formats supported:
    - Standalone RDX JSON
    - CycloneDX-embedded RDX JSON
    
Output format:
    - OpenXSAM XML format (based on typical OSAM structure)
"""

import json
import sys
import argparse
import uuid
from datetime import datetime
from xml.etree import ElementTree as ET
from xml.dom import minidom
from pathlib import Path


class RDXToOpenXSAMConverter:
    """Converts RDX format to OpenXSAM format."""
    
    def __init__(self):
        self.namespace = "http://www.itemis.com/openxsam/v1.0"
        self.rdx_data = None
        
    def extract_rdx_from_cyclonedx(self, cyclonedx_data):
        """Extract RDX data from CycloneDX metadata properties."""
        if not isinstance(cyclonedx_data, dict):
            return None
            
        metadata = cyclonedx_data.get('metadata', {})
        properties = metadata.get('properties', [])
        
        for prop in properties:
            if prop.get('name') == 'https://asrg.io/ns/rdx#document':
                try:
                    return json.loads(prop.get('value', '{}'))
                except json.JSONDecodeError:
                    print("Warning: Invalid JSON in RDX property")
                    return None
        return None
    
    def load_rdx_data(self, input_file):
        """Load and parse RDX data from input file."""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            raise ValueError(f"Error reading input file: {e}")
        
        # Check if it's a standalone RDX file or CycloneDX-embedded
        if 'schemaVersion' in data and 'riskSet' in data:
            # Standalone RDX format
            self.rdx_data = data
        elif 'bomFormat' in data and data.get('bomFormat') == 'CycloneDX':
            # CycloneDX-embedded format
            self.rdx_data = self.extract_rdx_from_cyclonedx(data)
            if not self.rdx_data:
                raise ValueError("No RDX data found in CycloneDX metadata")
        else:
            raise ValueError("Unrecognized input format. Expected RDX or CycloneDX with embedded RDX.")
        
        return self.rdx_data
    
    def create_openxsam_header(self, root):
        """Create OpenXSAM header information."""
        header = ET.SubElement(root, "Header")
        
        # Document metadata
        doc_info = ET.SubElement(header, "DocumentInformation")
        ET.SubElement(doc_info, "DocumentId").text = self.rdx_data.get('documentId', str(uuid.uuid4()))
        ET.SubElement(doc_info, "DocumentVersion").text = "1.0"
        ET.SubElement(doc_info, "DocumentDate").text = self.rdx_data.get('created', datetime.now().isoformat())
        ET.SubElement(doc_info, "CreatedBy").text = self.rdx_data.get('createdBy', 'RDX to OpenXSAM Converter')
        
        # Tool information
        tool_info = ET.SubElement(header, "ToolInformation")
        ET.SubElement(tool_info, "ToolName").text = "RDX to OpenXSAM Converter"
        ET.SubElement(tool_info, "ToolVersion").text = "1.0.0"
        ET.SubElement(tool_info, "ToolVendor").text = "ASRG RDX Project"
        
        # Sources
        if self.rdx_data.get('sources'):
            sources = ET.SubElement(header, "Sources")
            for source in self.rdx_data['sources']:
                ET.SubElement(sources, "Source").text = source
    
    def convert_item_definition(self, root):
        """Convert RDX itemDefinition to OpenXSAM ItemDefinition."""
        risk_set = self.rdx_data.get('riskSet', {})
        item_def = risk_set.get('itemDefinition', {})
        
        if not item_def:
            return
        
        item_definition = ET.SubElement(root, "ItemDefinition")
        item_definition.set("id", item_def.get('id', 'ITEM-001'))
        
        ET.SubElement(item_definition, "Name").text = item_def.get('title', 'Unnamed Item')
        
        if item_def.get('boundary'):
            ET.SubElement(item_definition, "Boundary").text = item_def['boundary']
        
        if item_def.get('architecture'):
            ET.SubElement(item_definition, "Architecture").text = item_def['architecture']
        
        if item_def.get('environment'):
            ET.SubElement(item_definition, "Environment").text = item_def['environment']
        
        # Functions
        if item_def.get('functions'):
            functions = ET.SubElement(item_definition, "Functions")
            for func in item_def['functions']:
                ET.SubElement(functions, "Function").text = func
        
        # Interfaces
        if item_def.get('interfaces'):
            interfaces = ET.SubElement(item_definition, "Interfaces")
            for interface in item_def['interfaces']:
                interface_elem = ET.SubElement(interfaces, "Interface")
                interface_elem.set("name", interface)
        
        # Assumptions
        if item_def.get('assumptions'):
            assumptions = ET.SubElement(item_definition, "Assumptions")
            for assumption in item_def['assumptions']:
                ET.SubElement(assumptions, "Assumption").text = assumption
    
    def convert_assets(self, root):
        """Convert RDX assets to OpenXSAM Assets."""
        risk_set = self.rdx_data.get('riskSet', {})
        assets = risk_set.get('assets', [])
        
        if not assets:
            return
        
        assets_elem = ET.SubElement(root, "Assets")
        
        for asset in assets:
            asset_elem = ET.SubElement(assets_elem, "Asset")
            asset_elem.set("id", asset.get('id', ''))
            
            ET.SubElement(asset_elem, "Name").text = asset.get('title', 'Unnamed Asset')
            
            # CIA Properties
            if asset.get('properties'):
                properties = ET.SubElement(asset_elem, "SecurityProperties")
                for prop in asset['properties']:
                    prop_elem = ET.SubElement(properties, "SecurityProperty")
                    prop_elem.set("type", prop)
            
            # External IDs
            if asset.get('externalIds'):
                external_ids = ET.SubElement(asset_elem, "ExternalIds")
                for ext_id in asset['externalIds']:
                    ET.SubElement(external_ids, "ExternalId").text = ext_id
    
    def convert_damage_scenarios(self, root):
        """Convert RDX damageScenarios to OpenXSAM DamageScenarios."""
        risk_set = self.rdx_data.get('riskSet', {})
        damage_scenarios = risk_set.get('damageScenarios', [])
        
        if not damage_scenarios:
            return
        
        scenarios_elem = ET.SubElement(root, "DamageScenarios")
        
        for scenario in damage_scenarios:
            scenario_elem = ET.SubElement(scenarios_elem, "DamageScenario")
            scenario_elem.set("id", scenario.get('id', ''))
            
            ET.SubElement(scenario_elem, "Name").text = scenario.get('title', 'Unnamed Damage Scenario')
            
            if scenario.get('description'):
                ET.SubElement(scenario_elem, "Description").text = scenario['description']
            
            # Impacted functions
            if scenario.get('impactedFunctions'):
                functions = ET.SubElement(scenario_elem, "ImpactedFunctions")
                for func in scenario['impactedFunctions']:
                    ET.SubElement(functions, "Function").text = func
            
            # Affected road users
            if scenario.get('affectedRoadUsers'):
                users = ET.SubElement(scenario_elem, "AffectedRoadUsers")
                for user in scenario['affectedRoadUsers']:
                    ET.SubElement(users, "RoadUser").text = user
    
    def convert_threat_scenarios(self, root):
        """Convert RDX threatScenarios to OpenXSAM ThreatScenarios."""
        risk_set = self.rdx_data.get('riskSet', {})
        threat_scenarios = risk_set.get('threatScenarios', [])
        
        if not threat_scenarios:
            return
        
        scenarios_elem = ET.SubElement(root, "ThreatScenarios")
        
        for scenario in threat_scenarios:
            scenario_elem = ET.SubElement(scenarios_elem, "ThreatScenario")
            scenario_elem.set("id", scenario.get('id', ''))
            
            ET.SubElement(scenario_elem, "Name").text = scenario.get('title', 'Unnamed Threat Scenario')
            
            if scenario.get('cause'):
                ET.SubElement(scenario_elem, "Cause").text = scenario['cause']
            
            # Targeted assets
            if scenario.get('targetedAssetIds'):
                targets = ET.SubElement(scenario_elem, "TargetedAssets")
                for asset_id in scenario['targetedAssetIds']:
                    target = ET.SubElement(targets, "TargetedAsset")
                    target.set("assetRef", asset_id)
            
            # Compromised properties
            if scenario.get('compromisedProperties'):
                properties = ET.SubElement(scenario_elem, "CompromisedProperties")
                for prop in scenario['compromisedProperties']:
                    prop_elem = ET.SubElement(properties, "CompromisedProperty")
                    prop_elem.set("type", prop)
    
    def convert_attack_paths(self, root):
        """Convert RDX attackPaths to OpenXSAM AttackPaths."""
        risk_set = self.rdx_data.get('riskSet', {})
        attack_paths = risk_set.get('attackPaths', [])
        
        if not attack_paths:
            return
        
        paths_elem = ET.SubElement(root, "AttackPaths")
        
        for path in attack_paths:
            path_elem = ET.SubElement(paths_elem, "AttackPath")
            path_elem.set("id", path.get('id', ''))
            
            ET.SubElement(path_elem, "Name").text = path.get('title', 'Unnamed Attack Path')
            
            if path.get('threatScenarioId'):
                ET.SubElement(path_elem, "ThreatScenarioRef").text = path['threatScenarioId']
            
            # Attack steps
            if path.get('steps'):
                steps = ET.SubElement(path_elem, "AttackSteps")
                for i, step in enumerate(path['steps'], 1):
                    step_elem = ET.SubElement(steps, "AttackStep")
                    step_elem.set("order", str(i))
                    step_elem.text = step
    
    def convert_risk_assessments(self, root):
        """Convert RDX risk ratings and values to OpenXSAM RiskAssessments."""
        risk_set = self.rdx_data.get('riskSet', {})
        risk_values = risk_set.get('riskValues', [])
        afr_ratings = risk_set.get('attackFeasibilityRatings', [])
        impact_ratings = risk_set.get('impactRatings', [])
        
        if not (risk_values or afr_ratings or impact_ratings):
            return
        
        assessments_elem = ET.SubElement(root, "RiskAssessments")
        
        # Convert risk values
        for risk_value in risk_values:
            assessment_elem = ET.SubElement(assessments_elem, "RiskAssessment")
            assessment_elem.set("id", risk_value.get('id', ''))
            
            if risk_value.get('threatScenarioId'):
                ET.SubElement(assessment_elem, "ThreatScenarioRef").text = risk_value['threatScenarioId']
            
            if risk_value.get('methodId'):
                ET.SubElement(assessment_elem, "Method").text = risk_value['methodId']
            
            score_elem = ET.SubElement(assessment_elem, "RiskScore")
            score_elem.text = str(risk_value.get('score', ''))
            if risk_value.get('band'):
                score_elem.set("band", risk_value['band'])
            
            if risk_value.get('rationale'):
                ET.SubElement(assessment_elem, "Rationale").text = risk_value['rationale']
    
    def convert_controls(self, root):
        """Convert RDX controls to OpenXSAM SecurityControls."""
        risk_set = self.rdx_data.get('riskSet', {})
        controls = risk_set.get('controls', [])
        
        if not controls:
            return
        
        controls_elem = ET.SubElement(root, "SecurityControls")
        
        for control in controls:
            control_elem = ET.SubElement(controls_elem, "SecurityControl")
            control_elem.set("id", control.get('id', ''))
            
            ET.SubElement(control_elem, "Name").text = control.get('title', 'Unnamed Control')
            
            if control.get('catalog'):
                ET.SubElement(control_elem, "Catalog").text = control['catalog']
            
            if control.get('controlId'):
                ET.SubElement(control_elem, "ControlId").text = control['controlId']
            
            if control.get('implementationStatus'):
                status_elem = ET.SubElement(control_elem, "ImplementationStatus")
                status_elem.text = control['implementationStatus']
    
    def convert_risk_treatment(self, root):
        """Convert RDX riskTreatmentDecisions to OpenXSAM RiskTreatment."""
        risk_set = self.rdx_data.get('riskSet', {})
        decisions = risk_set.get('riskTreatmentDecisions', [])
        
        if not decisions:
            return
        
        treatment_elem = ET.SubElement(root, "RiskTreatment")
        
        for decision in decisions:
            decision_elem = ET.SubElement(treatment_elem, "TreatmentDecision")
            decision_elem.set("id", decision.get('id', ''))
            
            if decision.get('riskValueId'):
                ET.SubElement(decision_elem, "RiskValueRef").text = decision['riskValueId']
            
            ET.SubElement(decision_elem, "Decision").text = decision.get('decision', 'accept')
            
            if decision.get('justification'):
                ET.SubElement(decision_elem, "Justification").text = decision['justification']
            
            # Applied controls
            if decision.get('controls'):
                controls = ET.SubElement(decision_elem, "AppliedControls")
                for control_id in decision['controls']:
                    control_ref = ET.SubElement(controls, "ControlRef")
                    control_ref.text = control_id
    
    def convert_to_openxsam(self, input_file, output_file=None):
        """Main conversion method."""
        # Load RDX data
        self.load_rdx_data(input_file)
        
        # Create root OpenXSAM element
        root = ET.Element("OpenXSAM")
        root.set("xmlns", self.namespace)
        root.set("version", "1.0")
        
        # Convert each section
        self.create_openxsam_header(root)
        self.convert_item_definition(root)
        self.convert_assets(root)
        self.convert_damage_scenarios(root)
        self.convert_threat_scenarios(root)
        self.convert_attack_paths(root)
        self.convert_risk_assessments(root)
        self.convert_controls(root)
        self.convert_risk_treatment(root)
        
        # Create XML tree and format
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ", level=0)
        
        # Generate output filename if not provided
        if output_file is None:
            input_path = Path(input_file)
            output_file = input_path.with_suffix('.openxsam.xml').name
        
        # Write to file
        try:
            tree.write(output_file, encoding='utf-8', xml_declaration=True)
            print(f"OpenXSAM file generated: {output_file}")
            return output_file
        except Exception as e:
            raise ValueError(f"Error writing output file: {e}")


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description='Convert RDX format to OpenXSAM format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python rdx_to_openxsam.py rdx-example.json
  python rdx_to_openxsam.py cyclonedx-embedded.json output.openxsam.xml
  python rdx_to_openxsam.py input.json --validate
        """
    )
    
    parser.add_argument('input_file', help='Input RDX or CycloneDX file')
    parser.add_argument('output_file', nargs='?', help='Output OpenXSAM file (optional)')
    parser.add_argument('--validate', action='store_true', 
                       help='Validate input file format before conversion')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not Path(args.input_file).exists():
        print(f"Error: Input file '{args.input_file}' not found")
        sys.exit(1)
    
    try:
        converter = RDXToOpenXSAMConverter()
        
        if args.validate:
            print("Validating input file...")
            converter.load_rdx_data(args.input_file)
            print("✓ Input file is valid RDX format")
        
        if args.verbose:
            print(f"Converting {args.input_file} to OpenXSAM format...")
        
        output_file = converter.convert_to_openxsam(args.input_file, args.output_file)
        
        if args.verbose:
            print(f"✓ Conversion completed successfully")
            print(f"✓ Output written to: {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()