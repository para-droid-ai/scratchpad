// Multi-Model Router - Orchestrate multiple AI providers
// Supports parallel execution, consensus, chaining, and fallback

import Anthropic from '@anthropic-ai/sdk';
import OpenAI from 'openai';
import { GoogleGenerativeAI } from '@google/generative-ai';
import { getApiKey, isModelEnabled, loadConfig } from '../utils/config.js';
import type { ModelProvider, OrchestrationConfig, ToolResponse } from '../types.js';

interface ModelResponse {
  provider: ModelProvider;
  content: string;
  confidence?: number;
  latency: number;
  error?: string;
}

interface ModelClient {
  provider: ModelProvider;
  generate: (prompt: string, systemPrompt?: string) => Promise<string>;
}

export class ModelRouter {
  private clients: Map<ModelProvider, ModelClient> = new Map();
  private defaultOrchestration: OrchestrationConfig = {
    mode: 'single',
    models: ['claude'],
    synthesisStrategy: 'best'
  };

  constructor() {
    this.initializeClients();
  }

  private initializeClients(): void {
    const config = loadConfig();

    // Initialize Claude
    if (isModelEnabled('claude')) {
      const client = new Anthropic({ apiKey: getApiKey('claude') });
      const modelId = config.models.available.claude.model;

      this.clients.set('claude', {
        provider: 'claude',
        generate: async (prompt: string, systemPrompt?: string) => {
          const response = await client.messages.create({
            model: modelId,
            max_tokens: 8192,
            system: systemPrompt || 'You are a helpful assistant.',
            messages: [{ role: 'user', content: prompt }]
          });
          return response.content[0].type === 'text' ? response.content[0].text : '';
        }
      });
    }

    // Initialize OpenAI
    if (isModelEnabled('openai')) {
      const client = new OpenAI({ apiKey: getApiKey('openai') });
      const modelId = config.models.available.openai.model;

      this.clients.set('openai', {
        provider: 'openai',
        generate: async (prompt: string, systemPrompt?: string) => {
          const response = await client.chat.completions.create({
            model: modelId,
            messages: [
              { role: 'system', content: systemPrompt || 'You are a helpful assistant.' },
              { role: 'user', content: prompt }
            ],
            max_tokens: 8192
          });
          return response.choices[0]?.message?.content || '';
        }
      });
    }

    // Initialize Gemini
    if (isModelEnabled('gemini')) {
      const genAI = new GoogleGenerativeAI(getApiKey('gemini')!);
      const modelId = config.models.available.gemini.model;

      this.clients.set('gemini', {
        provider: 'gemini',
        generate: async (prompt: string, systemPrompt?: string) => {
          const model = genAI.getGenerativeModel({
            model: modelId,
            systemInstruction: systemPrompt
          });
          const result = await model.generateContent(prompt);
          return result.response.text();
        }
      });
    }

    // Initialize Perplexity (OpenAI-compatible API)
    if (isModelEnabled('perplexity')) {
      const client = new OpenAI({
        apiKey: getApiKey('perplexity'),
        baseURL: 'https://api.perplexity.ai'
      });
      const modelId = config.models.available.perplexity.model;

      this.clients.set('perplexity', {
        provider: 'perplexity',
        generate: async (prompt: string, systemPrompt?: string) => {
          const response = await client.chat.completions.create({
            model: modelId,
            messages: [
              { role: 'system', content: systemPrompt || 'You are a helpful assistant.' },
              { role: 'user', content: prompt }
            ]
          });
          return response.choices[0]?.message?.content || '';
        }
      });
    }
  }

  getAvailableModels(): ModelProvider[] {
    return Array.from(this.clients.keys());
  }

  async generateSingle(
    provider: ModelProvider,
    prompt: string,
    systemPrompt?: string
  ): Promise<ModelResponse> {
    const client = this.clients.get(provider);
    if (!client) {
      return {
        provider,
        content: '',
        latency: 0,
        error: `Provider ${provider} not available`
      };
    }

    const startTime = Date.now();
    try {
      const content = await client.generate(prompt, systemPrompt);
      return {
        provider,
        content,
        latency: Date.now() - startTime
      };
    } catch (error) {
      return {
        provider,
        content: '',
        latency: Date.now() - startTime,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  async generateParallel(
    providers: ModelProvider[],
    prompt: string,
    systemPrompt?: string
  ): Promise<ModelResponse[]> {
    const promises = providers.map(p => this.generateSingle(p, prompt, systemPrompt));
    return Promise.all(promises);
  }

  async generateWithFallback(
    providers: ModelProvider[],
    prompt: string,
    systemPrompt?: string
  ): Promise<ModelResponse> {
    for (const provider of providers) {
      const response = await this.generateSingle(provider, prompt, systemPrompt);
      if (!response.error && response.content) {
        return response;
      }
    }
    return {
      provider: providers[0],
      content: '',
      latency: 0,
      error: 'All providers failed'
    };
  }

  async generateConsensus(
    providers: ModelProvider[],
    prompt: string,
    systemPrompt?: string
  ): Promise<{ responses: ModelResponse[]; synthesis: string }> {
    const responses = await this.generateParallel(providers, prompt, systemPrompt);
    const validResponses = responses.filter(r => !r.error && r.content);

    if (validResponses.length === 0) {
      return { responses, synthesis: 'All models failed to generate responses.' };
    }

    if (validResponses.length === 1) {
      return { responses, synthesis: validResponses[0].content };
    }

    // Use Claude (or first available) to synthesize
    const synthesisPrompt = `You have received responses from multiple AI models to the same query.
Your task is to synthesize these into a single, coherent response that:
1. Identifies points of agreement (high confidence)
2. Notes significant disagreements
3. Combines the best insights from each
4. Produces a unified, superior response

Original query: ${prompt}

Model responses:
${validResponses.map(r => `--- ${r.provider.toUpperCase()} ---\n${r.content}`).join('\n\n')}

Provide a synthesized response:`;

    const synthesizer = this.clients.get('claude') || this.clients.get(validResponses[0].provider);
    if (synthesizer) {
      try {
        const synthesis = await synthesizer.generate(synthesisPrompt);
        return { responses, synthesis };
      } catch {
        return { responses, synthesis: validResponses[0].content };
      }
    }

    return { responses, synthesis: validResponses[0].content };
  }

  async generateChain(
    chain: Array<{ provider: ModelProvider; transform?: string }>,
    initialPrompt: string,
    systemPrompt?: string
  ): Promise<{ steps: ModelResponse[]; final: string }> {
    const steps: ModelResponse[] = [];
    let currentContent = initialPrompt;

    for (const step of chain) {
      const prompt = step.transform
        ? step.transform.replace('{input}', currentContent)
        : currentContent;

      const response = await this.generateSingle(step.provider, prompt, systemPrompt);
      steps.push(response);

      if (response.error) {
        return { steps, final: `Chain failed at ${step.provider}: ${response.error}` };
      }

      currentContent = response.content;
    }

    return { steps, final: currentContent };
  }

  async orchestrate(
    config: OrchestrationConfig,
    prompt: string,
    systemPrompt?: string
  ): Promise<ToolResponse> {
    const startTime = Date.now();

    try {
      switch (config.mode) {
        case 'single': {
          const response = await this.generateSingle(config.models[0], prompt, systemPrompt);
          return {
            success: !response.error,
            data: response.content,
            error: response.error,
            metadata: {
              model: response.provider,
              processingTime: Date.now() - startTime
            }
          };
        }

        case 'parallel': {
          const responses = await this.generateParallel(config.models, prompt, systemPrompt);
          return {
            success: responses.some(r => !r.error),
            data: responses.map(r => ({ provider: r.provider, content: r.content })),
            metadata: { processingTime: Date.now() - startTime }
          };
        }

        case 'consensus': {
          const result = await this.generateConsensus(config.models, prompt, systemPrompt);
          return {
            success: !!result.synthesis,
            data: {
              synthesis: result.synthesis,
              individualResponses: result.responses.map(r => ({
                provider: r.provider,
                content: r.content.slice(0, 500) + '...'
              }))
            },
            metadata: { processingTime: Date.now() - startTime }
          };
        }

        case 'chain': {
          const chainConfig = config.models.map(m => ({ provider: m }));
          const result = await this.generateChain(chainConfig, prompt, systemPrompt);
          return {
            success: !!result.final,
            data: result.final,
            metadata: {
              processingTime: Date.now() - startTime
            }
          };
        }

        default:
          return {
            success: false,
            error: `Unknown orchestration mode: ${config.mode}`
          };
      }
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
        metadata: { processingTime: Date.now() - startTime }
      };
    }
  }

  // Specialized routing based on task type
  async smartRoute(
    prompt: string,
    taskType: 'research' | 'creative' | 'code' | 'analysis' | 'chat',
    systemPrompt?: string
  ): Promise<ToolResponse> {
    const routingStrategies: Record<string, OrchestrationConfig> = {
      research: {
        mode: 'consensus',
        models: ['perplexity', 'claude', 'gemini'] as ModelProvider[],
        synthesisStrategy: 'merge'
      },
      creative: {
        mode: 'single',
        models: ['claude'] as ModelProvider[]
      },
      code: {
        mode: 'chain',
        models: ['claude', 'openai'] as ModelProvider[] // Claude writes, GPT reviews
      },
      analysis: {
        mode: 'parallel',
        models: ['claude', 'gemini'] as ModelProvider[]
      },
      chat: {
        mode: 'single',
        models: ['claude'] as ModelProvider[],
        fallbackOrder: ['openai', 'gemini'] as ModelProvider[]
      }
    };

    const strategy = routingStrategies[taskType] || routingStrategies.chat;

    // Filter to only available models
    strategy.models = strategy.models.filter(m => this.clients.has(m));

    if (strategy.models.length === 0) {
      // Use any available model
      strategy.models = [this.getAvailableModels()[0]];
      strategy.mode = 'single';
    }

    return this.orchestrate(strategy, prompt, systemPrompt);
  }
}

// Singleton instance
export const modelRouter = new ModelRouter();
