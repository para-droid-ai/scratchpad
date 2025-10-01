#!/usr/bin/env python3
"""
Simple YAML Document Marker Addition Script

Adds the required `---` document start marker to YAML files that are missing it.
This is the minimal fix for YAML 1.2.2 compliance.

Author: YAML Codex Agent
Date: 2025-10-01
"""

import sys
from pathlib import Path

def add_doc_marker(filepath: Path) -> bool:
    """Add --- document marker to a YAML file if missing.
    
    Args:
        filepath: Path to the YAML file
        
    Returns:
        bool: True if file was modified
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has document marker
        if content.strip().startswith('---'):
            return False
        
        # Add marker
        new_content = '---\n' + content
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}", file=sys.stderr)
        return False

def main():
    """Main entry point."""
    base_dir = Path(__file__).parent.parent
    frameworks_dir = base_dir / 'frameworks'
    
    yaml_files = list(frameworks_dir.glob('**/*.yml')) + list(frameworks_dir.glob('**/*.yaml'))
    
    modified = 0
    skipped = 0
    
    print(f"Found {len(yaml_files)} YAML files")
    
    for yaml_file in sorted(yaml_files):
        if add_doc_marker(yaml_file):
            print(f"✅ Added marker: {yaml_file.name}")
            modified += 1
        else:
            skipped += 1
    
    print(f"\n✨ Complete! Modified {modified} files, skipped {skipped}")
    return 0

if __name__ == '__main__':
    sys.exit(main())