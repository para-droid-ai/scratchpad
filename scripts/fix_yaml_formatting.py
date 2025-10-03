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
    
    # Custom string classes for different formatting needs
    class LiteralStr(str): 
        """String subclass for literal block scalar style (|)."""
        pass
    
    class QuotedStr(str):
        """String subclass for double-quoted style."""
        pass
    
    # Configure YAML dumper with custom representers
    class CustomDumper(yaml.SafeDumper):
        pass
    
    def literal_str_representer(dumper, data):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    
    def quoted_str_representer(dumper, data):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
    
    CustomDumper.add_representer(LiteralStr, literal_str_representer)
    CustomDumper.add_representer(QuotedStr, quoted_str_representer)

    # Copy all original data, use safe access, and update only necessary fields
    new_data = dict(data)  # shallow copy preserves unknown keys
    new_data['name'] = QuotedStr(data.get('name', ''))
    new_data['version'] = QuotedStr(str(data.get('version', '')))
    new_data['category'] = QuotedStr(data.get('category', ''))
    
    # Documentation block - quote string values
    doc = data.get('documentation', {})
    new_doc = {}
    for key, value in doc.items():
        if isinstance(value, str):
            new_doc[key] = QuotedStr(value)
        else:
            new_doc[key] = value
    new_data['documentation'] = new_doc
    
    # Framework block
    framework = data.get('framework', {})
    content = framework.get('content', '')
    # Use custom type for literal block scalar
    framework_new = dict(framework)
    framework_new['content'] = LiteralStr(content)
    new_data['framework'] = framework_new

    # Serialize the new YAML content to a string
    new_yaml_str = yaml.dump(new_data, Dumper=CustomDumper, default_flow_style=False, sort_keys=False, allow_unicode=True)
    # Read the current file content
    with open(yaml_path, 'r', encoding='utf-8') as f:
        current_yaml_str = f.read()
    # Only write if the content has changed
    if current_yaml_str != new_yaml_str:
        with open(yaml_path, 'w', encoding='utf-8') as f:
            f.write(new_yaml_str)
        return True
    return False

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