# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Overview

The Scratchpad Framework is a curated collection of AI reasoning templates in YAML format, designed for Comet Browser and other AI assistants. The repository contains 30+ frameworks organized into three categories: **core** (general-purpose reasoning), **personas** (AI personalities), and **purpose-built** (task-specific frameworks).

## Quick Commands

### Validation & Testing
```bash
# Run YAML validation tests
python3 tests/test_yaml_frameworks.py

# Run all test suites
bash tests/run_all_tests.sh

# Run with verbose output
bash tests/run_all_tests.sh --verbose

# Validate YAML formatting (via yamllint if installed)
yamllint -c .yamllint.yaml frameworks/
```

### Framework Maintenance
```bash
# Fix YAML formatting (converts to literal block scalars)
python3 scripts/fix_yaml_formatting.py

# Add framework metadata
python3 scripts/add_framework_metadata.py

# Generate framework documentation
python3 scripts/generate_framework_docs.py

# Fix YAML 1.2.2 compliance
python3 scripts/fix_all_yaml_compliance.py
```

### Development
```bash
# Run remedial script for environment checks
bash scripts/remedial.sh

# View test coverage
python3 tests/test_yaml_frameworks.py  # Shows 6 test categories
```

## Repository Architecture

### Directory Structure
```
frameworks/
├── core/              # 10 general-purpose reasoning templates (scratchpad-*.yml)
├── personas/          # 8 AI personality frameworks (e.g., gilfoyle-bot.yml, debug-detective.yml)
└── purpose-built/     # 18 specialized task frameworks (e.g., deep-researcher.yml, podsynth-*.yml)

tests/                 # Validation test suite
├── test_yaml_frameworks.py       # Main YAML validation (15 tests passing)
├── test_bug_fixes.py             # Bug fix verification
├── run_all_tests.sh              # Master test runner
└── test_*.sh                     # Individual test suites

scripts/               # Utility scripts for maintenance
├── fix_yaml_formatting.py        # YAML literal block scalar converter
├── fix_all_yaml_compliance.py   # YAML 1.2.2 compliance fixer
├── add_framework_metadata.py    # Metadata injection
├── generate_framework_docs.py   # Auto-generate FRAMEWORK_REFERENCE.md
└── remedial.sh                   # Environment diagnostics

schemas/
└── prompt_framework.schema.json  # JSON Schema for framework validation

docs/                  # Documentation (guides, references, reports)
.github/workflows/     # CI/CD workflows
assets/showcase/       # Screenshots and visual demos
```

### Framework File Structure

All framework YAML files follow this schema (defined in `schemas/prompt_framework.schema.json`):

**Required fields:**
- `name` (string): Human-readable framework name
- `version` (string): Version number (quoted, e.g., "2.7" or "1.0")
- `framework.content` (string): The actual framework/prompt content

**Recommended fields:**
- `category` (string): One of "core", "personas", or "purpose-built"
- `documentation.purpose` (string): Brief description of framework purpose
- `documentation.use_case` (string): When to use this framework
- `documentation.character_count` (integer): Approximate character count

**Example:**
```yaml
---
name: Scratchpad 2.7
version: '2.7'
category: core
documentation:
  purpose: Latest comprehensive scratchpad framework with optimized cognitive workflow
  use_case: High-complexity tasks requiring systematic reasoning, quality validation, and exploration
  character_count: 2148
framework:
  content: |
    <system_prompt>
        <!-- Framework content here -->
    </system_prompt>
```

## YAML Formatting Rules

All framework YAML files **must** comply with these rules (enforced by `.yamllint.yaml` and test suite):

### Document Structure
- **MUST** start with `---` document marker
- **MUST** use 2-space indentation
- **MUST** use Unix line endings (`\n`)
- **MUST** end with single trailing newline
- Max line length: 120 characters (allows non-breakable words)

### Field Conventions
- **Version field**: Always quote version numbers as strings (`version: '2.7'`, not `version: 2.7`)
- **Multi-line content**: Use literal block scalars (`content: |`) for framework content
- **No tabs**: Only spaces for indentation
- **Comments**: Require starting space (`# comment`, not `#comment`)

### Content Formatting
```yaml
# CORRECT: Literal block scalar with proper indentation
framework:
  content: |
    Line 1 of content
    Line 2 of content
    Nested structure maintained

# INCORRECT: Escaped string format
framework:
  content: "Line 1 of content\nLine 2 of content\n"
```

### Schema Validation
Run validation before committing:
```bash
python3 tests/test_yaml_frameworks.py
```

This validates:
- YAML syntax correctness
- Required fields presence
- Field type correctness
- Metadata quality (purpose/use_case length, version presence)
- Content uniqueness across frameworks
- Category organization

## Development Workflows

### Adding a New Framework

1. **Choose category**: Determine if framework is `core`, `personas`, or `purpose-built`
2. **Create file**: Place in appropriate `frameworks/` subdirectory
   - Naming: Use lowercase with hyphens (e.g., `my-new-framework.yml`)
3. **Use template structure**:
   ```yaml
   ---
   name: My New Framework
   version: '1.0'
   category: core
   documentation:
     purpose: Brief description (< 30 words)
     use_case: When to use this (< 40 words)
     character_count: 0  # Update after content complete
   framework:
     content: |
       <!-- Your framework content here -->
   ```
4. **Validate locally**:
   ```bash
   python3 tests/test_yaml_frameworks.py
   yamllint -c .yamllint.yaml frameworks/your-category/your-framework.yml
   ```
5. **Auto-fix formatting if needed**:
   ```bash
   python3 scripts/fix_yaml_formatting.py
   python3 scripts/add_framework_metadata.py
   ```
6. **Update documentation**:
   ```bash
   python3 scripts/generate_framework_docs.py  # Regenerates FRAMEWORK_REFERENCE.md
   ```
7. **Test and commit**: Run full test suite before committing

### Modifying an Existing Framework

1. **Version bumping**:
   - Breaking changes: Increment major version (`2.7` → `3.0`)
   - New features: Increment minor version (`2.6` → `2.7`)
   - Bug fixes: Increment patch version (add `.1`, `.2`, etc.)

2. **Update related files**:
   - If changing `name` or `purpose`, run `scripts/generate_framework_docs.py`
   - If changing structure, verify schema compliance

3. **Validation workflow**:
   ```bash
   # Fix formatting
   python3 scripts/fix_yaml_formatting.py
   
   # Validate changes
   python3 tests/test_yaml_frameworks.py
   
   # Regenerate docs
   python3 scripts/generate_framework_docs.py
   ```

### Framework Naming Conventions

- **Core frameworks**: `scratchpad-<version/variant>.yml` (e.g., `scratchpad-2.7.yml`, `scratchpad-lite.yml`)
- **Personas**: `<name>-bot.yml` or descriptive name (e.g., `gilfoyle-bot.yml`, `debug-detective.yml`)
- **Purpose-built**: Descriptive names with hyphens (e.g., `deep-researcher.yml`, `podsynth-clean.yml`)

## Testing Strategy

### Test Suite Components

1. **test_yaml_frameworks.py** (Primary validation)
   - YAML syntax validation (all frameworks)
   - Required keys check (`name`, `version`, `framework.content`)
   - Field type validation (strings, objects, etc.)
   - Metadata quality checks (purpose/use_case length limits)
   - Content uniqueness detection
   - Category organization verification

2. **run_all_tests.sh** (Master test runner)
   - Runs all individual test suites
   - Supports `--verbose` and `--stop-on-failure` flags
   - Validates environment before running tests
   - Provides comprehensive final summary

3. **Individual test scripts**
   - `test_markdown_links.sh`: Validates documentation links
   - `test_framework_templates.sh`: Template validation
   - `test_bug_fixes.sh`: Regression testing

### Test Execution
```bash
# Quick validation
python3 tests/test_yaml_frameworks.py

# Full test suite
bash tests/run_all_tests.sh

# Verbose mode (see all output)
bash tests/run_all_tests.sh --verbose

# Stop on first failure
bash tests/run_all_tests.sh --stop-on-failure
```

## CI/CD Integration

The repository uses GitHub Actions for continuous integration (`.github/workflows/ci.yml`):

### CI Workflow
- **Triggers**: Push to `main`, pull requests to `main`
- **Python version**: 3.11
- **Dependencies**: `pytest`, `pyyaml`
- **Tests executed**:
  - `python tests/test_yaml_frameworks.py`
  - `python tests/test_bug_fixes.py`

### Local CI Parity
Run the same checks locally before pushing:
```bash
# Install dependencies
pip install pytest pyyaml

# Run CI test suite
python3 tests/test_yaml_frameworks.py
python3 tests/test_bug_fixes.py
```

## Common Issues & Solutions

### Issue: YAML validation fails with "not a valid YAML dictionary"
**Solution**: Ensure file starts with `---` and uses proper YAML structure
```bash
python3 scripts/fix_all_yaml_compliance.py
```

### Issue: Content field using escaped strings instead of literal blocks
**Solution**: Run the formatting script
```bash
python3 scripts/fix_yaml_formatting.py
```

### Issue: Version field parsed as number instead of string
**Solution**: Quote version numbers in YAML
```yaml
# CORRECT
version: '2.7'

# INCORRECT (parsed as float 2.7)
version: 2.7
```

### Issue: Purpose or use_case too verbose
**Warning threshold**: Purpose > 30 words, use_case > 40 words  
**Solution**: Edit for conciseness. These fields should be scannable summaries.

### Issue: Character count mismatch
**Solution**: Recalculate character count
```bash
python3 scripts/add_framework_metadata.py  # Auto-updates character counts
```

## Framework Content Guidelines

### Core Frameworks
- Focus on general-purpose reasoning structures
- Should be adaptable to various tasks
- Examples: scratchpad-lite (lightweight), scratchpad-2.7 (comprehensive)

### Personas
- Define consistent AI personality and tone
- Include interaction rules and example dialogues
- Should specify how to handle different user scenarios
- Examples: gilfoyle-bot (sarcastic technical expert), debug-detective (systematic problem-solver)

### Purpose-Built Frameworks
- Optimize for specific task domains
- Include domain-specific structure and terminology
- Examples: deep-researcher (research/investigation), podsynth-* (podcast generation)

### Content Structure Patterns
Most frameworks use one of these structures:
1. **XML-tagged system prompts** (e.g., `<system_prompt>`, `<formatting_rules>`)
2. **Markdown sections** with clear headings
3. **Hybrid approaches** combining both

Choose the structure that best fits your framework's purpose and target platform.

## Version History

- **v3.0 (October 2025)**: Major refactoring, YAML conversion, 100% validation passing
- **v2.x**: Various scratchpad iterations with enhanced reasoning capabilities
- **v1.x**: Initial framework collection

## Useful Scripts Reference

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `fix_yaml_formatting.py` | Convert to literal block scalars | After editing framework content |
| `fix_all_yaml_compliance.py` | Ensure YAML 1.2.2 compliance | Before committing changes |
| `add_framework_metadata.py` | Auto-calculate character counts | After content changes |
| `generate_framework_docs.py` | Regenerate FRAMEWORK_REFERENCE.md | After adding/modifying frameworks |
| `remedial.sh` | Environment diagnostics | Troubleshooting setup issues |

## Additional Resources

- `README.md`: Repository overview and quick start
- `CONTRIBUTING.md`: Contribution guidelines and style guides
- `docs/GUIDE.md`: User guide for understanding frameworks
- `docs/FRAMEWORK_REFERENCE.md`: Auto-generated framework catalog
- `docs/repository-manifest.md`: Complete file inventory and relationships
- `docs/FAQ.md`: Frequently asked questions
