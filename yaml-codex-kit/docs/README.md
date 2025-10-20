# YAML Codex Kit (Warp-Agent)

This kit gives your Warp agent a **single source of truth** for generating, linting, and validating **strict YAML (1.2.2)** and includes a **public-safe persona**.

## Contents
- `codex/Unified_YAML_Codex_Warp.md` — The rules your agent should follow.
- `templates/.yamllint.yaml` — Style enforcement.
- `templates/prompt_framework.schema.json` — Example JSON Schema.
- `templates/scratchpad-2.7.yml` — Example compliant YAML.
- `scripts/parse_all.py` — Parse check for YAML (multi-doc safe).
- `scripts/init_scan.py` — Exhaustive repo scanner for Task #1.
- `warp-agent/yaml_generation_rules.md` — Short checklist for the agent.
- `personas/gemini25_public.yaml` — Sanitized, **non‑jailbreak**, public-ready persona.

## Quickstart
```bash
make setup
make lint FILES="templates/scratchpad-2.7.yml"
make parse FILES="templates/scratchpad-2.7.yml"
```

## Repo Init Scan (Task #1)
```bash
python3 scripts/init_scan.py /path/to/repo > init_report.json
```

## Notes
- Prefer block scalars (`|+`) for large prompts.
- Always start documents with `---`.
- Normalize whitespace and replace NBSP with spaces.
- Validate to schema before shipping.
