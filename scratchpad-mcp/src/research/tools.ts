// Research Tools - Deep research and synthesis capabilities
// Integrates with multiple AI models for comprehensive research

import { modelRouter } from '../models/router.js';
import { personaEngine } from '../personas/engine.js';
import { COGNITIVE_OPERATIONS, createScratchpadBlock } from '../tools/cognitive.js';
import type { ResearchQuery, ResearchResult, SourceCitation } from '../types.js';

export class ResearchEngine {
  async conductResearch(query: ResearchQuery): Promise<ResearchResult> {
    const systemPrompt = personaEngine.getSystemPrompt('researcher');

    // Phase 1: Query Deconstruction
    const deconstructionPrompt = `
Analyze this research query and provide structured breakdown:

QUERY: ${query.topic}
DEPTH: ${query.depth}

Provide:
1. Core research questions (3-5)
2. Key concepts to investigate
3. Potential sources/domains to explore
4. Expected structure for findings
5. Potential biases or limitations to watch for`;

    const deconstruction = await modelRouter.generateSingle('claude', deconstructionPrompt, systemPrompt);

    // Phase 2: Multi-source gathering (if multiple models available)
    const gatheringPrompt = `
Research the following topic comprehensively:

TOPIC: ${query.topic}
RESEARCH FRAMEWORK:
${deconstruction.content}

Provide detailed findings with:
- Key facts and data
- Multiple perspectives
- Emerging trends or debates
- Historical context
- Practical implications

Be thorough and cite your reasoning.`;

    let gatheringResult;
    if (query.depth === 'exhaustive' || query.depth === 'deep') {
      // Use consensus mode for deep research
      gatheringResult = await modelRouter.generateConsensus(
        ['claude', 'perplexity', 'gemini'],
        gatheringPrompt,
        systemPrompt
      );
    } else {
      // Single model for quick research
      const singleResult = await modelRouter.generateSingle('claude', gatheringPrompt, systemPrompt);
      gatheringResult = { synthesis: singleResult.content, responses: [singleResult] };
    }

    // Phase 3: Synthesis into report
    const minWords = query.minWords || (query.depth === 'exhaustive' ? 10000 : query.depth === 'deep' ? 5000 : 2000);

    const synthesisPrompt = `
Create a comprehensive research report based on these findings:

${gatheringResult.synthesis}

REQUIREMENTS:
- Minimum ${minWords} words
- Academic prose style (no bullet points)
- Clear section structure with ## headers
- Inline citations where applicable
- Opening summary paragraph
- Minimum 5 main sections
- Conclusion with synthesis and recommendations

Write the complete report now:`;

    const report = await modelRouter.generateSingle('claude', synthesisPrompt, systemPrompt);

    // Extract sources (simplified - would be enhanced with actual web search)
    const sources = this.extractSourcesFromContent(report.content);

    // Generate follow-up questions
    const explorationPrompt = `
Based on this research report, generate 5 thought-provoking follow-up questions that would:
1. Deepen understanding
2. Challenge assumptions
3. Explore implications
4. Connect to related domains

Report excerpt: ${report.content.slice(0, 2000)}...

Provide 5 questions:`;

    const exploration = await modelRouter.generateSingle('claude', explorationPrompt);
    const relatedQueries = exploration.content.split('\n').filter(line => line.trim().length > 10).slice(0, 5);

    return {
      summary: report.content.slice(0, 500) + '...',
      sources,
      confidence: 0.85,
      relatedQueries,
      fullReport: report.content
    };
  }

  async quickResearch(topic: string): Promise<string> {
    const prompt = `
Provide a concise but comprehensive overview of: ${topic}

Include:
- Key facts and definitions
- Current state/status
- Major perspectives or debates
- Practical implications
- 3 questions for deeper exploration

Keep response focused but thorough (800-1200 words).`;

    const result = await modelRouter.smartRoute(prompt, 'research', personaEngine.getSystemPrompt('researcher'));
    return result.data as string;
  }

  async compareTopics(topics: string[]): Promise<string> {
    const prompt = `
Create a comprehensive comparison of the following topics:
${topics.map((t, i) => `${i + 1}. ${t}`).join('\n')}

Structure your comparison as:
1. Individual summaries of each topic
2. Key similarities
3. Critical differences
4. Comparative analysis table (as markdown)
5. Synthesis: How do these topics relate and inform each other?
6. Recommendations based on context

Be thorough and balanced in your analysis.`;

    const result = await modelRouter.generateSingle('claude', prompt, personaEngine.getSystemPrompt('researcher'));
    return result.content;
  }

  async factCheck(claim: string): Promise<{
    verdict: 'supported' | 'disputed' | 'unverified' | 'false';
    confidence: number;
    explanation: string;
    sources: string[];
  }> {
    const prompt = `
Analyze this claim for accuracy:

CLAIM: "${claim}"

Provide:
1. VERDICT: One of [SUPPORTED, DISPUTED, UNVERIFIED, FALSE]
2. CONFIDENCE: 0-100%
3. EXPLANATION: Detailed reasoning
4. EVIDENCE: Key supporting or contradicting points
5. CONTEXT: Important nuances or conditions
6. SOURCES: What types of sources would verify this

Be rigorous and balanced in your assessment.`;

    const result = await modelRouter.generateConsensus(['claude', 'perplexity'], prompt);

    // Parse the response (simplified parsing)
    const content = result.synthesis.toLowerCase();
    let verdict: 'supported' | 'disputed' | 'unverified' | 'false' = 'unverified';

    if (content.includes('supported') && !content.includes('not supported')) {
      verdict = 'supported';
    } else if (content.includes('false') || content.includes('incorrect')) {
      verdict = 'false';
    } else if (content.includes('disputed') || content.includes('debate')) {
      verdict = 'disputed';
    }

    return {
      verdict,
      confidence: 0.75,
      explanation: result.synthesis,
      sources: []
    };
  }

  async generateResearchPlan(topic: string, timeframe: string): Promise<string> {
    const prompt = `
Create a detailed research plan for investigating: ${topic}

Consider timeframe/scope: ${timeframe}

Include:
1. Research Questions (primary and secondary)
2. Methodology Approach
3. Source Types to Consult
4. Key Concepts and Keywords
5. Potential Challenges and Mitigations
6. Expected Deliverables
7. Quality Criteria for Sources
8. Synthesis Strategy

Provide actionable, structured plan.`;

    const result = await modelRouter.generateSingle('claude', prompt, personaEngine.getSystemPrompt('researcher'));
    return result.content;
  }

  private extractSourcesFromContent(content: string): SourceCitation[] {
    // Simplified source extraction - would be enhanced with actual citation parsing
    const citations: SourceCitation[] = [];

    // Look for markdown links
    const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
    let match;
    while ((match = linkRegex.exec(content)) !== null) {
      citations.push({
        title: match[1],
        url: match[2],
        relevance: 0.8
      });
    }

    // Look for numbered citations [1], [2], etc.
    const numberedRegex = /\[(\d+)\]/g;
    const numbers = new Set<number>();
    while ((match = numberedRegex.exec(content)) !== null) {
      numbers.add(parseInt(match[1]));
    }

    numbers.forEach(num => {
      if (!citations.some(c => c.title === `Source ${num}`)) {
        citations.push({
          title: `Source ${num}`,
          relevance: 0.7
        });
      }
    });

    return citations;
  }
}

export const researchEngine = new ResearchEngine();
