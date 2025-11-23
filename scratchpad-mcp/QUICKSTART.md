# Quick Start Guide

Get up and running with Scratchpad MCP in 5 minutes.

## 1. Install Dependencies

```bash
cd scratchpad-mcp
npm install
```

## 2. Configure API Keys

```bash
cp .env.example .env
```

Edit `.env` and add at least one API key:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

## 3. Build

```bash
npm run build
```

## 4. Add to Claude Code

Edit `~/.config/claude-code/settings.json`:

```json
{
  "mcpServers": {
    "scratchpad": {
      "command": "node",
      "args": ["/full/path/to/scratchpad-mcp/dist/index.js"],
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-your-key"
      }
    }
  }
}
```

## 5. Restart Claude Code

The tools are now available! Try:

- `list_personas` - See available personas
- `list_cognitive_ops` - See reasoning operations
- `list_models` - See configured AI models

## Quick Examples

### Saganpad Response
```
Use persona_generate with:
- prompt: "Explain why the sky is blue"
- persona: "saganpad"
```

### Cognitive Analysis
```
Use cognitive_analyze with:
- input: "Should I learn Rust or Go?"
- operations: ["attention_focus", "comparison", "critical_evaluation"]
```

### Multi-Model Consensus
```
Use model_consensus with:
- prompt: "What are the key trends in AI for 2025?"
```

## Available Slash Commands

If you're in the scratchpad repo, you also have:

- `/saganpad <topic>` - Carl Sagan perspective
- `/gilfoyle <question>` - Sardonic assistant
- `/research <topic>` - Deep research mode
- `/scratchpad <problem>` - Cognitive reasoning
- `/novelist <prompt>` - Creative writing
- `/consensus <topic>` - Multi-perspective analysis
