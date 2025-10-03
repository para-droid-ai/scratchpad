#!/usr/bin/env python3
"""
Edge Case Test Suite

Tests edge cases and error handling for all script functions.
Focuses on improving test coverage for error paths and boundary conditions.

Author: GitHub Copilot
Date: 2025-10-03
"""

import unittest
import sys
import tempfile
import shutil
from pathlib import Path
import yaml

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts import (
    fix_yaml_formatting,
    add_framework_metadata,
    generate_framework_docs,
    add_yaml_doc_markers,
    convert_frameworks_to_proper_yaml
)


class TestFixYAMLFormattingEdgeCases(unittest.TestCase):
    """Test edge cases for fix_yaml_formatting.py"""
    
    def setUp(self):
        """Set up temporary test directory."""
        self.test_dir = Path(tempfile.mkdtemp())
        
    def tearDown(self):
        """Clean up temporary test directory."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_empty_file(self):
        """Test handling of empty YAML file."""
        empty_file = self.test_dir / 'empty.yml'
        empty_file.write_text('')
        
        # Should return False (no changes needed)
        result = fix_yaml_formatting.fix_yaml_file(empty_file)
        self.assertFalse(result)
    
    def test_none_data(self):
        """Test handling of file that parses to None."""
        none_file = self.test_dir / 'none.yml'
        none_file.write_text('# Just a comment\n')
        
        # Should return False and not crash
        result = fix_yaml_formatting.fix_yaml_file(none_file)
        self.assertFalse(result)
    
    def test_missing_framework_key(self):
        """Test handling of YAML without framework key."""
        test_file = self.test_dir / 'no_framework.yml'
        test_data = {'name': 'Test', 'version': '1.0', 'category': 'test'}
        with open(test_file, 'w') as f:
            yaml.dump(test_data, f)
        
        # Should handle gracefully
        try:
            result = fix_yaml_formatting.fix_yaml_file(test_file)
            # Function should complete without error
            self.assertIsNotNone(result)
        except KeyError:
            self.fail("fix_yaml_file raised KeyError unexpectedly")
    
    def test_unicode_content(self):
        """Test handling of Unicode characters in content."""
        test_file = self.test_dir / 'unicode.yml'
        test_data = {
            'name': 'Unicode Test',
            'version': '1.0',
            'category': 'test',
            'documentation': {'purpose': 'Test with émojis 🎉'},
            'framework': {'content': 'Content with special chars: café, naïve, 中文'}
        }
        with open(test_file, 'w', encoding='utf-8') as f:
            yaml.dump(test_data, f)
        
        result = fix_yaml_formatting.fix_yaml_file(test_file)
        
        # Should handle Unicode correctly
        content = test_file.read_text(encoding='utf-8')
        self.assertIn('café', content)
        self.assertIn('中文', content)


class TestAddFrameworkMetadataEdgeCases(unittest.TestCase):
    """Test edge cases for add_framework_metadata.py"""
    
    def setUp(self):
        """Set up temporary test directory."""
        self.test_dir = Path(tempfile.mkdtemp())
        
    def tearDown(self):
        """Clean up temporary test directory."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_empty_yaml(self):
        """Test handling of empty YAML that parses to None."""
        empty_file = self.test_dir / 'empty.yml'
        empty_file.write_text('# Just comments\n')
        
        # Should handle None data gracefully
        result = add_framework_metadata.add_metadata_to_framework(empty_file)
        self.assertTrue(result)  # Should add metadata even to empty file
        
        # Check that metadata was added
        with open(empty_file, 'r') as f:
            data = yaml.safe_load(f)
        self.assertIsNotNone(data)
        self.assertIn('documentation', data)
    
    def test_partial_metadata(self):
        """Test handling of file with partial metadata."""
        test_file = self.test_dir / 'partial.yml'
        test_data = {
            'name': 'Partial Test',
            'version': '1.0',
            'category': 'test',
            'documentation': {
                'purpose': 'Already has purpose'
                # Missing use_case
            }
        }
        with open(test_file, 'w') as f:
            yaml.dump(test_data, f)
        
        result = add_framework_metadata.add_metadata_to_framework(test_file)
        
        # Should add missing use_case
        self.assertTrue(result)
        
        with open(test_file, 'r') as f:
            data = yaml.safe_load(f)
        
        self.assertIn('use_case', data['documentation'])
        self.assertEqual(data['documentation']['purpose'], 'Already has purpose')
    
    def test_no_matching_template(self):
        """Test handling of framework with no matching template."""
        test_file = self.test_dir / 'custom-unique-name-xyz.yml'
        test_data = {
            'name': 'Custom Framework',
            'category': 'custom'
        }
        with open(test_file, 'w') as f:
            yaml.dump(test_data, f)
        
        result = add_framework_metadata.add_metadata_to_framework(test_file)
        
        # Should generate generic metadata
        self.assertTrue(result)
        
        with open(test_file, 'r') as f:
            data = yaml.safe_load(f)
        
        self.assertIn('documentation', data)
        self.assertIn('purpose', data['documentation'])
        self.assertIn('version', data)


class TestGenerateFrameworkDocsEdgeCases(unittest.TestCase):
    """Test edge cases for generate_framework_docs.py"""
    
    def setUp(self):
        """Set up temporary test directory."""
        self.test_dir = Path(tempfile.mkdtemp())
        
    def tearDown(self):
        """Clean up temporary test directory."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_empty_frameworks_directory(self):
        """Test handling of empty frameworks directory."""
        frameworks_dir = self.test_dir / 'frameworks'
        frameworks_dir.mkdir()
        
        # Should handle empty directory gracefully
        summary = generate_framework_docs.generate_framework_summary(self.test_dir)
        
        self.assertIn('Framework Quick Reference', summary)
        self.assertIn('Table of Contents', summary)
    
    def test_invalid_yaml_file(self):
        """Test handling of invalid YAML file."""
        frameworks_dir = self.test_dir / 'frameworks'
        frameworks_dir.mkdir()
        
        bad_file = frameworks_dir / 'bad.yml'
        bad_file.write_text('invalid: yaml: content: [[[')
        
        # Should skip invalid file and continue
        try:
            summary = generate_framework_docs.generate_framework_summary(self.test_dir)
            self.assertIsNotNone(summary)
        except yaml.YAMLError:
            self.fail("generate_framework_summary should handle invalid YAML gracefully")
    
    def test_missing_documentation_fields(self):
        """Test handling of framework with missing documentation fields."""
        frameworks_dir = self.test_dir / 'frameworks'
        frameworks_dir.mkdir()
        
        minimal_file = frameworks_dir / 'minimal.yml'
        test_data = {
            'name': 'Minimal Framework',
            'framework': {'content': 'Some content'}
        }
        with open(minimal_file, 'w') as f:
            yaml.dump(test_data, f)
        
        summary = generate_framework_docs.generate_framework_summary(self.test_dir)
        
        # Should use default values for missing fields
        self.assertIn('Minimal Framework', summary)
        self.assertIn('N/A', summary)  # Default version


class TestAddYAMLDocMarkersEdgeCases(unittest.TestCase):
    """Test edge cases for add_yaml_doc_markers.py"""
    
    def setUp(self):
        """Set up temporary test directory."""
        self.test_dir = Path(tempfile.mkdtemp())
        
    def tearDown(self):
        """Clean up temporary test directory."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_already_has_marker(self):
        """Test file that already has document marker."""
        test_file = self.test_dir / 'has_marker.yml'
        test_file.write_text('---\nname: Test\n')
        
        result = add_yaml_doc_markers.add_doc_marker(test_file)
        
        # Should return False (no changes)
        self.assertFalse(result)
        
        # Content should be unchanged
        content = test_file.read_text()
        self.assertEqual(content.count('---'), 1)
    
    def test_marker_with_whitespace(self):
        """Test file that has marker after whitespace."""
        test_file = self.test_dir / 'whitespace.yml'
        test_file.write_text('  \n---\nname: Test\n')
        
        result = add_yaml_doc_markers.add_doc_marker(test_file)
        
        # Should return False (already has marker after stripping)
        self.assertFalse(result)
    
    def test_empty_file_marker(self):
        """Test adding marker to empty file."""
        test_file = self.test_dir / 'empty.yml'
        test_file.write_text('')
        
        result = add_yaml_doc_markers.add_doc_marker(test_file)
        
        # Should add marker
        self.assertTrue(result)
        
        content = test_file.read_text()
        self.assertTrue(content.startswith('---\n'))


class TestConvertFrameworksEdgeCases(unittest.TestCase):
    """Test edge cases for convert_frameworks_to_proper_yaml.py"""
    
    def setUp(self):
        """Set up temporary test directory."""
        self.test_dir = Path(tempfile.mkdtemp())
        
    def tearDown(self):
        """Clean up temporary test directory."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_non_dict_yaml(self):
        """Test handling of YAML that's not a dictionary."""
        test_file = self.test_dir / 'list.yml'
        test_file.write_text('- item1\n- item2\n')
        
        result = convert_frameworks_to_proper_yaml.convert_framework(test_file)
        
        # Should return False (no conversion for non-dict)
        self.assertFalse(result)
    
    def test_no_framework_key(self):
        """Test handling of file without framework key."""
        test_file = self.test_dir / 'no_framework.yml'
        test_data = {'name': 'Test', 'category': 'test'}
        with open(test_file, 'w') as f:
            yaml.dump(test_data, f)
        
        result = convert_frameworks_to_proper_yaml.convert_framework(test_file)
        
        # Should return False (no conversion needed)
        self.assertFalse(result)
    
    def test_already_converted(self):
        """Test handling of already converted framework."""
        test_file = self.test_dir / 'converted.yml'
        test_data = {
            'name': 'Test',
            'framework': {
                'structure': {'role': 'assistant'},
                'legacy_content': 'old content'
            }
        }
        with open(test_file, 'w') as f:
            yaml.dump(test_data, f)
        
        result = convert_frameworks_to_proper_yaml.convert_framework(test_file)
        
        # Should return False (already has structure key)
        self.assertFalse(result)
    
    def test_plain_content_no_xml(self):
        """Test handling of plain content without XML tags."""
        test_file = self.test_dir / 'plain.yml'
        test_data = {
            'name': 'Test',
            'framework': {
                'content': 'Just plain text content without any XML tags'
            }
        }
        with open(test_file, 'w') as f:
            yaml.dump(test_data, f)
        
        result = convert_frameworks_to_proper_yaml.convert_framework(test_file)
        
        # Should return False (no XML to convert)
        self.assertFalse(result)


class TestCleanTextFunction(unittest.TestCase):
    """Test the clean_text utility function."""
    
    def test_multiple_blank_lines(self):
        """Test collapsing multiple blank lines."""
        text = "line1\n\n\n\nline2"
        result = convert_frameworks_to_proper_yaml.clean_text(text)
        
        # Should collapse to double newline
        self.assertNotIn('\n\n\n\n', result)
        self.assertIn('line1', result)
        self.assertIn('line2', result)
    
    def test_trailing_whitespace(self):
        """Test removal of trailing whitespace."""
        text = "line1   \nline2  \n"
        result = convert_frameworks_to_proper_yaml.clean_text(text)
        
        # Should remove trailing spaces from lines
        self.assertIn('line1\n', result)
        self.assertIn('line2', result)


class TestParseScratchpadSections(unittest.TestCase):
    """Test the parse_scratchpad_sections utility function."""
    
    def test_bracketed_sections(self):
        """Test parsing bracketed section format."""
        content = "[Section1: desc1] some text [Section2: desc2]"
        result = convert_frameworks_to_proper_yaml.parse_scratchpad_sections(content)
        
        self.assertEqual(len(result), 2)
        self.assertIn('Section1', result)
        self.assertIn('Section2', result)
    
    def test_no_sections(self):
        """Test content without bracketed sections."""
        content = "Just plain text without any brackets"
        result = convert_frameworks_to_proper_yaml.parse_scratchpad_sections(content)
        
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()
