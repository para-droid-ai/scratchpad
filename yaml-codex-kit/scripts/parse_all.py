#!/usr/bin/env python3
"""
YAML File Validation Tool

Validates YAML files for syntax correctness using PyYAML's safe_load_all.
Supports both single-document and multi-document YAML streams.

This tool is useful for CI/CD pipelines to ensure all YAML files in a
repository are syntactically valid before deployment.

Author: YAML Codex Agent
Date: 2025-10-01
"""

import sys
import yaml
import pathlib


def main():
    """Parse and validate YAML files provided as command-line arguments.
    
    Validates each YAML file by attempting to parse it with yaml.safe_load_all().
    Supports multi-document YAML streams. Reports success or failure for each
    file and exits with appropriate status code.
    
    Exit Codes:
        0: All files parsed successfully
        1: One or more files failed to parse or no files provided
        
    Usage:
        python parse_all.py file1.yml file2.yaml file3.yml
        
    Output:
        [OK] path/to/file.yml    - File parsed successfully
        [FAIL] path/to/file.yml: error message  - File failed to parse
        
    Raises:
        SystemExit: Always exits with status code 0 or 1
    """
    files = [p for p in map(pathlib.Path, sys.argv[1:]) if p.suffix in ('.yml', '.yaml')]
    if not files:
        print("No YAML files provided to parse.", file=sys.stderr)
        sys.exit(1)
    failures = 0
    for p in files:
        try:
            with p.open('r', encoding='utf-8') as fh:
                content = fh.read()
            # Allow multi-doc streams
            for _doc in yaml.safe_load_all(content):
                pass
            print(f"[OK] {p}")
        except Exception as e:
            failures += 1
            print(f"[FAIL] {p}: {e}", file=sys.stderr)
    sys.exit(1 if failures else 0)

if __name__ == "__main__":
    main()
