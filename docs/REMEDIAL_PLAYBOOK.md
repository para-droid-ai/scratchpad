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
