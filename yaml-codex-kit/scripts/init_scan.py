#!/usr/bin/env python3
"""
Repository File Scanner and Inventory Tool

Scans a directory tree and generates a JSON inventory of all files with
their sizes and SHA256 checksums. Useful for tracking file changes and
generating repository manifests.

Author: YAML Codex Agent
Date: 2025-10-01
"""

import os
import sys
import hashlib
import json


def sha256(path):
    """Calculate SHA256 hash of a file.
    
    Reads the file in chunks to handle large files efficiently without
    loading the entire file into memory.
    
    Args:
        path: Path to the file to hash
        
    Returns:
        str: Hexadecimal SHA256 hash of the file contents
        
    Raises:
        IOError: If file cannot be read
    """
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    """Generate a comprehensive file inventory of a directory tree.
    
    Walks through the directory tree starting from the specified root
    (or current directory if not specified) and creates a JSON report
    containing file paths, sizes, and SHA256 checksums.
    
    Excludes common non-source directories:
    - .git (version control)
    - .venv (Python virtual environments)
    - node_modules (Node.js dependencies)
    - __pycache__ (Python bytecode cache)
    
    The report is printed to stdout in JSON format with the structure:
    {
        "root": "/path/to/scanned/directory",
        "files": [
            {"path": "relative/path/to/file", "size": 1234, "sha256": "abc..."},
            ...
        ]
    }
    
    Usage:
        python init_scan.py [directory_path]
        
    If no directory path is provided, scans the current directory.
    """
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    root = os.path.abspath(root)
    report = {"root": root, "files": []}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {'.git', '.venv', 'node_modules', '__pycache__'}]
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            try:
                st = os.stat(p)
                item = {
                    "path": os.path.relpath(p, root),
                    "size": st.st_size,
                    "sha256": sha256(p),
                }
                report["files"].append(item)
            except Exception as e:
                report["files"].append({"path": os.path.relpath(p, root), "error": str(e)})
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
