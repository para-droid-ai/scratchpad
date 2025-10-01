#!/usr/bin/env python3
import os
import sys
import hashlib
import json

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
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
