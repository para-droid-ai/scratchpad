#!/usr/bin/env python3
import sys, yaml, pathlib

def main():
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
