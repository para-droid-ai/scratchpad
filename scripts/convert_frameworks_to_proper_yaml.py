#!/usr/bin/env python3
"""
Convert framework files from XML-in-strings to proper YAML nesting.

This script converts frameworks that use XML embedded in string literals
to proper YAML structures with nested dictionaries and lists.
"""

import yaml
import re
from pathlib import Path
from typing import Dict, Any


def parse_xml_content(content: str) -> Dict[str, Any]:
    """
    Parse XML-like content and convert to YAML structure.

    For frameworks using XML tags like <role>, <scratchpad flow>, <task>,
    this converts them to proper YAML nested structures.
    """
    result = {}

    # Pattern to match XML-like tags
    tag_pattern = r'<(\w+[\s\w-]*)>(.*?)</\1>'

    matches = re.findall(tag_pattern, content, re.DOTALL)

    if not matches:
        # No XML tags found, return as plain content
        return {"content": content.strip()}

    for tag_name, tag_content in matches:
        # Clean tag name (remove extra spaces)
        clean_tag = tag_name.strip().replace(' ', '_').replace('-', '_')

        # Recursively parse nested content
        nested = parse_xml_content(tag_content.strip())

        if len(nested) == 1 and "content" in nested:
            # Simple content, no nesting
            result[clean_tag] = nested["content"]
        else:
            # Has nested structure
            result[clean_tag] = nested

    # Handle content outside tags
    remaining = re.sub(tag_pattern, '', content, flags=re.DOTALL).strip()
    remaining = re.sub(r'-+', '', remaining).strip()  # Remove separator lines

    if remaining and result:
        result["additional_content"] = remaining
    elif remaining and not result:
        result["content"] = remaining

    return result


def convert_framework(yaml_file: Path) -> bool:
    """
    Convert a single framework file to proper YAML structure.

    Returns True if conversion was made, False if no conversion needed.
    """
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        return False

    # Check if framework.content exists and contains XML
    if 'framework' not in data or 'content' not in data['framework']:
        return False

    content = data['framework']['content']

    # Check if content contains XML-like tags
    if not re.search(r'<\w+[\s\w-]*>', content):
        return False

    print(f"Converting: {yaml_file.name}")

    # Parse the XML content
    parsed_content = parse_xml_content(content)

    # Update the framework structure
    if len(parsed_content) > 1 or "content" not in parsed_content:
        # Has structure, use nested YAML
        data['framework'] = {
            **data['framework'],
            'structure': parsed_content
        }
        # Keep original as backup
        data['framework']['original_content'] = content
    else:
        # Just plain content, keep as is but use |+ block scalar
        pass

    # Write back with proper formatting
    with open(yaml_file, 'w', encoding='utf-8') as f:
        # Write document start marker
        f.write('---\n')

        # Write metadata fields
        for key in ['name', 'version', 'category']:
            if key in data:
                value = data[key]
                if isinstance(value, str):
                    f.write(f'{key}: "{value}"\n')
                else:
                    f.write(f'{key}: {value}\n')

        # Write documentation
        if 'documentation' in data:
            f.write('documentation:\n')
            for doc_key, doc_val in data['documentation'].items():
                if isinstance(doc_val, str):
                    f.write(f'  {doc_key}: "{doc_val}"\n')
                else:
                    f.write(f'  {doc_key}: {doc_val}\n')

        # Write framework with proper block scalar
        f.write('framework:\n')

        # If we have structured content
        if 'structure' in data['framework']:
            f.write('  structure:\n')
            # Dump structure as YAML
            struct_yaml = yaml.dump(data['framework']['structure'],
                                     default_flow_style=False,
                                     allow_unicode=True,
                                     width=120,
                                     indent=4)
            for line in struct_yaml.splitlines():
                f.write(f'    {line}\n')

        # Always keep original content with |+ block scalar
        f.write('  content: |+\n')
        for line in content.splitlines():
            f.write(f'    {line}\n')

    return True


def main():
    """Main conversion routine."""
    frameworks_dir = Path(__file__).parent.parent / 'frameworks'

    if not frameworks_dir.exists():
        print(f"Error: {frameworks_dir} does not exist")
        return 1

    converted = 0
    skipped = 0

    for yaml_file in sorted(frameworks_dir.glob('**/*.yml')):
        if convert_framework(yaml_file):
            converted += 1
        else:
            skipped += 1

    print("\nConversion complete:")
    print(f"  Converted: {converted} files")
    print(f"  Skipped: {skipped} files")

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
