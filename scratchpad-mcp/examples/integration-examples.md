# Integration Examples

Real-world usage patterns for Scratchpad MCP.

## Research Workflow

### Quick Fact Check
```
Use research_factcheck with:
- claim: "Electric vehicles produce more lifetime emissions than gas cars"
```

### Compare Technologies
```
Use research_compare with:
- topics: ["Kubernetes", "Docker Swarm", "Nomad"]
```

### Deep Dive Research
```
Use research_deep with:
- topic: "The impact of large language models on software development"
- depth: "deep"
- min_words: 5000
```

## Creative Writing Workflow

### Build a World
```
Use creative_world with:
- genre: "sci-fi noir"
- setting: "Mars colony in 2147"
- scope: "expansive"
```

### Develop Characters
```
Use creative_character with:
- name: "Maya Chen"
- role: "Protagonist - colony detective"
- traits: ["cynical", "brilliant", "haunted past", "reluctant hero"]
```

### Generate Plot
```
Use creative_plot with:
- premise: "A detective on Mars uncovers a conspiracy that threatens Earth-Mars relations"
- genre: "sci-fi noir"
- chapters: 15
```

### Write Chapter
```
Use creative_chapter with:
- story_id: "mars-noir"
- chapter_number: 1
- outline: "Maya investigates a murder in the lower domes. Clues point to corporate sabotage."
- word_target: 8000
```

## Multi-Model Orchestration

### Code Review Chain
```
Use model_chain with:
- prompt: "Review this code for security issues: [code]"
- chain: [
    {"model": "claude", "transform": "Analyze for security vulnerabilities: {input}"},
    {"model": "openai", "transform": "Critique and expand on this security analysis: {input}"},
    {"model": "claude", "transform": "Synthesize into final security report: {input}"}
  ]
```

### Research with Live Sources
```
Use model_consensus with:
- prompt: "What are the latest developments in quantum computing?"
- models: ["perplexity", "claude", "gemini"]
```

### Task-Based Routing
```
Use model_smart_route with:
- prompt: "Write a haiku about programming"
- task_type: "creative"
```

## Cognitive Operations

### Full Analysis
```
Use cognitive_analyze with:
- input: "Our startup is deciding between building a mobile app or a web app first"
- operations: [
    "attention_focus",
    "theory_of_mind",
    "constraint_check",
    "comparison",
    "critical_evaluation",
    "synthesis",
    "metacognition",
    "exploration"
  ]
```

### Quick Decision Support
```
Use scratchpad_reason with:
- query: "Should we migrate to microservices?"
- depth: "deep"
```

## Persona Combinations

### Blend for Balance
```
Use persona_blend with:
- prompt: "Explain quantum entanglement to a skeptical audience"
- personas: ["saganpad", "researcher"]
- weights: [0.6, 0.4]
```

### Style Transfer
```
Use creative_style_transfer with:
- text: "The function processes data and returns results"
- target_style: "Carl Sagan"
```

## Automation Ideas

### Daily Research Brief
Chain these tools:
1. `research_quick` on trending topics
2. `model_consensus` for validation
3. `persona_generate` with saganpad for engaging summary

### Novel Writing Pipeline
1. `creative_world` to establish setting
2. `creative_character` for each major character
3. `creative_plot` for structure
4. Loop: `creative_chapter` for each chapter

### Code Documentation
1. Read code files
2. `cognitive_analyze` with abstraction and key_extraction
3. `persona_generate` with researcher for technical docs
4. `persona_generate` with standard for user-friendly docs
