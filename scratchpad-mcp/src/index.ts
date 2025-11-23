#!/usr/bin/env node
/**
 * Scratchpad MCP Server
 * Unified AI Orchestration - Cognitive Operations, Personas, Multi-Model Routing
 *
 * A flexible, extensible MCP server that provides:
 * - Cognitive operations from the Scratchpad framework
 * - Dynamic persona switching (Saganpad, GilfoyleBot, Researcher, Novelist)
 * - Multi-model orchestration (Claude, GPT, Gemini, Perplexity)
 * - Research and creative writing tools
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { z } from 'zod';

import { loadConfig } from './utils/config.js';
import { COGNITIVE_OPERATIONS, createScratchpadBlock, executeCognitiveChain } from './tools/cognitive.js';
import { personaEngine, PERSONAS } from './personas/engine.js';
import { modelRouter } from './models/router.js';
import { researchEngine } from './research/tools.js';
import { creativeEngine } from './creative/tools.js';
import type { CognitiveOperation, PersonaName, ModelProvider } from './types.js';

// Initialize server
const server = new Server(
  {
    name: 'scratchpad-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
      resources: {},
    },
  }
);

// Tool definitions
const TOOLS = [
  // === COGNITIVE OPERATIONS ===
  {
    name: 'cognitive_analyze',
    description: 'Apply Scratchpad cognitive operations to analyze input. Supports: attention_focus, theory_of_mind, inference, synthesis, metacognition, and more.',
    inputSchema: {
      type: 'object',
      properties: {
        input: { type: 'string', description: 'The input to analyze' },
        operations: {
          type: 'array',
          items: { type: 'string' },
          description: 'Cognitive operations to apply (e.g., ["attention_focus", "theory_of_mind", "synthesis"])'
        },
        persona: { type: 'string', description: 'Optional persona to use (standard, saganpad, gilfoylebot, researcher, novelist)' }
      },
      required: ['input']
    }
  },
  {
    name: 'scratchpad_reason',
    description: 'Generate a full Scratchpad reasoning block with visible cognitive operations',
    inputSchema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'The query or problem to reason through' },
        depth: {
          type: 'string',
          enum: ['quick', 'standard', 'deep'],
          description: 'Reasoning depth (quick=3 ops, standard=6 ops, deep=all ops)'
        }
      },
      required: ['query']
    }
  },

  // === PERSONA MANAGEMENT ===
  {
    name: 'persona_switch',
    description: 'Switch to a different AI persona (saganpad, gilfoylebot, researcher, novelist, standard)',
    inputSchema: {
      type: 'object',
      properties: {
        persona: {
          type: 'string',
          enum: ['standard', 'saganpad', 'gilfoylebot', 'researcher', 'novelist'],
          description: 'The persona to activate'
        }
      },
      required: ['persona']
    }
  },
  {
    name: 'persona_generate',
    description: 'Generate a response using a specific persona',
    inputSchema: {
      type: 'object',
      properties: {
        prompt: { type: 'string', description: 'The prompt to respond to' },
        persona: { type: 'string', description: 'Persona to use' }
      },
      required: ['prompt', 'persona']
    }
  },
  {
    name: 'persona_blend',
    description: 'Blend multiple personas for a hybrid response',
    inputSchema: {
      type: 'object',
      properties: {
        prompt: { type: 'string', description: 'The prompt to respond to' },
        personas: {
          type: 'array',
          items: { type: 'string' },
          description: 'Personas to blend'
        },
        weights: {
          type: 'array',
          items: { type: 'number' },
          description: 'Optional weights for each persona (0-1, should sum to 1)'
        }
      },
      required: ['prompt', 'personas']
    }
  },

  // === MULTI-MODEL ORCHESTRATION ===
  {
    name: 'model_generate',
    description: 'Generate a response using a specific AI model',
    inputSchema: {
      type: 'object',
      properties: {
        prompt: { type: 'string', description: 'The prompt' },
        model: {
          type: 'string',
          enum: ['claude', 'openai', 'gemini', 'perplexity'],
          description: 'Model to use'
        },
        persona: { type: 'string', description: 'Optional persona for system prompt' }
      },
      required: ['prompt', 'model']
    }
  },
  {
    name: 'model_consensus',
    description: 'Get consensus from multiple AI models - they all respond, then synthesize',
    inputSchema: {
      type: 'object',
      properties: {
        prompt: { type: 'string', description: 'The prompt to send to all models' },
        models: {
          type: 'array',
          items: { type: 'string' },
          description: 'Models to query (default: all available)'
        }
      },
      required: ['prompt']
    }
  },
  {
    name: 'model_chain',
    description: 'Chain models: output of one becomes input to next',
    inputSchema: {
      type: 'object',
      properties: {
        prompt: { type: 'string', description: 'Initial prompt' },
        chain: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              model: { type: 'string' },
              transform: { type: 'string', description: 'Optional transform template. Use {input} for previous output' }
            }
          },
          description: 'Chain of models and optional transforms'
        }
      },
      required: ['prompt', 'chain']
    }
  },
  {
    name: 'model_smart_route',
    description: 'Automatically route to best model(s) based on task type',
    inputSchema: {
      type: 'object',
      properties: {
        prompt: { type: 'string', description: 'The prompt' },
        task_type: {
          type: 'string',
          enum: ['research', 'creative', 'code', 'analysis', 'chat'],
          description: 'Type of task for optimal routing'
        }
      },
      required: ['prompt', 'task_type']
    }
  },

  // === RESEARCH TOOLS ===
  {
    name: 'research_deep',
    description: 'Conduct deep research on a topic with comprehensive report (10,000+ words for exhaustive)',
    inputSchema: {
      type: 'object',
      properties: {
        topic: { type: 'string', description: 'Research topic' },
        depth: {
          type: 'string',
          enum: ['quick', 'standard', 'deep', 'exhaustive'],
          description: 'Research depth'
        },
        min_words: { type: 'number', description: 'Minimum words for report' }
      },
      required: ['topic']
    }
  },
  {
    name: 'research_quick',
    description: 'Quick research overview (800-1200 words)',
    inputSchema: {
      type: 'object',
      properties: {
        topic: { type: 'string', description: 'Topic to research' }
      },
      required: ['topic']
    }
  },
  {
    name: 'research_compare',
    description: 'Compare multiple topics or concepts',
    inputSchema: {
      type: 'object',
      properties: {
        topics: {
          type: 'array',
          items: { type: 'string' },
          description: 'Topics to compare'
        }
      },
      required: ['topics']
    }
  },
  {
    name: 'research_factcheck',
    description: 'Fact-check a claim using multiple sources',
    inputSchema: {
      type: 'object',
      properties: {
        claim: { type: 'string', description: 'The claim to verify' }
      },
      required: ['claim']
    }
  },
  {
    name: 'research_plan',
    description: 'Generate a research plan for a topic',
    inputSchema: {
      type: 'object',
      properties: {
        topic: { type: 'string', description: 'Topic to plan research for' },
        timeframe: { type: 'string', description: 'Scope/timeframe description' }
      },
      required: ['topic']
    }
  },

  // === CREATIVE WRITING TOOLS ===
  {
    name: 'creative_chapter',
    description: 'Generate a novel chapter (8,000+ words) with full scene architecture',
    inputSchema: {
      type: 'object',
      properties: {
        story_id: { type: 'string', description: 'Story identifier for context tracking' },
        chapter_number: { type: 'number', description: 'Chapter number' },
        outline: { type: 'string', description: 'Chapter outline/summary' },
        word_target: { type: 'number', description: 'Target word count (default 8000)' }
      },
      required: ['story_id', 'chapter_number', 'outline']
    }
  },
  {
    name: 'creative_scene',
    description: 'Generate a vivid scene with sensory immersion',
    inputSchema: {
      type: 'object',
      properties: {
        description: { type: 'string', description: 'Scene description' },
        characters: {
          type: 'array',
          items: { type: 'string' },
          description: 'Characters in scene'
        },
        mood: { type: 'string', description: 'Mood/atmosphere' },
        word_target: { type: 'number', description: 'Target words (default 2000)' }
      },
      required: ['description', 'characters', 'mood']
    }
  },
  {
    name: 'creative_dialogue',
    description: 'Generate character dialogue with subtext',
    inputSchema: {
      type: 'object',
      properties: {
        characters: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              name: { type: 'string' },
              role: { type: 'string' },
              traits: { type: 'array', items: { type: 'string' } }
            }
          },
          description: 'Character profiles'
        },
        situation: { type: 'string', description: 'Situation/context' },
        subtext: { type: 'string', description: 'Underlying subtext/tension' },
        length: { type: 'string', enum: ['short', 'medium', 'long'] }
      },
      required: ['characters', 'situation', 'subtext']
    }
  },
  {
    name: 'creative_character',
    description: 'Develop a deep character profile',
    inputSchema: {
      type: 'object',
      properties: {
        name: { type: 'string', description: 'Character name' },
        role: { type: 'string', description: 'Role in story' },
        traits: {
          type: 'array',
          items: { type: 'string' },
          description: 'Initial character traits'
        }
      },
      required: ['name', 'role', 'traits']
    }
  },
  {
    name: 'creative_world',
    description: 'Build a world for your story',
    inputSchema: {
      type: 'object',
      properties: {
        genre: { type: 'string', description: 'Story genre' },
        setting: { type: 'string', description: 'Basic setting description' },
        scope: { type: 'string', enum: ['focused', 'expansive'] }
      },
      required: ['genre', 'setting']
    }
  },
  {
    name: 'creative_plot',
    description: 'Generate a detailed plot outline',
    inputSchema: {
      type: 'object',
      properties: {
        premise: { type: 'string', description: 'Story premise' },
        genre: { type: 'string', description: 'Genre' },
        chapters: { type: 'number', description: 'Target number of chapters' }
      },
      required: ['premise', 'genre']
    }
  },
  {
    name: 'creative_style_transfer',
    description: 'Rewrite text in a different author\'s style',
    inputSchema: {
      type: 'object',
      properties: {
        text: { type: 'string', description: 'Text to transform' },
        target_style: { type: 'string', description: 'Target style (e.g., "Hemingway", "Tolkien", "cyberpunk")' }
      },
      required: ['text', 'target_style']
    }
  },

  // === UTILITY TOOLS ===
  {
    name: 'list_personas',
    description: 'List all available personas with descriptions',
    inputSchema: { type: 'object', properties: {} }
  },
  {
    name: 'list_cognitive_ops',
    description: 'List all available cognitive operations',
    inputSchema: { type: 'object', properties: {} }
  },
  {
    name: 'list_models',
    description: 'List available AI models and their status',
    inputSchema: { type: 'object', properties: {} }
  },
  {
    name: 'get_system_prompt',
    description: 'Get the system prompt for a persona (useful for copying)',
    inputSchema: {
      type: 'object',
      properties: {
        persona: { type: 'string', description: 'Persona name' }
      },
      required: ['persona']
    }
  }
];

// Handle list tools request
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools: TOOLS };
});

// Handle tool execution
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      // === COGNITIVE OPERATIONS ===
      case 'cognitive_analyze': {
        const input = args?.input as string;
        const operations = (args?.operations as CognitiveOperation[]) || ['attention_focus', 'theory_of_mind', 'synthesis'];
        const persona = args?.persona as PersonaName | undefined;

        if (persona) personaEngine.setPersona(persona);

        const systemPrompt = personaEngine.getSystemPrompt();
        const results = await executeCognitiveChain(
          operations,
          input,
          async (prompt) => {
            const response = await modelRouter.generateSingle('claude', prompt, systemPrompt);
            return response.content;
          }
        );

        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              operations: results.map(r => ({
                operation: r.operation,
                name: COGNITIVE_OPERATIONS[r.operation].name,
                output: r.output,
                confidence: r.confidence
              })),
              persona: personaEngine.getCurrentPersona()
            }, null, 2)
          }]
        };
      }

      case 'scratchpad_reason': {
        const query = args?.query as string;
        const depth = (args?.depth as string) || 'standard';

        const depthOps: Record<string, CognitiveOperation[]> = {
          quick: ['attention_focus', 'inference', 'key_extraction'],
          standard: ['attention_focus', 'theory_of_mind', 'constraint_check', 'reasoning_pathway', 'synthesis', 'metacognition'],
          deep: Object.keys(COGNITIVE_OPERATIONS) as CognitiveOperation[]
        };

        const operations = depthOps[depth] || depthOps.standard;
        const scratchpadBlock = createScratchpadBlock(operations, query);

        return {
          content: [{
            type: 'text',
            text: scratchpadBlock
          }]
        };
      }

      // === PERSONA MANAGEMENT ===
      case 'persona_switch': {
        const persona = args?.persona as PersonaName;
        personaEngine.setPersona(persona);
        return {
          content: [{
            type: 'text',
            text: `Switched to persona: ${persona}\n\nSystem prompt preview:\n${personaEngine.getSystemPrompt().slice(0, 500)}...`
          }]
        };
      }

      case 'persona_generate': {
        const prompt = args?.prompt as string;
        const persona = args?.persona as PersonaName;
        const systemPrompt = personaEngine.getSystemPrompt(persona);

        const response = await modelRouter.generateSingle('claude', prompt, systemPrompt);
        return {
          content: [{
            type: 'text',
            text: response.content
          }]
        };
      }

      case 'persona_blend': {
        const prompt = args?.prompt as string;
        const personas = args?.personas as PersonaName[];
        const weights = args?.weights as number[] | undefined;

        const blendedSystemPrompt = personaEngine.blendPersonas(personas, weights);
        const response = await modelRouter.generateSingle('claude', prompt, blendedSystemPrompt);

        return {
          content: [{
            type: 'text',
            text: response.content
          }]
        };
      }

      // === MULTI-MODEL ORCHESTRATION ===
      case 'model_generate': {
        const prompt = args?.prompt as string;
        const model = args?.model as ModelProvider;
        const persona = args?.persona as PersonaName | undefined;

        const systemPrompt = persona ? personaEngine.getSystemPrompt(persona) : undefined;
        const response = await modelRouter.generateSingle(model, prompt, systemPrompt);

        return {
          content: [{
            type: 'text',
            text: response.error ? `Error: ${response.error}` : response.content
          }]
        };
      }

      case 'model_consensus': {
        const prompt = args?.prompt as string;
        const models = (args?.models as ModelProvider[]) || modelRouter.getAvailableModels();

        const result = await modelRouter.generateConsensus(models, prompt);
        return {
          content: [{
            type: 'text',
            text: `## Consensus Response\n\n${result.synthesis}\n\n---\n\n### Individual Model Responses\n\n${
              result.responses.map(r => `**${r.provider}** (${r.latency}ms):\n${r.content.slice(0, 500)}...`).join('\n\n')
            }`
          }]
        };
      }

      case 'model_chain': {
        const prompt = args?.prompt as string;
        const chain = args?.chain as Array<{ model: ModelProvider; transform?: string }>;

        const chainConfig = chain.map(c => ({
          provider: c.model,
          transform: c.transform
        }));

        const result = await modelRouter.generateChain(chainConfig, prompt);
        return {
          content: [{
            type: 'text',
            text: `## Chain Result\n\n${result.final}\n\n---\n\n### Steps\n\n${
              result.steps.map((s, i) => `**Step ${i + 1} (${s.provider}):**\n${s.content.slice(0, 300)}...`).join('\n\n')
            }`
          }]
        };
      }

      case 'model_smart_route': {
        const prompt = args?.prompt as string;
        const taskType = args?.task_type as 'research' | 'creative' | 'code' | 'analysis' | 'chat';

        const result = await modelRouter.smartRoute(prompt, taskType);
        return {
          content: [{
            type: 'text',
            text: result.success ? (result.data as string) : `Error: ${result.error}`
          }]
        };
      }

      // === RESEARCH TOOLS ===
      case 'research_deep': {
        const topic = args?.topic as string;
        const depth = (args?.depth as 'quick' | 'standard' | 'deep' | 'exhaustive') || 'standard';
        const minWords = args?.min_words as number | undefined;

        const result = await researchEngine.conductResearch({
          topic,
          depth,
          requireCitations: true,
          minWords
        });

        return {
          content: [{
            type: 'text',
            text: result.fullReport || result.summary
          }]
        };
      }

      case 'research_quick': {
        const topic = args?.topic as string;
        const result = await researchEngine.quickResearch(topic);
        return { content: [{ type: 'text', text: result }] };
      }

      case 'research_compare': {
        const topics = args?.topics as string[];
        const result = await researchEngine.compareTopics(topics);
        return { content: [{ type: 'text', text: result }] };
      }

      case 'research_factcheck': {
        const claim = args?.claim as string;
        const result = await researchEngine.factCheck(claim);
        return {
          content: [{
            type: 'text',
            text: `## Fact Check Result\n\n**Verdict:** ${result.verdict.toUpperCase()}\n**Confidence:** ${(result.confidence * 100).toFixed(0)}%\n\n### Analysis\n\n${result.explanation}`
          }]
        };
      }

      case 'research_plan': {
        const topic = args?.topic as string;
        const timeframe = (args?.timeframe as string) || 'comprehensive';
        const result = await researchEngine.generateResearchPlan(topic, timeframe);
        return { content: [{ type: 'text', text: result }] };
      }

      // === CREATIVE WRITING TOOLS ===
      case 'creative_chapter': {
        const storyId = args?.story_id as string;
        const chapterNumber = args?.chapter_number as number;
        const outline = args?.outline as string;
        const wordTarget = args?.word_target as number | undefined;

        const result = await creativeEngine.generateChapter(storyId, chapterNumber, outline, {
          type: 'chapter',
          wordTarget,
          planFirst: true
        });

        return { content: [{ type: 'text', text: result }] };
      }

      case 'creative_scene': {
        const description = args?.description as string;
        const characters = args?.characters as string[];
        const mood = args?.mood as string;
        const wordTarget = args?.word_target as number | undefined;

        const result = await creativeEngine.generateScene(description, characters, mood, wordTarget);
        return { content: [{ type: 'text', text: result }] };
      }

      case 'creative_dialogue': {
        const characters = args?.characters as Array<{ name: string; role: string; traits: string[] }>;
        const situation = args?.situation as string;
        const subtext = args?.subtext as string;
        const length = (args?.length as 'short' | 'medium' | 'long') || 'medium';

        const result = await creativeEngine.generateDialogue(
          characters.map(c => ({ ...c, name: c.name, role: c.role, traits: c.traits })),
          situation,
          subtext,
          length
        );
        return { content: [{ type: 'text', text: result }] };
      }

      case 'creative_character': {
        const name = args?.name as string;
        const role = args?.role as string;
        const traits = args?.traits as string[];

        const result = await creativeEngine.developCharacter(name, role, traits);
        return {
          content: [{
            type: 'text',
            text: `## Character Profile: ${result.name}\n\n**Role:** ${result.role}\n**Traits:** ${result.traits.join(', ')}\n\n${result.backstory}`
          }]
        };
      }

      case 'creative_world': {
        const genre = args?.genre as string;
        const setting = args?.setting as string;
        const scope = (args?.scope as 'focused' | 'expansive') || 'focused';

        const result = await creativeEngine.buildWorld(genre, setting, scope);
        return { content: [{ type: 'text', text: result }] };
      }

      case 'creative_plot': {
        const premise = args?.premise as string;
        const genre = args?.genre as string;
        const chapters = args?.chapters as number | undefined;

        const result = await creativeEngine.generatePlotOutline(premise, genre, chapters);
        return { content: [{ type: 'text', text: result }] };
      }

      case 'creative_style_transfer': {
        const text = args?.text as string;
        const targetStyle = args?.target_style as string;

        const result = await creativeEngine.styleTransfer(text, targetStyle);
        return { content: [{ type: 'text', text: result }] };
      }

      // === UTILITY TOOLS ===
      case 'list_personas': {
        const personas = personaEngine.listPersonas();
        const descriptions = personas.map(p => {
          const persona = PERSONAS[p as PersonaName];
          return `**${p}**: ${persona?.systemPrompt.slice(0, 150)}...`;
        });

        return {
          content: [{
            type: 'text',
            text: `## Available Personas\n\n${descriptions.join('\n\n')}`
          }]
        };
      }

      case 'list_cognitive_ops': {
        const ops = Object.entries(COGNITIVE_OPERATIONS).map(([key, value]) =>
          `**${key}** (${value.name}): ${value.description}`
        );

        return {
          content: [{
            type: 'text',
            text: `## Cognitive Operations\n\n${ops.join('\n\n')}`
          }]
        };
      }

      case 'list_models': {
        const available = modelRouter.getAvailableModels();
        const config = loadConfig();

        const modelList = Object.keys(config.models.available).map(m => {
          const isAvailable = available.includes(m as ModelProvider);
          return `**${m}**: ${isAvailable ? '✅ Available' : '❌ Not configured (missing API key)'}`;
        });

        return {
          content: [{
            type: 'text',
            text: `## Available Models\n\n${modelList.join('\n')}\n\nCurrent primary: ${config.models.primary}`
          }]
        };
      }

      case 'get_system_prompt': {
        const persona = args?.persona as PersonaName;
        const systemPrompt = personaEngine.getSystemPrompt(persona);

        return {
          content: [{
            type: 'text',
            text: `## System Prompt: ${persona}\n\n\`\`\`\n${systemPrompt}\n\`\`\``
          }]
        };
      }

      default:
        return {
          content: [{
            type: 'text',
            text: `Unknown tool: ${name}`
          }],
          isError: true
        };
    }
  } catch (error) {
    return {
      content: [{
        type: 'text',
        text: `Error executing ${name}: ${error instanceof Error ? error.message : 'Unknown error'}`
      }],
      isError: true
    };
  }
});

// Handle resources (expose personas and frameworks as readable resources)
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: 'scratchpad://personas/saganpad',
        name: 'Saganpad Persona',
        description: 'Carl Sagan-inspired persona with cosmic perspective',
        mimeType: 'text/plain'
      },
      {
        uri: 'scratchpad://personas/gilfoylebot',
        name: 'GilfoyleBot Persona',
        description: 'Deadpan, sardonic assistant persona',
        mimeType: 'text/plain'
      },
      {
        uri: 'scratchpad://personas/researcher',
        name: 'Deep Researcher Persona',
        description: 'Academic research assistant',
        mimeType: 'text/plain'
      },
      {
        uri: 'scratchpad://personas/novelist',
        name: 'Novelist Persona',
        description: 'Creative writing assistant',
        mimeType: 'text/plain'
      },
      {
        uri: 'scratchpad://framework/cognitive-ops',
        name: 'Cognitive Operations Reference',
        description: 'All available cognitive operations and their descriptions',
        mimeType: 'text/plain'
      }
    ]
  };
});

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;

  if (uri.startsWith('scratchpad://personas/')) {
    const personaName = uri.replace('scratchpad://personas/', '') as PersonaName;
    const systemPrompt = personaEngine.getSystemPrompt(personaName);
    return {
      contents: [{
        uri,
        mimeType: 'text/plain',
        text: systemPrompt
      }]
    };
  }

  if (uri === 'scratchpad://framework/cognitive-ops') {
    const ops = Object.entries(COGNITIVE_OPERATIONS).map(([key, value]) =>
      `## ${value.name} (${key})\n\n${value.description}\n\n### Prompt Template:\n${value.prompt}`
    ).join('\n\n---\n\n');

    return {
      contents: [{
        uri,
        mimeType: 'text/plain',
        text: ops
      }]
    };
  }

  throw new Error(`Resource not found: ${uri}`);
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Scratchpad MCP Server running on stdio');
}

main().catch(console.error);
