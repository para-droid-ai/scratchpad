# Agent Jules work order

# Jules Kit

This repository contains Jules’ Remedial Playbook, shell helpers, and templates to execute daily tasks safely and recover quickly from errors.

## Contents
- `REMEDIAL_PLAYBOOK`: Primary directive and recovery manual.
- `templates/error-log-template`: Standard incident/error log template.
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
---

You have **three** major tasks today. All of which have subtasks. You are to complete them with the extreme precision end efficiently.
If you get stuck you are to to review your "🛠 Jules’ Remedial Playbook"


1. Your task is to thoroughly document this entire repository. Please follow these steps meticulously for your first objective.
2. Your task is to find and fix a major and three minor verifiable bug within this repository. Please follow these steps meticulously as set below.
3. Your task is to meaningfully improve the test coverage of this repository. Please follow these steps meticulously on your third objective.

---

1. **Full Docstring Coverage**: Systematically scan every source file. Add a complete docstring to every single public function, method, and class. Do not skip any, regardless of their apparent simplicity.

**High-Quality Docstrings**: For each docstring, ensure you clearly explain:
- The purpose or main action of the code.
- A description for every parameter/argument.
- A description of the return value.

**Follow Conventions**: Adhere to the standard documentation style for the repository's programming language (e.g., JSDoc, Google Style Python Docstrings, GoDoc).

**Update the README**: Review and update the main README file to be a complete guide for a new developer, covering purpose, setup, and usage. If no README exists, create one from scratch.

You should not ask me questions until the task is completed.

---

2. **Codebase Analysis & Bug Identification**: Systematically analyze the codebase to identify a potential bug. This could be a logical error, an unhandled edge case, or a deviation from documented behavior. Prioritize bugs that are verifiable with a clear failure case.

**Detailed Bug Report**: Before writing any code, provide a brief report explaining:
- The file and line number(s) where the bug is located.
- A clear description of the bug and its impact on the user or system.
- Your proposed strategy for fixing it.

**Targeted Fix Implementation**: Implement the most direct and clean fix for the identified bugs. Avoid making unrelated refactors or style changes in the process.

**Verification Through Testing**: To validate your fix, you must:
- Write a new test case that specifically fails before your fix and passes after it, proving the bug is resolved.
- Run the entire existing test suite to ensure your changes have not introduced any regressions.

---

3. **Coverage Analysis**: Scan the repository to identify source files, functions, or modules with the lowest test coverage. Determine the most critical and currently untested code paths.

   **Meaningful Test Implementation**: Write new, high-quality tests (e.g., unit, integration) to cover the identified gaps. Your tests should be robust and verify important business logic or edge cases, not just trivially increase the coverage percentage.

   **Follow Existing Conventions**: Your new tests must adhere to the style, structure, and testing framework already used in the project. Use existing test helpers and mocks where appropriate to maintain consistency.

   **Validation**: Ensure that all new tests pass as expected. Critically, run the entire existing test suite to confirm that you have not introduced any breaking changes or regressions.

**Summary of Improvements**: In addition to the code, conclude with a summary detailing which files you modified and what new behaviors, functions, or edge cases are now covered by your tests.

---

# Jules’ Remedial Playbook

This document defines your core directives and recovery protocols.
It is split into two halves:

1. Daily Tasks & Execution Directives
2. Remedial Safety Net (use if you get stuck, blocked, or break things)

---

## Part I: Execution Directives

You have three major tasks today, each with explicit subtasks.
Follow them with precision and efficiency.
If you get stuck, consult Part II: Remedial Safety Net before escalating.
You should not ask questions until the tasks are completed.

### Task 1: Full Documentation Coverage

1. Systematic Scan
   - Inspect every source file.
   - Add a complete docstring to every public function, method, and class.

2. High-Quality Docstrings must include:
   - Purpose / main action.
   - Description of each parameter/argument.
   - Description of the return value.

3. Conventions
   - Use the repository’s standard style: JSDoc, Google-style Python docstrings, GoDoc, etc.
   - Remain consistent across the entire codebase.

4. README Update
   - If README exists: review and update so a new developer can onboard easily.
   - If README does not exist: create a new one with purpose, setup, and usage.

### Task 2: Bug Hunt and Fixes

1. Codebase Analysis
   - Systematically scan to identify:
     - 1 major verifiable bug
     - 3 minor verifiable bugs

2. Bug Report (before fixing)
   For each bug, document:
   - File and line number(s)
   - Clear description of the bug and its impact
   - Proposed fix strategy

3. Fix Implementation
   - Apply the cleanest, most direct fix.
   - Avoid unrelated refactors.

4. Verification
   - Write a new test that fails before your fix and passes after.
   - Run the full test suite to confirm no regressions.

### Task 3: Improve Test Coverage

1. Coverage Analysis
   - Identify lowest-coverage files/modules.
   - Target critical and untested logic paths.

2. Meaningful Tests
   - Write robust unit/integration tests.
   - Cover important business logic, not trivial cases.
   - Use existing test helpers/mocks for consistency.

3. Validation
   - Ensure new tests pass.
   - Run the full suite to confirm no regressions.

4. Summary Report
   - Document which files you modified.
   - List new behaviors/edge cases covered.

---

## Part II: Remedial Safety Net

If you mess up or get blocked: Stop. Log. Roll back. Recover.
Use the following commands and guardrails.

### 1. Guardrails
- Do not thrash: one failed retry means stop.
- Always log before fixing.
- Roll back to a known good state if in doubt.
- Escalate only after two failed recovery attempts.

### 2. Logging
```bash
# Capture full error output
<your_command> 2>&1 | tee error.log
```

### 3. Git Recovery
```bash
git reset --hard
git clean -fdx
git reset --hard <baseline-tag>   # rollback to safe tag if needed
```

### 4. Docker Recovery
```bash
docker compose down -v
docker compose up --build -d
docker ps
```

### 5. Python Recovery
```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip cache purge
```

### 6. Node.js Recovery
```bash
rm -rf node_modules
npm install
npm cache clean --force
```

### 7. Environment Reset
```bash
exec $SHELL -l
which python
which node
docker --version
```

### 8. Kill Stuck Processes
```bash
pkill -9 -f "python|node|docker"
```

### 9. Config Fallback
```bash
mv config.yaml config.yaml.bak
<tool> init
```

## Escalation Rule
If you cannot recover after two safe attempts:
- Stop.
- Attach error.log.
- List the last commands you tried.
- Hand off with context.

----

# Error/Incident Log Template

- Date/Time:
- Machine/OS:
- Repository commit/tag:
- Command that failed:
- Full output (or attach `error.log`):
- Expected behavior:
- Actual behavior:
- Impact:
- Recovery steps attempted (in order):
  1.
  2.
- Current status:
- Next action / escalation:


----

```bash
#!/usr/bin/env bash
set -euo pipefail

# Log wrapper: run a command and tee to error.log
logrun() {
  echo "+ $*"
  "$@" 2>&1 | tee error.log
}

echo "Remedial actions menu (edit as needed):"

echo "1) Git clean reset"
git reset --hard || true
git clean -fdx || true

echo "2) Docker rebuild"
docker compose down -v || true
docker compose up --build -d || true
docker ps || true

echo "3) Python env rebuild"
**if** command -v python3 >/dev/null 2>&1; **then**
  rm -rf .venv || true
  python3 -m venv .venv
  # shellcheck disable=SC1091
  source .venv/bin/activate
  pip install -r requirements.txt || true
  pip cache purge || true
**fi**

echo "4) Node env rebuild"
**if** command -v npm >/dev/null 2>&1; **then**
  rm -rf node_modules || true
  npm install || true
  npm cache clean --force || true
**fi**

echo "5) Environment reset"
exec $SHELL -l
```