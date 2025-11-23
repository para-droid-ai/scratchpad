# Scratchpad MCP Server

**Unified AI Orchestration Layer** - A flexible, extensible MCP server that brings together cognitive operations, personas, multi-model orchestration, research, and creative writing tools.

## 🚀 What This Does

Scratchpad MCP transforms your AI assistant into a powerful orchestration hub:

- **🧠 Cognitive Operations**: Apply structured reasoning (attention focus, theory of mind, metacognition, synthesis, etc.)
- **🎭 Persona Engine**: Switch between specialized personas (Saganpad, GilfoyleBot, Researcher, Novelist)
- **🔀 Multi-Model Routing**: Orchestrate Claude, GPT, Gemini, and Perplexity with parallel execution, consensus, and chaining
- **📚 Deep Research**: Conduct comprehensive research with multi-source synthesis
- **✍️ Creative Writing**: Generate novels, scenes, characters, and worlds with the Novelize Protocol

## 📦 Installation

```bash
# Navigate to the MCP server directory
cd scratchpad-mcp

# Install dependencies
npm install

# Copy environment template and add your API keys
cp .env.example .env

# Build the server
npm run build
```

## ⚙️ Configuration

### API Keys (.env)

```bash
ANTHROPIC_API_KEY=sk-ant-...    # Required for Claude
OPENAI_API_KEY=sk-...           # Optional for GPT-4/5
GOOGLE_API_KEY=...              # Optional for Gemini
PERPLEXITY_API_KEY=pplx-...     # Optional for real-time research
```

### Claude Code Integration

Add to your Claude Code MCP settings (`~/.config/claude-code/settings.json` or project `.claude/settings.json`):

```json
{
  "mcpServers": {
    "scratchpad": {
      "command": "node",
      "args": ["/path/to/scratchpad-mcp/dist/index.js"],
      "env": {
        "ANTHROPIC_API_KEY": "your-key",
        "OPENAI_API_KEY": "your-key",
        "GOOGLE_API_KEY": "your-key",
        "PERPLEXITY_API_KEY": "your-key"
      }
    }
  }
}
```

### Claude Desktop Integration

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "scratchpad": {
      "command": "node",
      "args": ["/path/to/scratchpad-mcp/dist/index.js"],
      "env": {
        "ANTHROPIC_API_KEY": "your-key"
      }
    }
  }
}
```

## 🛠️ Available Tools

### Cognitive Operations

| Tool | Description |
|------|-------------|
| `cognitive_analyze` | Apply cognitive operations to analyze input |
| `scratchpad_reason` | Generate full Scratchpad reasoning block |

### Persona Management

| Tool | Description |
|------|-------------|
| `persona_switch` | Switch active persona |
| `persona_generate` | Generate response with specific persona |
| `persona_blend` | Blend multiple personas for hybrid response |
| `list_personas` | List all available personas |
| `get_system_prompt` | Get system prompt for any persona |

### Multi-Model Orchestration

| Tool | Description |
|------|-------------|
| `model_generate` | Generate with specific model |
| `model_consensus` | Get consensus from multiple models |
| `model_chain` | Chain models (output → next input) |
| `model_smart_route` | Auto-route based on task type |
| `list_models` | List available models and status |

### Research Tools

| Tool | Description |
|------|-------------|
| `research_deep` | Comprehensive research (10,000+ words) |
| `research_quick` | Quick overview (800-1200 words) |
| `research_compare` | Compare multiple topics |
| `research_factcheck` | Fact-check claims with multi-source |
| `research_plan` | Generate research plan |

### Creative Writing

| Tool | Description |
|------|-------------|
| `creative_chapter` | Generate novel chapter (8,000+ words) |
| `creative_scene` | Generate immersive scene |
| `creative_dialogue` | Generate character dialogue |
| `creative_character` | Develop deep character profile |
| `creative_world` | Build story world |
| `creative_plot` | Generate plot outline |
| `creative_style_transfer` | Rewrite in different author's style |

## 🎭 Personas

### Saganpad
Channels Carl Sagan's cosmic perspective with wonder, skeptical inquiry, and poetic precision. Perfect for explaining complex topics with awe and humility.

### GilfoyleBot
Deadpan, sardonic assistant in the style of Silicon Valley's Gilfoyle. Competent but openly unimpressed. Great for cutting through BS.

### Researcher
Deep research assistant producing academic-quality 10,000+ word reports with proper citations and formal prose.

### Novelist
Creative writing assistant following the Novelize Protocol for publication-quality fiction with scene architecture and character consistency.

## 🧠 Cognitive Operations

The cognitive operations are based on the Scratchpad framework:

- **attention_focus**: Identify critical elements and distractions
- **theory_of_mind**: Analyze user perspective and needs
- **clarity_goal**: Define accuracy and clarity objectives
- **revision_query**: Restate request for calibration
- **constraint_check**: Identify boundaries and limits
- **context_integration**: Incorporate relevant background
- **abstraction**: Elevate to patterns and principles
- **comparison**: Compare options systematically
- **inference**: Draw logical conclusions
- **synthesis**: Combine elements coherently
- **analogy**: Find illuminating parallels
- **critical_evaluation**: Assess validity and weaknesses
- **reasoning_pathway**: Map logical steps
- **key_extraction**: Isolate critical information
- **metacognition**: Analyze the thinking process
- **exploration**: Generate follow-up questions

## 🔀 Orchestration Modes

### Single
Use one model directly.

### Parallel
Query multiple models simultaneously, return all responses.

### Consensus
Query multiple models, synthesize into unified response with confidence assessment.

### Chain
Output of one model becomes input to next. Useful for:
- Claude writes → GPT critiques → Claude refines
- Perplexity researches → Claude synthesizes → Gemini formats

## 📖 Usage Examples

### Apply Cognitive Analysis
```
Use cognitive_analyze with:
- input: "Should we use microservices or monolith?"
- operations: ["attention_focus", "comparison", "critical_evaluation", "synthesis"]
```

### Get Multi-Model Consensus
```
Use model_consensus with:
- prompt: "What are the implications of quantum computing for cryptography?"
- models: ["claude", "perplexity", "gemini"]
```

### Generate Saganpad Response
```
Use persona_generate with:
- prompt: "Explain the scale of the universe"
- persona: "saganpad"
```

### Deep Research
```
Use research_deep with:
- topic: "The future of nuclear fusion energy"
- depth: "exhaustive"
- min_words: 10000
```

### Generate Novel Chapter
```
Use creative_chapter with:
- story_id: "my-novel"
- chapter_number: 1
- outline: "Protagonist discovers the hidden message..."
- word_target: 8000
```

## 🏗️ Architecture

```
scratchpad-mcp/
├── src/
│   ├── index.ts              # Main MCP server
│   ├── types.ts              # TypeScript types
│   ├── tools/
│   │   └── cognitive.ts      # Cognitive operations
│   ├── personas/
│   │   └── engine.ts         # Persona management
│   ├── models/
│   │   └── router.ts         # Multi-model orchestration
│   ├── research/
│   │   └── tools.ts          # Research engine
│   ├── creative/
│   │   └── tools.ts          # Creative writing
│   └── utils/
│       └── config.ts         # Configuration
├── config/
│   └── default.json          # Default settings
├── package.json
├── tsconfig.json
└── .env.example
```

## 🔧 Extending

### Add a Custom Persona

```typescript
import { personaEngine } from './personas/engine.js';

personaEngine.registerCustomPersona('my-persona', {
  systemPrompt: 'You are...',
  responseFormat: 'detailed',
  cognitiveEmphasis: ['synthesis', 'analogy']
});
```

### Add a New Model Provider

Add configuration to `config/default.json` and implement the client in `models/router.ts`.

## 📝 License

MIT - Based on the [Scratchpad Framework](https://github.com/para-droid-ai/scratchpad)

## 🙏 Credits

Built on the Scratchpad cognitive framework by para-droid-ai. Integrates concepts from:
- Saganpad (Carl Sagan persona)
- GilfoyleBot (Silicon Valley)
- Deep Researcher Protocol
- Novelize Protocol
