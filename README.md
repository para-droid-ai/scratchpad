# The Scratchpad Framework
<img width="1536" height="1024" alt="483854870-514bd1e1-6ef5-4403-8d0a-441881c5217e" src="https://github.com/user-attachments/assets/d1032a2e-d001-4be8-b57f-803e82218dea" />

![Tests](https://img.shields.io/badge/tests-15/15_passing-brightgreen)
![Bugs](https://img.shields.io/badge/bugs-0_known-brightgreen)
![YAML](https://img.shields.io/badge/YAML-1.2.2_compliant-blue)
![License](https://img.shields.io/badge/license-MIT-blue)

**Advanced AI Reasoning Templates for Comet Browser**

---

## Overview

The Scratchpad Framework is a curated collection of **AI reasoning templates** designed to transform how AI assistants think and respond. All frameworks are in clean YAML format, optimized for Comet Browser's character limits.

## Repository Structure

```
scratchpad/
├── frameworks/
│   ├── core/              # 10 general-purpose reasoning templates
│   ├── purpose-built/     # 18 task-specific frameworks
│   └── personas/          # 2 AI assistant personalities
├── docs/                  # Documentation and guides
├── scripts/               # Utility scripts
├── assets/showcase/       # Screenshots and demos
├── tests/                 # Validation test suite
├── README.md             # This file
└── license.txt           # MIT License
```

## Quick Start

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Fayeblade1488/scratchpad_fayeblade.git
cd scratchpad_fayeblade
```

2. **Install dependencies** (for development and testing)
```bash
pip install -r requirements.txt
```

### Using a Framework

1. Browse the `frameworks/` directory to find a suitable template
2. Copy the YAML content from your chosen framework
3. Paste it as a system prompt in Comet Browser or your AI assistant
4. Start chatting and enjoy structured, transparent AI reasoning!

### Example Usage

**Using Scratchpad Lite for quick tasks:**
```yaml
# Copy content from frameworks/core/scratchpad-lite.yml
# Paste into Comet Browser's system prompt field
# Ask your question - the AI will now use structured reasoning
```

**For research tasks:**
```yaml
# Use frameworks/purpose-built/deep-researcher.yml
# Perfect for academic research and literature reviews
```

## Framework Categories

### Core Frameworks (10)
- `scratchpad-lite.yml` - Lightweight, 3-step reasoning
- `scratchpad-2.6.yml` - Comprehensive 11-step analysis
- `scratchpad-2.5-refined.yml` - Deep, multi-faceted reasoning
- `scratchpad-concise.yml` - Short, to-the-point answers
- `scratchpad-think.yml` - Metacognitive verbalization
- Plus 5 more variants...

### Purpose-Built Frameworks (18)
- `deep-researcher.yml` - Research and investigation
- `game-design-gabg.yml` - Game design planning
- `emotional-intelligence.yml` - Emotion-aware responses
- `podsynth-clean.yml` - Podcast script generation
- Plus 14 more specialized frameworks...

### Persona Frameworks (2)
- `gilfoyle-bot.yml` - Systems architecture expertise (cynical tone)
- `anton-bot.yml` - Browser automation specialist

## Technical Details

### File Format
- **Format:** YAML 1.2.2 compliant
- **Encoding:** UTF-8
- **Structure:** Nested dictionaries with documented keys
- **Content Style:** Literal block scalars (`|`) for long content

### Framework Structure
Each framework YAML file contains:
```yaml
name: "Framework Name"
version: "1.0"
category: "core|purpose-built|personas"
documentation:
  purpose: "Brief description of framework purpose"
  use_case: "Specific use cases and scenarios"
  character_count: 1234
framework:
  content: |
    The actual framework prompt content
    Uses literal block scalar for readability
```

### Requirements
- **Python:** 3.8+ (for development/testing)
- **Dependencies:** PyYAML, pytest, coverage (see requirements.txt)
- **No runtime dependencies** for using frameworks

### Validation
- **YAML Syntax:** 100% passing
- **Test Suite:** 40 tests, all passing
- **Code Coverage:** 59% for utility scripts
- **YAML Compliance:** Full YAML 1.2.2 compliance

## Testing

### Run All Tests
```bash
# Run complete test suite
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run with coverage report
python -m coverage run -m pytest tests/
python -m coverage report
```

### Run Individual Test Suites
```bash
# YAML validation tests
python -m pytest tests/test_yaml_frameworks.py

# Script functionality tests
python -m pytest tests/test_scripts.py

# Bug fix validation tests
python -m pytest tests/test_bug_fixes.py

# Edge case tests
python -m pytest tests/test_edge_cases.py
```

### Test Coverage
Current test coverage: **59%** for scripts, **40 tests passing**

Coverage includes:
- YAML syntax validation
- Framework structure verification
- Script functionality testing
- Edge case handling
- Error recovery paths

## Development

### Repository Scripts

The `scripts/` directory contains utility tools for framework maintenance:

- `fix_yaml_formatting.py` - Ensures proper YAML formatting with literal block scalars
- `add_framework_metadata.py` - Adds or updates framework metadata
- `generate_framework_docs.py` - Auto-generates markdown documentation
- `refactor_frameworks.py` - Converts legacy XML format to modern YAML
- `convert_frameworks_to_proper_yaml.py` - Converts XML-embedded content to structured YAML
- `add_yaml_doc_markers.py` - Adds YAML 1.2.2 document markers
- `fix_all_yaml_compliance.py` - Comprehensive YAML compliance remediation

### Running Scripts

```bash
# Fix YAML formatting
python scripts/fix_yaml_formatting.py

# Add missing metadata
python scripts/add_framework_metadata.py

# Generate documentation
python scripts/generate_framework_docs.py
```

### Environment Variables

Scripts support the `SCRATCHPAD_DIR` environment variable:
```bash
export SCRATCHPAD_DIR=/path/to/repository
python scripts/fix_yaml_formatting.py
```

## License
MIT License - Free for commercial and personal use.

See [license.txt](license.txt) for full license text.

## Contributing

We welcome contributions! Here's how you can help:

### Reporting Issues
- Use GitHub Issues for bug reports
- Include framework name and error details
- Provide example YAML content if relevant

### Adding New Frameworks
1. Create YAML file in appropriate category directory
2. Follow the standard framework structure
3. Include complete documentation metadata
4. Test with `pytest tests/`
5. Submit a Pull Request

### Code Contributions
1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure all tests pass
5. Submit a Pull Request

### Documentation
- Improvements to README or docs always welcome
- Keep explanations clear and beginner-friendly
- Include examples where helpful

## Project Overview
- **30 frameworks** persona and framework rework
- **70% file reduction** (240 → 73 files)
- **19% size reduction** (149MB → 121MB)
- **100% YAML validation** passing

---

## Credits and Mentions 
- Orignal repo and author: https://github.com/para-droid-ai/scratchpad
- Discord with information: https://discord.gg/mmbQG63U
- OP of scratch-Pad: https://github.com/para-droid-ai
- Fayeblade Repo Author: https://github.com/Fayeblade1488

**Version 3.0 (October 2025)** - Major refactoring and YAML conversion complete.
