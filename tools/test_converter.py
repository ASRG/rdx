#!/usr/bin/env python3
"""
Simple test script to validate the RDX to OpenXSAM converter
"""

import json
import sys
from pathlib import Path

# Add the tools directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from rdx_to_openxsam import RDXToOpenXSAMConverter

def test_converter():
    """Test the converter with example data."""
    converter = RDXToOpenXSAMConverter()
    
    # Test with standalone RDX example
    try:
        print("Testing standalone RDX conversion...")
        rdx_file = Path(__file__).parent.parent / "examples" / "rdx-example.json"
        output_file = converter.convert_to_openxsam(str(rdx_file))
        print(f"✓ Standalone RDX conversion successful: {output_file}")
    except Exception as e:
        print(f"✗ Standalone RDX conversion failed: {e}")
    
    # Test with CycloneDX embedded RDX
    try:
        print("\nTesting CycloneDX embedded RDX conversion...")
        cyclonedx_file = Path(__file__).parent.parent / "examples" / "cyclonedx-embedded.json"
        output_file = converter.convert_to_openxsam(str(cyclonedx_file))
        print(f"✓ CycloneDX embedded RDX conversion successful: {output_file}")
    except Exception as e:
        print(f"✗ CycloneDX embedded RDX conversion failed: {e}")

if __name__ == '__main__':
    test_converter()