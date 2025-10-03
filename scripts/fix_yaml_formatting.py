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
    
    # Prepare to preserve all original keys and format framework.content as a literal block scalar
    from yaml.representer import SafeRepresenter

    class LiteralStr(str): pass
    def literal_str_representer(dumper, data):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    yaml.add_representer(LiteralStr, literal_str_representer)

    # Copy all original data, use safe access, and update only necessary fields
    new_data = dict(data)  # shallow copy preserves unknown keys
    new_data['name'] = data.get('name', '')
    new_data['version'] = str(data.get('version', ''))
    new_data['category'] = data.get('category', '')
    # Documentation block
    new_data['documentation'] = data.get('documentation', {})
    # Framework block
    framework = data.get('framework', {})
    content = framework.get('content', '')
    # Use custom type for literal block scalar
    framework_new = dict(framework)
    framework_new['content'] = LiteralStr(content)
    new_data['framework'] = framework_new

    # Write the properly formatted YAML, preserving unknown keys
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(new_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
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