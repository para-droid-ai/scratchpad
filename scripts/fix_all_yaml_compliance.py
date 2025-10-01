#!/usr/bin/env python3
"""
Comprehensive YAML 1.2.2 Compliance Remediation Script

Fixes all identified YAML compliance issues:
- Adds document start markers (---)
- Converts backslash escapes to block scalars
- Quotes ambiguous values
- Fixes indentation
- Removes NBSP characters
- Standardizes formatting

Author: YAML Codex Agent
Date: 2025-10-01
"""

import yaml
import re
import sys
from pathlib import Path
from typing import Dict, Any, List
import json

class YAMLRemediator:
    """Comprehensive YAML 1.2.2 compliance remediation tool."""
    
    # Values that need quoting to avoid type coercion
    AMBIGUOUS_VALUES = {
        'YES', 'Yes', 'yes', 'NO', 'No', 'no',
        'ON', 'On', 'on', 'OFF', 'Off', 'off',
        'TRUE', 'True', 'true', 'FALSE', 'False', 'false',
        'Y', 'y', 'N', 'n', '~', 'null', 'NULL', 'Null'
    }
    
    def __init__(self, verbose: bool = True):
        """Initialize the remediator.
        
        Args:
            verbose: If True, print detailed progress information
        """
        self.verbose = verbose
        self.stats = {
            'files_processed': 0,
            'files_fixed': 0,
            'doc_markers_added': 0,
            'escapes_fixed': 0,
            'values_quoted': 0,
            'nbsp_removed': 0,
            'errors': []
        }
    
    def log(self, message: str) -> None:
        """Log a message if verbose mode is enabled."""
        if self.verbose:
            print(message)
    
    def fix_yaml_file(self, filepath: Path) -> bool:
        """Fix all compliance issues in a single YAML file.
        
        Args:
            filepath: Path to the YAML file to fix
            
        Returns:
            True if file was fixed successfully, False otherwise
        """
        self.log(f"Processing: {filepath.name}")
        
        try:
            # Read the original file
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Track if we made changes
            original_content = content
            
            # Step 1: Remove NBSP characters (U+00A0)
            if '\u00a0' in content:
                content = content.replace('\u00a0', ' ')
                self.stats['nbsp_removed'] += 1
                self.log("  ✓ Removed NBSP characters")
            
            # Step 2: Parse YAML to understand structure
            try:
                data = yaml.safe_load(content)
                if not data:
                    data = {}
            except yaml.YAMLError as e:
                self.log(f"  ⚠ Warning: Could not parse YAML: {e}")
                data = {}
            
            # Step 3: Rebuild YAML with proper formatting
            yaml_lines = []
            
            # Add document start marker
            if not content.strip().startswith('---'):
                yaml_lines.append('---')
                self.stats['doc_markers_added'] += 1
            else:
                yaml_lines.append('---')
            
            # Process main structure
            if isinstance(data, dict):
                yaml_lines.extend(self._format_dict(data, 0))
            
            # Join lines and ensure proper formatting
            new_content = '\n'.join(yaml_lines)
            if not new_content.endswith('\n'):
                new_content += '\n'
            
            # Step 4: Fix remaining issues with regex
            new_content = self._fix_escaped_content(new_content)
            
            # Write back if changed
            if new_content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                self.stats['files_fixed'] += 1
                self.log(f"  ✅ Fixed: {filepath.name}")
                return True
            else:
                self.log(f"  ⏭ No changes needed: {filepath.name}")
                return False
                
        except Exception as e:
            error_msg = f"Error processing {filepath}: {e}"
            self.stats['errors'].append(error_msg)
            self.log(f"  ❌ {error_msg}")
            return False
        finally:
            self.stats['files_processed'] += 1
    
    def _format_dict(self, data: Dict[str, Any], indent: int) -> List[str]:
        """Format a dictionary as YAML lines.
        
        Args:
            data: Dictionary to format
            indent: Current indentation level
            
        Returns:
            List of formatted YAML lines
        """
        lines = []
        spaces = '  ' * indent
        
        for key, value in data.items():
            if value is None:
                lines.append(f'{spaces}{key}: null')
            elif isinstance(value, bool):
                lines.append(f'{spaces}{key}: {str(value).lower()}')
            elif isinstance(value, (int, float)):
                # Quote version-like numbers
                if key in ['version', 'v'] or str(value) in ['1.0', '2.0', '2.5']:
                    lines.append(f'{spaces}{key}: "{value}"')
                    self.stats['values_quoted'] += 1
                else:
                    lines.append(f'{spaces}{key}: {value}')
            elif isinstance(value, str):
                # Check if it needs special handling
                if self._needs_quoting(value):
                    lines.append(f'{spaces}{key}: "{self._escape_quotes(value)}"')
                    self.stats['values_quoted'] += 1
                elif self._is_multiline(value):
                    # Use block scalar for multiline content
                    lines.append(f'{spaces}{key}: |+')
                    for line in value.split('\n'):
                        lines.append(f'{spaces}  {line}')
                    self.stats['escapes_fixed'] += 1
                else:
                    # Regular string
                    lines.append(f'{spaces}{key}: "{self._escape_quotes(value)}"')
            elif isinstance(value, list):
                lines.append(f'{spaces}{key}:')
                for item in value:
                    if isinstance(item, dict):
                        lines.append(f'{spaces}  -')
                        dict_lines = self._format_dict(item, indent + 2)
                        # Adjust first line
                        if dict_lines:
                            first_line = dict_lines[0].lstrip()
                            lines[-1] += f' {first_line}'
                            lines.extend(dict_lines[1:])
                    else:
                        formatted_item = self._format_scalar(item)
                        lines.append(f'{spaces}  - {formatted_item}')
            elif isinstance(value, dict):
                lines.append(f'{spaces}{key}:')
                lines.extend(self._format_dict(value, indent + 1))
            else:
                lines.append(f'{spaces}{key}: {value}')
        
        return lines
    
    def _format_scalar(self, value: Any) -> str:
        """Format a scalar value for YAML.
        
        Args:
            value: Value to format
            
        Returns:
            Formatted string representation
        """
        if value is None:
            return 'null'
        elif isinstance(value, bool):
            return str(value).lower()
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            if self._needs_quoting(value):
                return f'"{self._escape_quotes(value)}"'
            else:
                return f'"{self._escape_quotes(value)}"'
        else:
            return str(value)
    
    def _needs_quoting(self, value: str) -> bool:
        """Check if a string value needs quoting.
        
        Args:
            value: String to check
            
        Returns:
            True if value needs quoting
        """
        # Check for ambiguous values
        if value in self.AMBIGUOUS_VALUES:
            return True
        
        # Check for special characters
        if any(char in value for char in [':', '#', '@', '|', '>', '-', '[', ']', '{', '}', ',']):
            return True
        
        # Check if it looks like a number
        try:
            float(value)
            return True
        except ValueError:
            pass
        
        return False
    
    def _is_multiline(self, value: str) -> bool:
        """Check if a string should use block scalar notation.
        
        Args:
            value: String to check
            
        Returns:
            True if string should use block scalar
        """
        # Check for escaped newlines or actual newlines
        return ('\\n' in value or '\n' in value or 
                '\\t' in value or len(value) > 80)
    
    def _escape_quotes(self, value: str) -> str:
        """Escape quotes in a string value.
        
        Args:
            value: String to escape
            
        Returns:
            String with escaped quotes
        """
        return value.replace('"', '\\"')
    
    def _fix_escaped_content(self, content: str) -> str:
        """Fix escaped content using regex patterns.
        
        Args:
            content: YAML content to fix
            
        Returns:
            Fixed content
        """
        # Pattern to find content fields with escapes
        pattern = r'(\s+content:\s*)"([^"]*(?:\\[nt"])[^"]*)"'
        
        def replace_escapes(match):
            indent = match.group(1)
            value = match.group(2)
            
            # Unescape the content
            value = value.replace('\\n', '\n')
            value = value.replace('\\t', '\t')
            value = value.replace('\\"', '"')
            value = value.replace('\\\\', '\\')
            
            # Format as block scalar
            lines = [f'{indent}content: |+']
            for line in value.split('\n'):
                lines.append(f'{indent}  {line}')
            
            self.stats['escapes_fixed'] += 1
            return '\n'.join(lines)
        
        # Apply the fix
        content = re.sub(pattern, replace_escapes, content, flags=re.MULTILINE | re.DOTALL)
        
        return content
    
    def process_directory(self, directory: Path) -> None:
        """Process all YAML files in a directory recursively.
        
        Args:
            directory: Directory to process
        """
        yaml_files = list(directory.glob('**/*.yml')) + list(directory.glob('**/*.yaml'))
        
        self.log("\n🔧 YAML Compliance Remediation")
        self.log(f"Found {len(yaml_files)} YAML files to process\n")
        
        for yaml_file in sorted(yaml_files):
            self.fix_yaml_file(yaml_file)
        
        self.print_summary()
    
    def print_summary(self) -> None:
        """Print a summary of the remediation results."""
        print("\n" + "="*50)
        print("📊 Remediation Summary")
        print("="*50)
        print(f"Files Processed: {self.stats['files_processed']}")
        print(f"Files Fixed: {self.stats['files_fixed']}")
        print(f"Document Markers Added: {self.stats['doc_markers_added']}")
        print(f"Escaped Sequences Fixed: {self.stats['escapes_fixed']}")
        print(f"Values Quoted: {self.stats['values_quoted']}")
        print(f"NBSP Characters Removed: {self.stats['nbsp_removed']}")
        
        if self.stats['errors']:
            print(f"\n⚠ Errors ({len(self.stats['errors'])}):")
            for error in self.stats['errors']:
                print(f"  - {error}")
        
        success_rate = (self.stats['files_processed'] - len(self.stats['errors'])) / max(self.stats['files_processed'], 1) * 100
        print(f"\n✨ Success Rate: {success_rate:.1f}%")
        
        # Save stats to file
        stats_file = Path(__file__).parent.parent / 'docs' / 'yaml-remediation-report.json'
        with open(stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
        print(f"\n📄 Detailed report saved to: {stats_file}")


def main():
    """Main entry point for the remediation script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Fix YAML compliance issues')
    parser.add_argument(
        'directory',
        nargs='?',
        default='frameworks',
        help='Directory to process (default: frameworks)'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress verbose output'
    )
    
    args = parser.parse_args()
    
    # Get the base directory
    base_dir = Path(__file__).parent.parent
    target_dir = base_dir / args.directory
    
    if not target_dir.exists():
        print(f"❌ Error: Directory not found: {target_dir}")
        return 1
    
    # Run remediation
    remediator = YAMLRemediator(verbose=not args.quiet)
    remediator.process_directory(target_dir)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())