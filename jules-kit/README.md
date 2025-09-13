# Jules Kit

This repository contains Jules’ Remedial Playbook, shell helpers, and templates to execute daily tasks safely and recover quickly from errors.

## Contents
- `REMEDIAL_PLAYBOOK.md`: Primary directive and recovery manual.
- `templates/error-log-template.md`: Standard incident/error log template.
- `scripts/remedial.sh`: Copy-paste friendly rescue commands.

## Usage
1. Read `REMEDIAL_PLAYBOOK.md` before starting work.
2. For documentation tasks, follow Part I Task 1 exactly.
3. For bug fixing and tests, follow Part I Task 2 and Task 3.
4. If blocked or broken, use `scripts/remedial.sh` and the guidance in Part II.

## Conventions
- Do not ask questions until tasks are completed.
- Always capture output: `cmd 2>&1 | tee error.log`.
- Escalate only after two failed recovery attempts with logs attached.

## Verification
- Run the full test suite after any change.
- Ensure new tests fail before the fix and pass after the fix.
