# Scratchpad Framework FAQ & Troubleshooting

Common questions, issues, and solutions for using Scratchpad frameworks effectively.

---

## General Questions

### What is a Scratchpad Framework?

A Scratchpad Framework is a structured system prompt that guides AI models through explicit reasoning steps before generating responses. Unlike simple prompts, frameworks define cognitive operations, reasoning pathways, and quality checks that enhance output quality and transparency.

### Why use YAML format?

YAML provides:
- **Human-readable** structure that's easy to edit
- **Machine-parseable** for automation and tooling
- **Consistent** format across all frameworks
- **Metadata** support for categorization and documentation
- **Optimized** for character-limited environments like Comet Browser

### Which framework should I use?

| Use Case | Recommended Framework | Why |
|----------|----------------------|-----|
| Quick tasks, limited characters | `scratchpad-lite.yml` | Minimal overhead, fast |
| Complex reasoning tasks | `scratchpad-2.7.yml` | Full cognitive operations |
| Research and analysis | `deep-researcher.yml` | Systematic investigation |
| Creative writing | `emotional-intelligence.yml` | Nuanced expression |
| Technical debugging | `debug-detective.yml` (persona) | Root cause focus |
| Casual interaction | `gilfoyle-bot.yml` (persona) | Personality-driven |

---

## Usage Questions

### How do I use a framework with an AI assistant?

**Method 1: Direct Copy-Paste**
1. Open desired `.yml` file
2. Copy the entire `content` section under `framework:`
3. Paste into AI chat before your query
4. Ask your question

**Method 2: System Prompt (if supported)**
1. Copy framework content
2. Set as system/custom instruction in AI settings
3. All subsequent queries will use framework

**Method 3: API Integration**
```python
import yaml

with open('frameworks/core/scratchpad-2.7.yml') as f:
    framework = yaml.safe_load(f)
    system_prompt = framework['framework']['content']

# Use system_prompt in API call
```

### Can I modify frameworks?

**Yes!** Frameworks are templates. Common modifications:
- Adjust verbosity levels
- Add domain-specific reasoning steps
- Customize output format instructions
- Merge multiple frameworks for hybrid approaches

### Do frameworks work with all AI models?

**Mostly**, but effectiveness varies:
- ✅ **Excellent**: Claude (Opus/Sonnet), GPT-4, Gemini Pro
- ⚠️ **Good**: GPT-3.5-turbo, Llama 70B+, Command R+
- ❌ **Limited**: Smaller models (<10B parameters) may not follow complex instructions

---

## Troubleshooting

### Problem: Framework output is too verbose

**Solutions:**
1. Use `scratchpad-concise.yml` or `scratchpad-lite.yml`
2. Add explicit instruction: "Keep response under 500 words"
3. For Comet Browser, specify character limit in query
4. Edit framework to remove `Exploration` or `Metacognition` sections

**Example:**
```
[Using scratchpad-lite.yml]
Brief explanation only, max 200 words: How does photosynthesis work?
```

### Problem: AI ignores framework structure

**Possible Causes & Fixes:**

| Cause | Solution |
|-------|----------|
| Framework too complex for model | Switch to simpler framework (lite/concise) |
| Framework not in system prompt | Ensure pasted *before* query in conversation |
| Query conflicts with framework | Rephrase query to align with framework expectations |
| Model doesn't support structured prompts | Try different AI model (Claude/GPT-4 recommended) |

### Problem: Scratchpad section visible in output

**Expected Behavior**: The scratchpad (reasoning steps) should ideally be hidden or clearly separated from final output.

**Fixes:**
1. Add instruction: "Hide scratchpad, show only final answer"
2. Use frameworks with explicit `[Hidden from user]` markers
3. For Comet: Add "Output only the final response section"

**Note**: Some models show reasoning by default. This is actually beneficial for transparency and learning.

### Problem: Framework doesn't improve output quality

**Diagnostics:**
1. **Is model capable enough?** Try with GPT-4 or Claude first
2. **Is query complex enough?** Simple queries ("What is 2+2?") don't benefit much
3. **Is framework appropriate?** Match framework to task type
4. **Is prompt clear?** Ambiguous queries get ambiguous results even with frameworks

**Test with known-good example:**
```
[Using scratchpad-2.7.yml]
Explain the ethical implications of AI-generated art, considering perspectives of artists, consumers, and AI developers.
```

If this doesn't produce structured, multi-perspective analysis, the issue is with model or implementation, not the framework.

### Problem: Character count too high for Comet Browser

**Comet Browser Limit**: ~4000 characters for optimal performance

**Optimization Strategies:**
1. **Use compact frameworks**:
   - `scratchpad-lite.yml` (~800 chars)
   - `scratchpad-concise.yml` (~600 chars)
   
2. **Abbreviate framework sections**:
   ```yaml
   # Instead of full names
   [AttentionFocus] → [Focus]
   [CognitiveOperations] → [CogOps]
   [ReasoningPathway] → [Path]
   ```

3. **Remove optional sections**:
   - Exploration (follow-up questions)
   - Metacognition (self-assessment)
   - Keep only: Focus, Query, KeyInfo, Pathway

4. **Use framework once, reference for follow-ups**:
   ```
   First message: [Full framework] + query
   Follow-ups: "Continue with same reasoning approach"
   ```

---

## Advanced Usage

### Can I combine multiple frameworks?

**Yes!** Common patterns:

**Pattern 1: Reasoning + Persona**
```
[Scratchpad-2.7 framework for reasoning]
+
[Deep Thinker persona for communication style]
```

**Pattern 2: Domain-Specific Hybrid**
```
[Scratchpad-lite for structure]
+
[Custom domain rules]
Example: "Additionally, all code must follow PEP-8 style"
```

### How do I create a custom framework?

See [docs/GUIDE.md](GUIDE.md) for beginner guide. Advanced tips:

1. **Start with existing framework** as template
2. **Define clear sections** with distinct purposes
3. **Test with various query types** (simple, complex, ambiguous)
4. **Optimize character count** vs. capability trade-off
5. **Document** purpose and use cases in YAML metadata

### Framework versioning strategy?

**Semantic versioning adapted for prompts:**
- **Major** (2.0 → 3.0): Fundamental reasoning structure changes
- **Minor** (2.6 → 2.7): New sections or significant improvements
- **Suffix** (-lite, -pplx, -alt): Variations for specific contexts

---

## Performance & Optimization

### Why is response slower with frameworks?

**Reasoning requires more computation**:
- More tokens to process (framework text)
- Explicit reasoning steps take time
- Quality vs. speed trade-off

**Optimization strategies:**
- Use lite frameworks for quick tasks
- Keep framework in system prompt (not repeated per query)
- For time-sensitive queries, add "Prioritize speed, brevity OK"

### Do frameworks cost more API credits?

**Yes**, due to increased token count:
- Framework adds 200-2000 tokens depending on version
- Reasoning output adds 20-50% more tokens
- **Trade-off**: Higher cost but better output quality
- **Mitigation**: Use appropriate framework size for task

---

## Environment-Specific Issues

### Comet Browser
- **Character Limit**: Use lite/concise frameworks
- **No System Prompt**: Include framework in every query
- **Hidden Reasoning**: Works well, scratchpad typically hidden

### ChatGPT Web Interface
- **Custom Instructions**: Place framework there permanently
- **Long Context**: Full frameworks work excellently
- **Memory**: Maintains framework across conversations

### API Usage (OpenAI, Anthropic)
- **System Prompt**: Best practice for frameworks
- **Token Limits**: Monitor with long frameworks
- **Caching**: Some services cache system prompts (reduces cost)

---

## Contributing

### Found a bug or issue not listed here?

1. Check [error-log-template.md](error-log-template.md)
2. Open issue on GitHub with:
   - Framework version
   - AI model used
   - Expected vs. actual behavior
   - Minimal reproduction example

### Have a solution or tip?

Pull requests welcome! Update this FAQ or create new documentation.

---

## Additional Resources

- **Beginner Guide**: [docs/GUIDE.md](GUIDE.md)
- **Persona Ops**: [docs/persona-operations-guide.md](persona-operations-guide.md)
- **White Paper**: [docs/white paper.md](white%20paper.md)
- **Testing Guide**: [tests/test_yaml_frameworks.py](../tests/test_yaml_frameworks.py)

---

**Last Updated**: 2025-10-01  
**Maintainers**: Repository contributors  
**Feedback**: Open an issue or discussion on GitHub
