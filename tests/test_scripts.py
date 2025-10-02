import unittest
import sys
import os
from pathlib import Path
import shutil
import yaml

# Add parent directory to path to allow script imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts import generate_framework_docs, add_framework_metadata, refactor_frameworks

class TestScripts(unittest.TestCase):
    """Test suite for the utility scripts in the scripts/ directory."""

    def setUp(self):
        """Set up a temporary directory for test artifacts."""
        self.test_dir = Path(__file__).parent / 'temp_test_data'
        self.test_dir.mkdir(exist_ok=True)

    def tearDown(self):
        """Remove the temporary directory after tests."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_generate_framework_docs(self):
        """Tests the generate_framework_docs.py script.

        This test creates a temporary directory with dummy framework files,
        runs the documentation generation script, and verifies that the
        output markdown files are created and contain the expected content.
        """
        # 1. Create a dummy frameworks directory structure
        dummy_frameworks_dir = self.test_dir / 'frameworks'
        core_dir = dummy_frameworks_dir / 'core'
        core_dir.mkdir(parents=True)

        # 2. Create a dummy framework file
        dummy_framework_data = {
            'name': 'Dummy Framework',
            'version': '1.0',
            'category': 'core',
            'documentation': {
                'purpose': 'A dummy framework for testing.',
                'use_case': 'Used in the test suite for script validation.',
                'character_count': 123
            },
            'framework': {
                'system_prompt': {
                    'directive': 'Be a dummy.'
                }
            }
        }
        with open(core_dir / 'dummy.yml', 'w') as f:
            yaml.dump(dummy_framework_data, f)

        # 3. Run the documentation generation function
        summary_md = generate_framework_docs.generate_framework_summary(self.test_dir)
        comparison_md = generate_framework_docs.generate_comparison_table(self.test_dir)

        # 4. Assert the output is correct
        # Check the summary document
        self.assertIn("# Framework Quick Reference", summary_md)
        self.assertIn("## Core", summary_md)
        self.assertIn("### Dummy Framework", summary_md)
        self.assertIn("**Purpose**: A dummy framework for testing.", summary_md)

        # Check the comparison table
        self.assertIn("# Framework Comparison Table", comparison_md)
        self.assertIn("| Dummy Framework | Core | `1.0` | 123 |", comparison_md)

    def test_add_framework_metadata(self):
        """Tests the add_framework_metadata.py script.

        This test creates a dummy framework file missing its metadata,
        runs the metadata generation script, and verifies that the
        missing fields are correctly added based on templates.
        """
        # 1. Create a dummy framework file with missing metadata
        dummy_frameworks_dir = self.test_dir / 'frameworks'
        core_dir = dummy_frameworks_dir / 'core'
        core_dir.mkdir(parents=True, exist_ok=True)

        dummy_framework_path = core_dir / 'scratchpad-lite.yml'
        dummy_framework_data = {
            'name': 'Scratchpad Lite',
            'category': 'core',
            'framework': { 'system_prompt': {} }
        }
        with open(dummy_framework_path, 'w') as f:
            yaml.dump(dummy_framework_data, f)

        # 2. Run the metadata addition function
        modified = add_framework_metadata.add_metadata_to_framework(dummy_framework_path)
        self.assertTrue(modified, "The script should have modified the file.")

        # 3. Read the file back and assert that metadata was added
        with open(dummy_framework_path, 'r') as f:
            updated_data = yaml.safe_load(f)

        self.assertIn('version', updated_data)
        self.assertEqual('1.0', updated_data['version'])

        self.assertIn('documentation', updated_data)
        doc = updated_data['documentation']
        self.assertIn('purpose', doc)
        self.assertIn('Lightweight reasoning framework', doc['purpose'])
        self.assertIn('use_case', doc)
        self.assertIn('Quick tasks', doc['use_case'])

    def test_refactor_frameworks(self):
        """Tests the refactor_frameworks.py script.

        This test creates a dummy framework file using the legacy
        XML-in-a-string format and verifies that the refactoring script
        correctly converts it to the new, structured format.
        """
        # 1. Create a dummy legacy framework file
        dummy_frameworks_dir = self.test_dir / 'frameworks'
        core_dir = dummy_frameworks_dir / 'core'
        core_dir.mkdir(parents=True, exist_ok=True)

        dummy_framework_path = core_dir / 'legacy.yml'
        legacy_content = """
        <system_prompt>
            <formatting_rules>
                <rule>Rule 1.</rule>
                <rule>Rule 2.</rule>
            </formatting_rules>
            <execution_flow>
                <scratchpad_logic>
                    <step name="Step1">Description 1</step>
                    <step name="Step2">Description 2</step>
                </scratchpad_logic>
                <final_output>Final output description.</final_output>
            </execution_flow>
            <directive>A final directive.</directive>
        </system_prompt>
        """
        dummy_framework_data = {
            'name': 'Legacy Framework',
            'category': 'core',
            'framework': {
                'legacy_content': legacy_content
            }
        }
        with open(dummy_framework_path, 'w') as f:
            yaml.dump(dummy_framework_data, f)

        # 2. Run the refactoring function
        refactor_frameworks.refactor_framework_file(dummy_framework_path)

        # 3. Read the file back and assert the structure is correct
        with open(dummy_framework_path, 'r') as f:
            updated_data = yaml.safe_load(f)

        self.assertNotIn('legacy_content', updated_data['framework'])
        self.assertIn('system_prompt', updated_data['framework'])

        system_prompt = updated_data['framework']['system_prompt']
        self.assertIn('formatting_rules', system_prompt)
        self.assertEqual(['Rule 1.', 'Rule 2.'], system_prompt['formatting_rules'])

        execution_flow = system_prompt['execution_flow']
        self.assertIn('steps', execution_flow)
        self.assertEqual(2, len(execution_flow['steps']))
        self.assertEqual('Step1', execution_flow['steps'][0]['name'])
        self.assertEqual('Final output description.', execution_flow['final_output'])
        self.assertEqual('A final directive.', system_prompt['directive'])

    def test_refactor_frameworks_skips_unknown_format(self):
        """Tests that the refactoring script safely skips unknown formats.

        This test verifies that the script does not perform a destructive
        write when it encounters a legacy file that doesn't match its
        expected XML structure, preventing data loss.
        """
        # 1. Create a dummy legacy file with an unsupported format
        dummy_frameworks_dir = self.test_dir / 'frameworks'
        core_dir = dummy_frameworks_dir / 'core'
        core_dir.mkdir(parents=True, exist_ok=True)

        dummy_framework_path = core_dir / 'unsupported.yml'
        unsupported_content = "### Special Title\n[section1]: some content"

        dummy_framework_data = {
            'name': 'Unsupported Framework',
            'category': 'core',
            'framework': { 'legacy_content': unsupported_content }
        }
        with open(dummy_framework_path, 'w') as f:
            yaml.dump(dummy_framework_data, f)

        original_text = dummy_framework_path.read_text()

        # 2. Run the refactoring function
        refactor_frameworks.refactor_framework_file(dummy_framework_path)

        # 3. Assert that the file was NOT modified
        new_text = dummy_framework_path.read_text()
        self.assertEqual(original_text, new_text, "Script should not modify files with unknown legacy formats.")


if __name__ == '__main__':
    unittest.main()