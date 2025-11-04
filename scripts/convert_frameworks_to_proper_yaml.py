#!/usr/bin/env python3
"""
Convert framework files from XML-in-strings to proper YAML nesting.

This script converts frameworks that use XML embedded in string literals
to proper YAML structures with nested dictionaries and lists.
"""

import yaml
import re
from pathlib import Path
from typing import Dict, Any, List


def clean_text(text: str) -> str:
    """Clean and normalize text content.
    
    Removes excessive whitespace and normalizes line endings for cleaner
    YAML output. This includes:
    - Collapsing multiple blank lines into double newlines
    - Removing trailing whitespace from each line
    - Trimming leading/trailing whitespace from the entire text
    
    Args:
        text: The text string to clean and normalize
        
    Returns:
        str: Cleaned and normalized text
    """
    # Remove excessive whitespace
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    # Remove trailing/leading whitespace from each line
    lines = [line.rstrip() for line in text.split('\n')]
    return '\n'.join(lines).strip()


def parse_scratchpad_sections(content: str) -> List[str]:
    """Extract scratchpad section names from bracketed format.
    
    Parses content using bracketed scratchpad format like:
    [Section Name: description]
    
    and extracts just the section names.
    
    Args:
        content: String containing bracketed section markers
        
    Returns:
        List[str]: List of section names found in the content
    """
    pattern = r'\[([^:]+):.*?\]'
    sections = re.findall(pattern, content)
    return [s.strip() for s in sections]


def parse_xml_to_yaml(content: str) -> Dict[str, Any]:
    """
    Parse XML-like content and convert to YAML structure.
    
    Converts embedded XML-like markup to proper YAML dictionaries and lists.
    Handles several formats:
    - Simple tags: <role>text</role> -> {"role": "text"}
    - Tags with spaces: <scratchpad flow>...</scratchpad flow> -> {"scratchpad_flow": {...}}
    - Nested tags: Recursively processes nested XML structures
    - Bracketed sections: [Section: description] format for scratchpad templates
    
    The function intelligently detects content types:
    - Nested XML: Recursively parsed
    - Bracketed sections: Extracted as section lists
    - Plain text: Stored as string content
    
    Args:
        content: String containing XML-like markup to parse
        
    Returns:
        Dict[str, Any]: Parsed YAML structure as nested dictionaries and lists
    """
    result = {}

    # Pattern to match XML-like tags (including tags with spaces)
    tag_pattern = r'<([^/>]+)>(.*?)</\1>'

    matches = re.findall(tag_pattern, content, re.DOTALL | re.IGNORECASE)

    if not matches:
        # No XML tags found, check for bracketed sections
        if '[' in content and ']' in content:
            sections = parse_scratchpad_sections(content)
            if sections:
                return {"sections": sections, "raw_format": clean_text(content)}
        return {"content": clean_text(content)}

    for tag_name, tag_content in matches:
        # Clean tag name
        clean_tag = tag_name.strip().lower()
        clean_tag = re.sub(r'[\s-]+', '_', clean_tag)

        tag_content = tag_content.strip()

        # Check if content has nested tags
        if re.search(r'<[^/>]+>.*?</[^>]+>', tag_content, re.DOTALL):
            # Recursively parse nested content
            nested = parse_xml_to_yaml(tag_content)
            result[clean_tag] = nested
        # Check for bracketed sections (scratchpad format)
        elif '[' in tag_content and ']:' in tag_content:
            sections = parse_scratchpad_sections(tag_content)
            # Extract instructions before the template
            instructions_match = re.search(r'^(.+?)```', tag_content, re.DOTALL)
            instructions = clean_text(instructions_match.group(1)) if instructions_match else None

            result[clean_tag] = {
                "format": "bracketed_sections",
                "sections": sections,
            }
            if instructions:
                result[clean_tag]["usage"] = instructions
            result[clean_tag]["template"] = clean_text(tag_content)
        else:
            # Simple text content
            result[clean_tag] = clean_text(tag_content)

    # Handle content outside tags (instructions, separators)
    remaining = re.sub(tag_pattern, '', content, flags=re.DOTALL).strip()
    remaining = re.sub(r'-{3,}', '', remaining).strip()  # Remove separator lines
    remaining = clean_text(remaining)

    if remaining:
        result["instructions"] = remaining

    return result


def convert_framework(yaml_file: Path) -> bool:
    """
    Convert a single framework file to proper YAML structure.
    
    This function checks if a framework file needs conversion from the legacy
    XML-embedded format to modern structured YAML. It:
    - Loads the existing YAML file
    - Checks for framework.content field with XML or bracketed content
    - Parses the content into structured YAML
    - Updates the framework with a 'structure' field
    - Preserves original content in 'legacy_content' for reference
    - Writes back with proper YAML formatting including document start marker
    
    Files that don't need conversion (already converted or no XML content)
    are skipped without modification.
    
    Args:
        yaml_file: Path object pointing to the framework YAML file
        
    Returns:
        bool: True if conversion was performed, False if file was skipped
        
    Raises:
        yaml.YAMLError: If YAML parsing or dumping fails
        IOError: If file read/write operations fail
    """
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        return False

    # Check if framework.content exists
    if 'framework' not in data or 'content' not in data['framework']:
        return False

    content = data['framework']['content']

    # Check if already converted (has 'structure' key)
    if 'structure' in data['framework']:
        return False

    # Check if content contains XML-like tags or needs conversion
    has_xml = re.search(r'<[^/>]+>.*?</[^>]+>', content, re.DOTALL)
    has_brackets = '[' in content and ']:' in content

    if not (has_xml or has_brackets):
        # Plain content, no conversion needed
        return False

    print(f"Converting: {yaml_file.name}")

    # Parse the content to YAML structure
    parsed = parse_xml_to_yaml(content)

    # Update framework with proper YAML structure
    data['framework']['structure'] = parsed
    # Keep original for reference
    data['framework']['legacy_content'] = content
    # Remove old content key
    del data['framework']['content']

    # Write back as proper YAML
    with open(yaml_file, 'w', encoding='utf-8') as f:
        # Add document start marker
        f.write('---\n')
        yaml.dump(data, f,
                  default_flow_style=False,
                  allow_unicode=True,
                  sort_keys=False,
                  width=120,
                  indent=2,
                  explicit_start=False)  # We already wrote ---

    return True


def main():
    """Main conversion routine.
    
    Processes all framework YAML files in the frameworks directory,
    converting them from legacy XML-embedded format to modern structured YAML.
    
    The function:
    - Validates the frameworks directory exists
    - Recursively finds all .yml files
    - Converts each file that needs conversion
    - Provides summary statistics of conversion results
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
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
