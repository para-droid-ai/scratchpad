---
# Changelog
All notable changes to the Scratchpad Framework repository.

## [3.1.0] - 2025-10-01

### Added

#### YAML Codex Integration
- ✅ **YAML Codex Kit consolidated** into main repository structure
  - Created `/tools/yaml-codex/` directory with all YAML validation tools
  - Moved schemas to centralized `/schemas/` directory
  - Added repository-wide `.yamllint.yaml` configuration
  - Integrated `init_scan.py` and `parse_all.py` utilities

#### New Personas
- ✅ **YAML Codex Agent** (`frameworks/personas/yaml-codex-agent.yml`)
  - Expert YAML 1.2.2 compliance agent
  - 7,807 bytes of comprehensive YAML knowledge
  - Validation, generation, and repair capabilities
- ✅ **Gemini 2.5 Public** (`frameworks/personas/gemini.25.yaml`)
  - Public-safe Gemini configuration
  - 4,640 bytes with safety policies enabled

#### Documentation
- ✅ **Repository Manifest** (`docs/repository-manifest.md`)
  - Complete inventory of all 115 files
  - Detailed framework relationships and dependencies
  - Size statistics and maintenance status
- ✅ **YAML Codex Kit Inventory** (`docs/yaml-codex-kit-inventory.md`)
  - Component documentation with SHA256 hashes
  - Integration points and reusable patterns
- ✅ **YAML Audit Report** (`docs/yaml-audit.md`)
  - Comprehensive YAML 1.2.2 compliance analysis
  - 96% of files need remediation
  - Detailed action plan for fixes
- ✅ **Bug Report** (`docs/bug-reports/bug-report-2025-10-01.md`)
  - 8 documented bugs (5 minor, 3 major)
  - Reproduction steps and fix strategies
  - Priority recommendations
- ✅ **Migration Log** (`docs/yaml-codex-migration-log.md`)
  - File movement tracking
  - Integration benefits documented

### Discovered Issues

#### Major Bugs (3)
1. **Widespread Backslash Escape Contamination**
   - 33+ YAML files affected
   - 346+ instances of `\\n`, `\\t`, `\\\"`
   - Violates YAML 1.2.2 specification

2. **Missing Document Start Markers**
   - 49/49 YAML files missing `---`
   - Parser compatibility issues
   - Multi-document stream failures

3. **Unquoted Ambiguous Values**
   - Version numbers parsed as floats
   - `NO`, `YES`, `ON`, `OFF` misinterpreted as booleans
   - Data corruption risk

#### Minor Bugs (5)
1. **Missing Error Handling** in `generate_framework_docs.py`
2. **Hardcoded Paths** in all Python scripts
3. **Missing Null Checks** in `add_framework_metadata.py`
4. **Incorrect Version Type Handling** in `fix_yaml_formatting.py`
5. **Missing Character Count Validation** in tests

### Changed

#### Repository Structure
- Created `/schemas/` directory for JSON schemas
- Created `/tools/yaml-codex/` for YAML utilities
- Added `/docs/bug-reports/` directory
- Organized documentation in `/docs/`

### Security
- Identified and documented prompt injection vulnerabilities
- Added security protocols to YAML Codex Agent
- Enforced no language-native tags policy

### Testing
- Identified test coverage gaps (~60% current coverage)
- Documented missing test categories:
  - No Python docstring validation
  - No YAML schema compliance tests
  - No integration tests
  - No performance tests
  - No cross-platform tests

## Statistics

### Repository Metrics
- **Total Files**: 115 (excluding .git)
- **Total Size**: ~52 MB
- **YAML Files**: 49 frameworks
- **Documentation**: 14 markdown files
- **Scripts**: 7 Python, 6 Shell
- **Test Coverage**: ~60%

### Compliance Status
- **YAML 1.2.2 Compliant**: 1/49 files (2%)
- **Needs Major Fixes**: 47/49 files (96%)
- **Critical Issues**: 33 files (67%)
- **Estimated Remediation**: 4-6 hours with automation

## Next Steps

### Immediate Priority
1. Fix backslash escapes in 33+ YAML files
2. Add document start markers to all YAML files
3. Quote all ambiguous values

### High Priority
1. Implement comprehensive YAML remediation script
2. Add failing tests for all 8 discovered bugs
3. Increase test coverage to 80%

### Medium Priority
1. Add Python docstrings to all scripts
2. Create pre-commit hooks for YAML validation
3. Update CI/CD pipelines

## Contributors
- **YAML Codex Agent** - Primary auditor and documentation
- **Warp AI Agent** - Integration and consolidation

## References
- YAML 1.2.2 Specification
- Unified YAML Codex Warp (`/tools/yaml-codex/`)
- Comet Browser AI Framework Guidelines

---

*This changelog follows [Keep a Changelog](https://keepachangelog.com/) format.*