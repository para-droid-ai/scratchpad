#!/usr/bin/env python3
"""
Framework Documentation Generator

Automatically generates markdown documentation from YAML framework metadata.
Useful for creating quick reference guides and maintaining documentation consistency.

Author: Warp AI Agent
Date: 2025-10-01
"""

import yaml
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def load_framework(yaml_path):
    """Load and parse a YAML framework file.
    
    Args:
        yaml_path: Path to the YAML framework file
        
    Returns:
        dict: Parsed YAML data structure
        
    Raises:
        yaml.YAMLError: If YAML parsing fails
        FileNotFoundError: If file doesn't exist
    """
    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def generate_framework_summary(base_dir):
    """Generate markdown summary of all frameworks.
    
    Args:
        base_dir: Base directory path containing frameworks subdirectory
        
    Returns:
        str: Formatted markdown documentation
    """
    frameworks_dir = Path(base_dir) / 'frameworks'
    
    # Organize by category
    categories = defaultdict(list)
    
    for yaml_file in frameworks_dir.glob('**/*.yml'):
        try:
            data = load_framework(yaml_file)
            category = yaml_file.parent.name
            
            framework_info = {
                'name': data.get('name', yaml_file.stem),
                'version': data.get('version', 'N/A'),
                'file': yaml_file.name,
                'purpose': data.get('documentation', {}).get('purpose', 'No description'),
                'use_case': data.get('documentation', {}).get('use_case', 'No use case specified'),
                'character_count': data.get('documentation', {}).get('character_count', 'Unknown'),
            }
            
            categories[category].append(framework_info)
        except Exception as e:
            print(f"Warning: Could not process {yaml_file}: {e}")
    
    # Generate markdown
    md_lines = [
        "# Framework Quick Reference\n",
        "_Auto-generated documentation from YAML metadata_\n",
        f"**Last Updated**: {datetime.fromtimestamp(Path(__file__).stat().st_mtime).isoformat()}\n",
        "---\n\n"
    ]
    
    # Table of contents
    md_lines.append("## Table of Contents\n\n")
    for category in sorted(categories.keys()):
        md_lines.append(f"- [{category.title()}](#{category})\n")
    md_lines.append("\n---\n\n")
    
    # Framework details by category
    for category in sorted(categories.keys()):
        md_lines.append(f"## {category.title()}\n\n")
        
        for fw in sorted(categories[category], key=lambda x: x['name']):
            md_lines.append(f"### {fw['name']}\n\n")
            md_lines.append(f"**File**: `{fw['file']}` | **Version**: {fw['version']} | **Size**: ~{fw['character_count']} chars\n\n")
            
            if fw['purpose'] and fw['purpose'] != 'No description':
                md_lines.append(f"**Purpose**: {fw['purpose']}\n\n")
            
            if fw['use_case'] and fw['use_case'] != 'No use case specified':
                md_lines.append(f"**Use Cases**: {fw['use_case']}\n\n")
            
            md_lines.append("---\n\n")
    
    return ''.join(md_lines)

def generate_comparison_table(base_dir):
    """Generate a comparison table of all frameworks.
    
    Args:
        base_dir: Base directory path containing frameworks subdirectory
        
    Returns:
        str: Markdown-formatted comparison table
    """
    frameworks_dir = Path(base_dir) / 'frameworks'
    
    frameworks = []
    for yaml_file in frameworks_dir.glob('**/*.yml'):
        try:
            data = load_framework(yaml_file)
            frameworks.append({
                'name': data.get('name', yaml_file.stem),
                'category': yaml_file.parent.name,
                'version': data.get('version', ''),
                'chars': data.get('documentation', {}).get('character_count', '?'),
            })
        except (yaml.YAMLError, FileNotFoundError, KeyError) as e:
            print(f"Warning: Could not process {yaml_file}: {e}")
            continue
    
    # Sort by category then name
    frameworks.sort(key=lambda x: (x['category'], x['name']))
    
    md_lines = [
        "# Framework Comparison Table\n\n",
        "| Framework | Category | Version | Size (chars) |\n",
        "|-----------|----------|---------|-------------|\n"
    ]
    
    for fw in frameworks:
        md_lines.append(f"| {fw['name']} | {fw['category']} | {fw['version']} | {fw['chars']} |\n")
    
    return ''.join(md_lines)

def main():
    """Generate all documentation.
    
    Returns:
        int: Exit code (0 for success)
    """
    base_dir = Path(__file__).parent.parent
    output_dir = base_dir / 'docs'
    output_dir.mkdir(exist_ok=True)
    
    print("Generating framework documentation...")
    
    # Generate summary
    summary = generate_framework_summary(base_dir)
    summary_path = output_dir / 'FRAMEWORK_REFERENCE.md'
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"✅ Generated: {summary_path}")
    
    # Generate comparison table
    comparison = generate_comparison_table(base_dir)
    comparison_path = output_dir / 'FRAMEWORK_COMPARISON.md'
    with open(comparison_path, 'w', encoding='utf-8') as f:
        f.write(comparison)
    print(f"✅ Generated: {comparison_path}")
    
    print("\n✨ Documentation generation complete!")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
