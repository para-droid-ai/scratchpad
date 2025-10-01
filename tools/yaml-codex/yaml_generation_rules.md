# YAML Agent: YAML Generation Rules (Checklist)

1. Start every file with `---` (YAML 1.2.2).
2. Use 2-space indentation. No tabs.
3. Prefer double-quoted strings; escape internal quotes.
4. Quote anything ambiguous: versions, numbers-with-leading-zeros, `NO`, `ON`, `YES`, strings with `:`, `,`, or `#`.
5. Use block scalars for large prompts/policies. Prefer `|+`.
6. Anchors/aliases only for maps/sequences; depth ≤ 10; no recursion.
7. No language-native tags (e.g., `!!python/object`). Output must be safe to `safe_load`.
8. Prefer block-style lists over flow style.
9. Validate to schema; then lint; then ship.
10. Replace NBSP (U+00A0) with normal spaces.
