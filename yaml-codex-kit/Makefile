SHELL := /bin/bash

.PHONY: setup lint parse

setup:
	python3 -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install yamllint pyyaml

lint:
	yamllint -c templates/.yamllint.yaml $(FILES)

# Parse all YAML to ensure syntax; exits non-zero if any fail
parse:
	python3 scripts/parse_all.py $(FILES)
