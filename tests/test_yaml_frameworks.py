#!/usr/bin/env python3
"""
YAML Framework Validation Test Suite
Validates all Scratchpad framework YAML files for syntax, structure, and semantic quality.

Author: Warp AI Agent
Date: 2025-10-01
"""

import sys
import yaml
from pathlib import Path
import re

def test_yaml_syntax():
    """Test that all YAML files have valid syntax.
    
    This test validates that all YAML framework files in the frameworks/
    directory can be successfully parsed by PyYAML's safe_load function.
    
    Raises:
        AssertionError: If any YAML files fail to parse
    """
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
    assert failed == 0


def test_required_keys():
    """Test that all frameworks have required keys.
    
    Validates that every framework YAML file contains the mandatory keys:
    - name: Framework name identifier
    - category: Framework category/type
    - documentation: Documentation metadata
    - framework: Main framework content structure
    
    Raises:
        AssertionError: If any frameworks are missing required keys
    """
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
    assert failed == 0


def test_framework_categories():
    """Test that frameworks are in correct directories.
    
    Verifies the repository structure contains the expected framework categories:
    - core: General-purpose reasoning templates (minimum 5 expected)
    - purpose-built: Task-specific frameworks
    - personas: AI assistant personality frameworks (minimum 2 expected)
    
    Ensures a minimum total of 20 frameworks across all categories.
    
    Raises:
        AssertionError: If total framework count is below 20
    """
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
    
    assert total >= 20  # Expect at least 20 frameworks


def test_metadata_quality():
    """Test quality and consistency of framework metadata.
    
    Validates metadata quality including:
    - Purpose field: Should be concise (< 30 words recommended)
    - Use case field: Should be descriptive (< 40 words recommended)
    - Version field: Must be present and non-empty
    - Content field: Must be substantial (> 100 characters)
    
    Issues warnings for quality concerns but allows some flexibility.
    
    Raises:
        AssertionError: If more than 10 quality warnings are detected
    """
    base_dir = Path(__file__).parent.parent
    frameworks_dir = base_dir / 'frameworks'
    
    yaml_files = list(frameworks_dir.glob('**/*.yml'))
    passed = 0
    warnings = []
    
    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            # Check documentation fields
            if 'documentation' in data:
                doc = data['documentation']
                
                # Check purpose length (should be concise)
                if 'purpose' in doc and doc['purpose']:
                    purpose_words = len(doc['purpose'].split())
                    if purpose_words > 30:
                        warnings.append(f"  ⚠️  {yaml_file.name}: Purpose too long ({purpose_words} words, recommend <30)")
                else:
                    warnings.append(f"  ⚠️  {yaml_file.name}: Missing or empty purpose field")
                
                # Check use_case field
                if 'use_case' in doc and doc['use_case']:
                    use_case_words = len(doc['use_case'].split())
                    if use_case_words > 40:
                        warnings.append(f"  ⚠️  {yaml_file.name}: Use case too long ({use_case_words} words, recommend <40)")
                else:
                    warnings.append(f"  ⚠️  {yaml_file.name}: Missing or empty use_case field")
            
            # Check version field
            if 'version' not in data or not data['version']:
                warnings.append(f"  ⚠️  {yaml_file.name}: Missing or empty version field")
            
            # Check content field
            if 'framework' in data and 'content' in data['framework']:
                content = data['framework']['content']
                if len(content) < 100:
                    warnings.append(f"  ⚠️  {yaml_file.name}: Framework content seems too short ({len(content)} chars)")
            
            passed += 1
        except Exception as e:
            warnings.append(f"  ❌ {yaml_file.name}: Error reading file - {e}")
    
    # Print warnings
    if warnings:
        print("\nMetadata Quality Warnings:")
        for warning in warnings:
            print(warning)
    
    print(f"\nMetadata Quality: {passed} files checked, {len(warnings)} warnings")
    assert len(warnings) < 10  # Allow some warnings but not too many


def test_field_types():
    """Validate that YAML fields have correct data types.
    
    Ensures type consistency across all framework files:
    - String fields: name, version, category
    - Dictionary fields: documentation, framework
    
    This prevents data type errors that could cause parsing issues
    in consuming applications.
    
    Raises:
        AssertionError: If any fields have incorrect data types
    """
    base_dir = Path(__file__).parent.parent
    frameworks_dir = base_dir / 'frameworks'
    
    yaml_files = list(frameworks_dir.glob('**/*.yml'))
    passed = 0
    failed = 0
    
    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            errors = []
            
            # Check string fields
            if 'name' in data and not isinstance(data['name'], str):
                errors.append("'name' must be a string")
            if 'version' in data and not isinstance(data.get('version'), str):
                errors.append("'version' must be a string")
            if 'category' in data and not isinstance(data['category'], str):
                errors.append("'category' must be a string")
            
            # Check nested dict fields
            if 'documentation' in data and not isinstance(data['documentation'], dict):
                errors.append("'documentation' must be a dictionary")
            if 'framework' in data and not isinstance(data['framework'], dict):
                errors.append("'framework' must be a dictionary")
            
            if errors:
                print(f"  ❌ {yaml_file.name}: {', '.join(errors)}")
                failed += 1
            else:
                passed += 1
                
        except Exception as e:
            print(f"  ❌ {yaml_file.name}: {e}")
            failed += 1
    
    print(f"Field Types: {passed} passed, {failed} failed")
    assert failed == 0


def test_content_uniqueness():
    """Detect highly similar content across frameworks.
    
    Performs a simple similarity check by comparing the first 500 characters
    of each framework's content field (normalized to lowercase with whitespace
    collapsed). This helps identify unintentional duplicates or copy-paste errors.
    
    Note: This is a basic check that detects exact duplicates. Frameworks may
    have similar structure while serving different purposes.
    
    Raises:
        AssertionError: If any frameworks have identical content samples
    """
    base_dir = Path(__file__).parent.parent
    frameworks_dir = base_dir / 'frameworks'
    
    yaml_files = list(frameworks_dir.glob('**/*.yml'))
    
    # Extract first 500 chars of each framework's content
    content_samples = {}
    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            if 'framework' in data and 'content' in data['framework']:
                content = data['framework']['content']
                # Normalize: lowercase, remove extra whitespace
                normalized = re.sub(r'\s+', ' ', content[:500].lower())
                content_samples[yaml_file.name] = normalized
        except Exception:
            continue
    
    # Simple similarity check - look for exact duplicates
    duplicates = []
    seen = {}
    for name, content in content_samples.items():
        if content in seen:
            duplicates.append(f"  ⚠️  {name} may be similar to {seen[content]}")
        else:
            seen[content] = name
    
    if duplicates:
        print("\nPotential Content Duplicates:")
        for dup in duplicates:
            print(dup)
    else:
        print("No obvious content duplication detected")
    
    assert len(duplicates) == 0


def main():
    """Run all tests and provide summary report.
    
    Executes the complete test suite for YAML framework validation including:
    - Syntax validation
    - Required keys check
    - Field type validation  
    - Metadata quality assessment
    - Content uniqueness check
    - Category organization verification
    
    Provides a detailed summary of test results with pass/fail/warning counts.
    
    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    print("="*70)
    print(" YAML Framework Validation Test Suite")
    print(" Enhanced with Semantic & Quality Checks")
    print("="*70)
    print()
    
    tests = [
        ("YAML Syntax Validation", test_yaml_syntax),
        ("Required Keys Check", test_required_keys),
        ("Field Type Validation", test_field_types),
        ("Metadata Quality Check", test_metadata_quality),
        ("Content Uniqueness Check", test_content_uniqueness),
        ("Framework Categories", test_framework_categories),
    ]
    
    passed = 0
    failed = 0
    warnings = 0
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        result = test_func()
        if result:
            print(f"✅ {test_name} PASSED")
            passed += 1
        else:
            # Metadata quality and uniqueness can fail with warnings
            if "Quality" in test_name or "Uniqueness" in test_name:
                print(f"⚠️  {test_name} HAS WARNINGS")
                warnings += 1
            else:
                print(f"❌ {test_name} FAILED")
                failed += 1
    
    print()
    print("="*70)
    print(f"Test Results: {passed} passed, {failed} failed, {warnings} warnings")
    print("="*70)
    
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
