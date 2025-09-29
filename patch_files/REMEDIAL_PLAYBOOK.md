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
   - Systematically scan to identify one or more verifiable bugs (e.g., logical errors, unhandled edge cases).

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

If you get blocked or break the environment, stop. Log your actions, roll back to a known good state, and then attempt a safe recovery.

### 1. Automated Recovery: Your First Step

Before attempting manual fixes, use the automated recovery script. It is designed to solve common environment issues safely.

```bash
# Run the automated remedial script from anywhere in the repository.
./jules-kit/scripts/remedial.sh
```

This script will:
-   Correctly identify the repository's root directory.
-   Check for and help resolve Docker permission issues on Linux.
-   Create a detailed `error.log` file in the repository root for diagnostics.

### 2. Manual Recovery Commands

If the automated script does not resolve your issue, you can use the following manual commands.

#### Logging
Always log your commands to track what you've tried. The `remedial.sh` script does this automatically. For manual commands, you can do the same:

```bash
# Capture the full output of any command you run
<your_command> 2>&1 | tee manual_error.log
```

#### Git Recovery
To reset your codebase to a clean state:
```bash
# Discard all local changes and untracked files
git reset --hard
git clean -fdx
```

#### Docker Recovery
If you are having issues with Docker containers:
```bash
docker compose down -v
docker compose up --build -d
docker ps
```

#### Environment Reset
To reset your shell environment:
```bash
exec $SHELL -l
```

### 3. Escalation Rule
If you cannot recover after two safe attempts (one automated, one manual):
- Stop.
- Attach `error.log` and any manual logs.
- List the last commands you tried.
- Hand off with context.