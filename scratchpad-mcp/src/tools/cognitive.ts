// Core Cognitive Operations Module
// Implements the Scratchpad reasoning framework as callable tools

import type { CognitiveOperation, CognitiveResult } from '../types.js';

export const COGNITIVE_OPERATIONS: Record<CognitiveOperation, {
  name: string;
  description: string;
  prompt: string;
}> = {
  attention_focus: {
    name: 'Attention Focus',
    description: 'Identify critical elements and potential distractions in the query',
    prompt: `Analyze this input and identify:
1. PRIMARY FOCUS: What is the core question/task?
2. CRITICAL ELEMENTS: What details are essential to address?
3. DISTRACTIONS: What might lead to tangential responses?
4. HIDDEN REQUIREMENTS: What implicit needs exist?

Input: {input}

Provide structured analysis.`
  },

  theory_of_mind: {
    name: 'Theory of Mind',
    description: 'Analyze user perspective, assumptions, and underlying needs',
    prompt: `Apply Theory of Mind analysis:
1. USER PERSPECTIVE: What is their likely background/expertise?
2. ASSUMPTIONS: What do they assume I already know?
3. UNDERLYING NEEDS: Beyond the literal request, what do they really want?
4. COMMUNICATION STYLE: How should I calibrate my response?
5. POTENTIAL FRUSTRATIONS: What might confuse or disappoint them?

Input: {input}

Provide empathetic analysis.`
  },

  clarity_goal: {
    name: 'Clarity/Accuracy Goal',
    description: 'State the overarching goal for this reasoning process',
    prompt: `Define the clarity and accuracy goal:
1. PRIMARY OBJECTIVE: What must this response achieve?
2. SUCCESS CRITERIA: How will we know the response succeeded?
3. ACCURACY REQUIREMENTS: What level of precision is needed?
4. CLARITY STANDARD: How should information be structured?

Input: {input}

State the goal clearly.`
  },

  revision_query: {
    name: 'Revision Query',
    description: 'Restate the request in your own words for calibration',
    prompt: `Restate this request to demonstrate understanding:
1. MY UNDERSTANDING: In my own words, the user is asking...
2. KEY DELIVERABLES: They expect me to provide...
3. CONSTRAINTS NOTED: I should avoid/include...
4. CLARIFICATION NEEDED: If anything is unclear...

Input: {input}

Demonstrate comprehension.`
  },

  constraint_check: {
    name: 'Constraint Check',
    description: 'Identify explicit and implicit boundaries',
    prompt: `Identify all constraints:
1. EXPLICIT CONSTRAINTS: What boundaries are stated?
2. IMPLICIT CONSTRAINTS: What limits are implied by context?
3. ETHICAL BOUNDARIES: What should be avoided?
4. RESOURCE CONSTRAINTS: Time, length, complexity limits?
5. DOMAIN CONSTRAINTS: What's in/out of scope?

Input: {input}

List all constraints.`
  },

  context_integration: {
    name: 'Context Integration',
    description: 'Incorporate relevant prior context and background',
    prompt: `Integrate contextual information:
1. PRIOR CONTEXT: What relevant history exists?
2. DOMAIN KNOWLEDGE: What background is relevant?
3. USER HISTORY: What do we know about this user?
4. ENVIRONMENTAL FACTORS: What external context matters?

Input: {input}
Prior Context: {context}

Synthesize context.`
  },

  abstraction: {
    name: 'Abstraction',
    description: 'Elevate to higher-level patterns and principles',
    prompt: `Apply abstraction:
1. PATTERN RECOGNITION: What general patterns apply here?
2. UNDERLYING PRINCIPLES: What fundamental concepts are at play?
3. CATEGORY MEMBERSHIP: What class of problems is this?
4. TRANSFERABLE INSIGHTS: What learnings generalize?

Input: {input}

Identify abstractions.`
  },

  comparison: {
    name: 'Comparison',
    description: 'Compare and contrast relevant options or approaches',
    prompt: `Perform comparative analysis:
1. OPTIONS IDENTIFIED: What alternatives exist?
2. SIMILARITIES: What do they have in common?
3. DIFFERENCES: How do they diverge?
4. TRADE-OFFS: What are the pros/cons of each?
5. RECOMMENDATION: Which is optimal and why?

Input: {input}

Compare systematically.`
  },

  inference: {
    name: 'Inference',
    description: 'Draw logical conclusions from available information',
    prompt: `Apply logical inference:
1. PREMISES: What facts/assumptions are we working with?
2. LOGICAL CHAIN: What follows from these premises?
3. CERTAINTY LEVELS: How confident are each inference?
4. CONCLUSIONS: What can we definitively conclude?
5. GAPS: What inferences are we unable to make?

Input: {input}

Draw inferences.`
  },

  synthesis: {
    name: 'Synthesis',
    description: 'Combine multiple elements into coherent whole',
    prompt: `Synthesize information:
1. COMPONENTS: What elements need integration?
2. RELATIONSHIPS: How do they connect?
3. EMERGENT INSIGHTS: What new understanding emerges from combination?
4. UNIFIED VIEW: Present the integrated perspective
5. COHERENCE CHECK: Does the synthesis hold together?

Input: {input}

Create synthesis.`
  },

  analogy: {
    name: 'Analogy',
    description: 'Find illuminating parallels and metaphors',
    prompt: `Generate analogies:
1. CORE CONCEPT: What are we trying to explain?
2. ANALOGOUS DOMAINS: What familiar concepts parallel this?
3. MAPPING: How do the elements correspond?
4. ILLUMINATION: What does the analogy clarify?
5. LIMITATIONS: Where does the analogy break down?

Input: {input}

Provide useful analogies.`
  },

  critical_evaluation: {
    name: 'Critical Evaluation',
    description: 'Assess validity, weaknesses, and counter-arguments',
    prompt: `Apply critical evaluation:
1. STRENGTHS: What is solid about this approach/argument?
2. WEAKNESSES: What are the vulnerabilities?
3. COUNTER-ARGUMENTS: What would critics say?
4. EVIDENCE QUALITY: How reliable is supporting information?
5. BIAS CHECK: What biases might be influencing analysis?
6. STEEL-MAN: What's the strongest version of opposing views?

Input: {input}

Evaluate critically.`
  },

  reasoning_pathway: {
    name: 'Reasoning Pathway',
    description: 'Outline logical steps from premises to conclusions',
    prompt: `Map the reasoning pathway:
1. STARTING POINT: What do we know/assume?
2. STEP 1: First logical move...
3. STEP 2: Following from that...
[Continue as needed]
N. DESTINATION: Therefore, we conclude...
PATHWAY VALIDATION: Is each step sound?

Input: {input}

Show your reasoning path.`
  },

  key_extraction: {
    name: 'Key Information Extraction',
    description: 'Isolate the most critical facts and data',
    prompt: `Extract key information:
1. CRITICAL FACTS: What information is essential?
2. SUPPORTING DATA: What evidence matters?
3. PRIORITY RANKING: Order by importance
4. ACTIONABLE ITEMS: What requires action?
5. REFERENCE POINTS: What might need revisiting?

Input: {input}

Extract essentials.`
  },

  metacognition: {
    name: 'Metacognition',
    description: 'Analyze the thinking process itself',
    prompt: `Apply metacognitive analysis:
1. THINKING PROCESS: How am I approaching this problem?
2. STRATEGY ASSESSMENT: Is this the best approach?
3. CONFIDENCE CALIBRATION: How certain am I, and should I be?
4. BLIND SPOTS: What might I be missing?
5. IMPROVEMENT: How could my reasoning be better?
6. ALTERNATIVE APPROACHES: What other methods could work?

Input: {input}

Reflect on reasoning.`
  },

  exploration: {
    name: 'Exploration',
    description: 'Generate thought-provoking follow-up questions',
    prompt: `Generate exploratory questions:
Given the topic/response, what 3-5 thought-provoking questions would:
1. Deepen understanding?
2. Challenge assumptions?
3. Extend to related domains?
4. Invite practical application?
5. Spark curiosity?

Input: {input}

Provide exploration questions.`
  }
};

export function getCognitivePrompt(operation: CognitiveOperation, input: string, context?: string): string {
  const op = COGNITIVE_OPERATIONS[operation];
  let prompt = op.prompt.replace('{input}', input);
  if (context) {
    prompt = prompt.replace('{context}', context);
  }
  return prompt;
}

export function buildCognitiveChain(operations: CognitiveOperation[]): string {
  return operations.map(op => {
    const config = COGNITIVE_OPERATIONS[op];
    return `## ${config.name}\n${config.description}`;
  }).join('\n\n');
}

export function createScratchpadBlock(operations: CognitiveOperation[], input: string): string {
  const blocks = operations.map(op => {
    const config = COGNITIVE_OPERATIONS[op];
    return `### ${config.name}
${config.prompt.replace('{input}', input).replace('{context}', '[Prior context if available]')}`;
  });

  return `<scratchpad>
${blocks.join('\n\n')}
</scratchpad>`;
}

export async function executeCognitiveOperation(
  operation: CognitiveOperation,
  input: string,
  executor: (prompt: string) => Promise<string>
): Promise<CognitiveResult> {
  const prompt = getCognitivePrompt(operation, input);
  const startTime = Date.now();

  try {
    const output = await executor(prompt);
    const processingTime = Date.now() - startTime;

    return {
      operation,
      output,
      confidence: 0.85, // Could be enhanced with self-assessment
      metadata: { processingTime }
    };
  } catch (error) {
    return {
      operation,
      output: `Error executing ${operation}: ${error}`,
      confidence: 0,
      metadata: { error: true }
    };
  }
}

export async function executeCognitiveChain(
  operations: CognitiveOperation[],
  input: string,
  executor: (prompt: string) => Promise<string>
): Promise<CognitiveResult[]> {
  const results: CognitiveResult[] = [];
  let accumulatedContext = input;

  for (const operation of operations) {
    const result = await executeCognitiveOperation(operation, accumulatedContext, executor);
    results.push(result);
    // Build context for next operation
    accumulatedContext = `${input}\n\nPrior Analysis:\n${result.output}`;
  }

  return results;
}
