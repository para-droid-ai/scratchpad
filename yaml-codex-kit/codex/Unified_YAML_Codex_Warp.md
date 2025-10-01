# The Unified YAML Codex — Warp-Agent Edition

This manual distills and unifies your uploaded YAML guides into a single, strict, security-first reference for **automated generation**. The rules are written for machines: explicit, testable, and unfussy.

---

## 1. Spec & Ground Rules (YAML 1.2.2)
- **Spec lock:** Target YAML **1.2.2** at all times.
- **Doc markers:** Every document starts with `---`; use `...` when another document follows.
- **Indentation:** Spaces only; **2 spaces** per level; zero tabs.
- **Collections:** 
  - Mappings: unordered; keys unique.
  - Sequences: ordered; duplicates ok.
  - Scalars: strings, numbers, booleans, null.
- **Comments:** `#` followed by a space; prefer full-line comments before the thing described.

## 2. Canonical Structures
- **Mappings:** `key: value` (colon + space). Keys SHOULD be simple scalars; avoid complex keys.
- **Sequences:** Block style only for non-empty lists:
  ```yaml
  teams:
    - Boston Red Sox
    - Detroit Tigers
  ```
  Flow style `[a, b]` allowed only for empty lists or schema-mandated compaction.
- **Hierarchy:** Only indentation creates structure. Never imply nesting inside a scalar.

## 3. Scalars & Defensive Quoting
- **Booleans:** `true` / `false`
- **Null:** `null`
- **Numbers:** Quote things that look numeric but are meant as strings (e.g., `"1.0"`, `"09"`).
- **Strings:** Default to **double quotes** unless the string is alnum + underscore and has no specials.
- **Colon, hash, comma inside strings:** Always quote (`"key: val"`, `"hello, world"`, `"hash # not comment"`).

## 4. Multi-line Content (Block Scalars)
- Use **literal** (`|`) to preserve newlines; **folded** (`>`) to wrap to spaces.
- Always add a **chomp modifier**:
  - `|-` strip final newline
  - `|+` keep trailing newlines
  - `>-` folded + strip
  - `>+` folded + keep
- For long prompts, policies, or embedded XML/Markdown, prefer **`|+`** to preserve exact formatting.

## 5. Anchors, Aliases, and Merge Keys
- **Anchors (`&`) & aliases (`*`):** Only for **non-empty maps/sequences**, not scalars.
- **Depth limit:** Max 10 nested expansions; **no recursion**.
- **Merge keys (`<<`):** Only merge **maps**; local keys override merged values.

## 6. Security Protocols (Inert-by-Design)
- **No language-native tags** like `!!python/object`.
- Output must be safe to parse with `safe_load` / equivalents.
- Never inline plaintext secrets for platform configs (e.g., Kubernetes); use refs.
- For K8s, always include `securityContext` and `resources` requests/limits; never run privileged.

## 7. Validation Loop (Schema-Driven)
1. Load target **JSON Schema** (or OpenAPI-derived constraints).
2. Generate YAML strictly to schema.
3. Validate → Repair (fail-fast). Ship only on green.
4. Lint with `.yamllint` (style) and parser (syntax).

## 8. Common Failure Modes (and Fixes)
- **“Norway Problem” (NO, YES, ON):** Quote those strings.
- **Flow-style delimiter collisions:** Prefer block style for lists, always quote commas inside strings.
- **Dangling indentation / mixed tabs:** Normalize to 2-space; convert tabs to spaces.
- **NBSP (U+00A0) contamination:** Replace with regular spaces.

## 9. Warp-Agent Generation Heuristics
- Start every file with `---`.
- Default to double-quoted strings; escape inner quotes.
- For large prompt content, use `|+` literal blocks.
- Normalize whitespace; strip trailing spaces.
- On conflict, **choose stricter rule**.
- Emit **one logical concept per document** unless a multi-doc stream is explicitly required.

---

### Ready-to-paste Patterns

**Multi-environment config with merge keys**
```yaml
---
defaults: &defaults
  retries: 3
  timeout_seconds: 30

dev:
  <<: *defaults
  debug: true

prod:
  <<: *defaults
  timeout_seconds: 60
```

**Kubernetes container with safe defaults**
```yaml
---
apiVersion: "v1"
kind: "Pod"
metadata:
  name: "safe-pod"
spec:
  containers:
    - name: "app"
      image: "example/app:1.0.0"
      securityContext:
        runAsNonRoot: true
        allowPrivilegeEscalation: false
      resources:
        requests:
          cpu: "250m"
          memory: "256Mi"
        limits:
          cpu: "500m"
          memory: "512Mi"
```

**Prompt-as-data with literal block scalar**
```yaml
---
framework:
  content: |+
    <system_prompt>
      Rules:
        1) Be explicit.
        2) Validate to schema before shipping.
    </system_prompt>
```
