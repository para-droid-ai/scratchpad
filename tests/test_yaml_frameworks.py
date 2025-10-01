#!/usr/bin/env python3
"""
YAML Framework Validation Test Suite
Validates all Scratchpad framework YAML files for syntax and structure.

Author: Warp AI Agent
Date: 2025-10-01
"""

import os
import sys
import yaml
from pathlib import Path

def test_yaml_syntax():
    """Test that all YAML files have valid syntax."""
    base_dir = Path(__file__).parent.parent
    frameworks_dir = base_dir / 'frameworks'
    
    yaml_files = list(frameworks_dir.glob('**/*.yml'))
    if not yaml_files:
        print("❌ FAIL: No YAML files found")
        return False
    
    print(f"Found {len(yaml_files)} YAML files")
    
    passed = 0
    failed = 0
    
    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
            print(f"  ✅ {yaml_file.relative_to(base_dir)}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {yaml_file.relative_to(base_dir)}: {e}")
            failed += 1
    
    print(f"\nYAML Syntax: {passed} passed, {failed} failed")
    return failed == 0


def test_required_keys():
    """Test that all frameworks have required keys."""
    base_dir = Path(__file__).parent.parent
    frameworks_dir = base_dir / 'frameworks'
    
    required_keys = ['name', 'category', 'documentation', 'framework']
    
    yaml_files = list(frameworks_dir.glob('**/*.yml'))
    passed = 0
    failed = 0
    
    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if not isinstance(data, dict):
                print(f"  ❌ {yaml_file.name}: Not a YAML dictionary")
                failed += 1
                continue
            
            missing_keys = [key for key in required_keys if key not in data]
            if missing_keys:
                print(f"  ⚠️  {yaml_file.name}: Missing keys {missing_keys}")
                failed += 1
            else:
                passed += 1
        except Exception as e:
            print(f"  ❌ {yaml_file.name}: {e}")
            failed += 1
    
    print(f"Required Keys: {passed} passed, {failed} failed")
    return failed == 0


def test_framework_categories():
    """Test that frameworks are in correct directories."""
    base_dir = Path(__file__).parent.parent
    frameworks_dir = base_dir / 'frameworks'
    
    categories = {
        'core': list((frameworks_dir / 'core').glob('*.yml')),
        'purpose-built': list((frameworks_dir / 'purpose-built').glob('*.yml')),
        'personas': list((frameworks_dir / 'personas').glob('*.yml'))
    }
    
    print("Framework Categories:")
    for category, files in categories.items():
        print(f"  {category}: {len(files)} frameworks")
    
    # Verify minimum counts
    if len(categories['core']) < 5:
        print("  ⚠️  Warning: Less than 5 core frameworks")
    if len(categories['personas']) < 2:
        print("  ⚠️  Warning: Less than 2 persona frameworks")
    
    total = sum(len(files) for files in categories.values())
    print(f"\nTotal: {total} frameworks")
    
    return total >= 20  # Expect at least 20 frameworks


def main():
    """Run all tests."""
    print("="*70)
    print(" YAML Framework Validation Test Suite")
    print("="*70)
    print()
    
    tests = [
        ("YAML Syntax Validation", test_yaml_syntax),
        ("Required Keys Check", test_required_keys),
        ("Framework Categories", test_framework_categories),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            print(f"✅ {test_name} PASSED")
            passed += 1
        else:
            print(f"❌ {test_name} FAILED")
            failed += 1
    
    print()
    print("="*70)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*70)
    
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
