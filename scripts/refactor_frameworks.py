import os
import re
import yaml

def refactor_framework_file(filepath):
    """
    Refactors a single framework YAML file from the legacy XML-like
    string format to a structured YAML format.

    Args:
        filepath (str): The path to the framework YAML file.
    """
    with open(filepath, 'r') as f:
        data = yaml.safe_load(f)

    if 'framework' not in data or 'legacy_content' not in data['framework']:
        # This case handles files that are already refactored or don't have legacy content.
        return

    legacy_content = data['framework']['legacy_content']

    # Bug Fix: Add a check for the expected structure before proceeding.
    # If the key tag is missing, skip the file to prevent data loss.
    if '<system_prompt>' not in legacy_content:
        print(f"Skipping {filepath}, unknown legacy format (missing <system_prompt> tag).")
        return

    # Extract formatting rules
    rules_match = re.search(r'<formatting_rules>(.*?)</formatting_rules>', legacy_content, re.DOTALL)
    rules = []
    if rules_match:
        rules_str = rules_match.group(1)
        rule_matches = re.findall(r'<rule>(.*?)</rule>', rules_str, re.DOTALL)
        rules = [r.strip() for r in rule_matches]

    # Extract execution flow steps
    steps_match = re.search(r'<scratchpad_logic>(.*?)</scratchpad_logic>', legacy_content, re.DOTALL)
    steps = []
    if steps_match:
        steps_str = steps_match.group(1)
        step_matches = re.findall(r'<step name="(.*?)">(.*?)</step>', steps_str)
        steps = [{'name': name.strip(), 'description': desc.strip()} for name, desc in step_matches]

    # Extract final output and directive
    final_output_match = re.search(r'<final_output>(.*?)</final_output>', legacy_content, re.DOTALL)
    final_output = final_output_match.group(1).strip() if final_output_match else ""

    directive_match = re.search(r'<directive>(.*?)</directive>', legacy_content, re.DOTALL)
    directive = directive_match.group(1).strip() if directive_match else ""

    # Create the new structured framework
    new_framework = {
        'system_prompt': {
            'formatting_rules': rules,
            'execution_flow': {
                'steps': steps,
                'final_output': final_output
            },
            'directive': directive
        }
    }

    # Replace the old framework structure
    data['framework'] = new_framework

    # Write the updated data back to the file
    with open(filepath, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, indent=2)

    print(f"Refactored {filepath}")

def main():
    """
    Main function to find and refactor all framework YAML files.
    """
    frameworks_dir = 'frameworks'
    for root, _, files in os.walk(frameworks_dir):
        for file in files:
            if file.endswith('.yml') or file.endswith('.yaml'):
                filepath = os.path.join(root, file)
                refactor_framework_file(filepath)

if __name__ == '__main__':
    main()