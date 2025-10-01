#!/usr/bin/env python3
"""
Fix YAML Framework Formatting

Ensures all framework content uses literal block scalars (|) 
instead of escaped string format.

Author: Warp AI Agent
Date: 2025-10-01
"""

import yaml
from pathlib import Path

def fix_yaml_file(yaml_path):
    """Fix a single YAML file to use literal block scalars.
    
    Args:
        yaml_path: Path object pointing to the YAML file
        
    Returns:
        bool: True if file was modified
        
    Raises:
        yaml.YAMLError: If YAML parsing fails
        IOError: If file operations fail
    """
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Guard against None data
    if not data:
        return False
    
    # Manually construct the YAML with literal block scalars
    yaml_lines = []
    yaml_lines.append(f"name: {data['name']}")
    
    # Version might be number or string - quote defensively
    version = data.get('version', '')
    if isinstance(version, (int, float)):
        yaml_lines.append(f"version: \"{version}\"")
    else:
        yaml_lines.append(f"version: \"{version}\"")
    
    yaml_lines.append(f"category: {data['category']}")
    yaml_lines.append("documentation:")
    
    doc = data.get('documentation', {})
    if doc.get('purpose'):
        yaml_lines.append(f"  purpose: {doc['purpose']}")
    if doc.get('use_case'):
        yaml_lines.append(f"  use_case: {doc['use_case']}")
    if doc.get('character_count'):
        yaml_lines.append(f"  character_count: {doc['character_count']}")
    if doc.get('operational_guide'):
        yaml_lines.append(f"  operational_guide: {doc['operational_guide']}")
    
    yaml_lines.append("framework:")
    
    # Use literal block scalar for content
    content = data.get('framework', {}).get('content', '')
    yaml_lines.append("  content: |")
    
    # Add content lines with proper indentation
    for line in content.split('\n'):
        yaml_lines.append(f"    {line}" if line else "")
    
    # Write the properly formatted YAML
    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(yaml_lines))
        f.write('\n')  # Add final newline
    
    return True

def main():
    """Process all YAML files in the frameworks directory.
    
    Returns:
        int: Exit code (0 for success)
    """
    import os
    base_dir = Path(os.getenv('SCRATCHPAD_DIR', Path(__file__).parent.parent))
    frameworks_dir = base_dir / 'frameworks'
    
    fixed_count = 0
    skipped_count = 0
    
    print("Fixing YAML formatting to use literal block scalars...")
    print()
    
    for yaml_file in sorted(frameworks_dir.glob('**/*.yml')):
        if fix_yaml_file(yaml_file):
            print(f"✅ Fixed: {yaml_file.name}")
            fixed_count += 1
        else:
            print(f"⏭️  Already clean: {yaml_file.name}")
            skipped_count += 1
    
    print()
    print(f"✨ Complete! Fixed {fixed_count} files, {skipped_count} already clean")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())