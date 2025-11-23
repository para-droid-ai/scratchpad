import { readFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

dotenv.config();

const __dirname = dirname(fileURLToPath(import.meta.url));

export interface ServerConfig {
  server: { name: string; version: string };
  models: {
    primary: string;
    available: Record<string, {
      enabled: boolean;
      model: string;
      apiKeyEnv: string;
      baseUrl?: string;
    }>;
  };
  personas: {
    default: string;
    available: string[];
  };
  cognitiveOps: {
    defaultOperations: string[];
  };
  research: {
    maxSources: number;
    synthesisMinWords: number;
  };
  creative: {
    defaultChapterWords: number;
    planningRequired: boolean;
  };
}

let config: ServerConfig | null = null;

export function loadConfig(): ServerConfig {
  if (config) return config;

  const configPath = join(__dirname, '../../config/default.json');

  if (!existsSync(configPath)) {
    throw new Error(`Config file not found at ${configPath}`);
  }

  const rawConfig = readFileSync(configPath, 'utf-8');
  config = JSON.parse(rawConfig) as ServerConfig;

  return config;
}

export function getApiKey(provider: string): string | undefined {
  const cfg = loadConfig();
  const modelConfig = cfg.models.available[provider];

  if (!modelConfig) return undefined;

  return process.env[modelConfig.apiKeyEnv];
}

export function isModelEnabled(provider: string): boolean {
  const cfg = loadConfig();
  const modelConfig = cfg.models.available[provider];

  if (!modelConfig) return false;

  return modelConfig.enabled && !!getApiKey(provider);
}

export function getEnabledModels(): string[] {
  const cfg = loadConfig();
  return Object.keys(cfg.models.available).filter(isModelEnabled);
}
