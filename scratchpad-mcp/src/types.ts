// Core types for Scratchpad MCP

export type ModelProvider = 'claude' | 'openai' | 'gemini' | 'perplexity' | 'local';

export type PersonaName = 'standard' | 'saganpad' | 'gilfoylebot' | 'researcher' | 'novelist' | 'custom';

export type CognitiveOperation =
  | 'attention_focus'
  | 'theory_of_mind'
  | 'clarity_goal'
  | 'revision_query'
  | 'constraint_check'
  | 'context_integration'
  | 'abstraction'
  | 'comparison'
  | 'inference'
  | 'synthesis'
  | 'analogy'
  | 'critical_evaluation'
  | 'reasoning_pathway'
  | 'key_extraction'
  | 'metacognition'
  | 'exploration';

export interface CognitiveResult {
  operation: CognitiveOperation;
  output: string;
  confidence: number;
  metadata?: Record<string, unknown>;
}

export interface PersonaConfig {
  name: PersonaName;
  systemPrompt: string;
  voiceStyle?: string;
  responseFormat?: 'concise' | 'detailed' | 'academic' | 'creative';
  cognitiveEmphasis?: CognitiveOperation[];
}

export interface ModelConfig {
  provider: ModelProvider;
  model: string;
  apiKey?: string;
  baseUrl?: string;
  temperature?: number;
  maxTokens?: number;
}

export interface OrchestrationConfig {
  mode: 'single' | 'parallel' | 'consensus' | 'chain';
  models: ModelProvider[];
  synthesisStrategy?: 'vote' | 'merge' | 'best' | 'debate';
  fallbackOrder?: ModelProvider[];
}

export interface ResearchQuery {
  topic: string;
  depth: 'quick' | 'standard' | 'deep' | 'exhaustive';
  sources?: string[];
  requireCitations: boolean;
  minWords?: number;
}

export interface ResearchResult {
  summary: string;
  sources: SourceCitation[];
  confidence: number;
  relatedQueries: string[];
  fullReport?: string;
}

export interface SourceCitation {
  title: string;
  url?: string;
  author?: string;
  date?: string;
  relevance: number;
  excerpt?: string;
}

export interface CreativeConfig {
  type: 'chapter' | 'scene' | 'dialogue' | 'description' | 'poem' | 'script';
  wordTarget?: number;
  style?: string;
  planFirst: boolean;
  consistencyContext?: string;
}

export interface SessionContext {
  id: string;
  persona: PersonaName;
  cognitiveHistory: CognitiveResult[];
  userCalibration: Record<string, unknown>;
  conversationSummary?: string;
}

export interface ToolResponse {
  success: boolean;
  data?: unknown;
  error?: string;
  metadata?: {
    model?: ModelProvider;
    persona?: PersonaName;
    operations?: CognitiveOperation[];
    processingTime?: number;
  };
}
