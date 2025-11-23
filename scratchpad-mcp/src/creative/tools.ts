// Creative Writing Tools - Novel generation, storytelling, and creative content
// Implements the Novelize Protocol for high-quality fiction

import { modelRouter } from '../models/router.js';
import { personaEngine } from '../personas/engine.js';
import type { CreativeConfig } from '../types.js';

interface StoryContext {
  title?: string;
  genre?: string;
  setting?: string;
  characters?: CharacterProfile[];
  plotPoints?: string[];
  currentChapter?: number;
  previousSummary?: string;
  worldRules?: string[];
  themes?: string[];
}

interface CharacterProfile {
  name: string;
  role: string;
  traits: string[];
  backstory?: string;
  voice?: string;
  goals?: string[];
  currentState?: string;
}

interface SceneArchitecture {
  setting: string;
  time: string;
  atmosphere: string;
  characters: string[];
  objectives: string[];
  sensoryPalette: {
    sights: string[];
    sounds: string[];
    smells: string[];
    textures: string[];
  };
  emotionalBeats: string[];
  plotFunction: string;
}

export class CreativeEngine {
  private storyContexts: Map<string, StoryContext> = new Map();

  async generateChapter(
    storyId: string,
    chapterNumber: number,
    outline: string,
    config: CreativeConfig
  ): Promise<string> {
    const context = this.storyContexts.get(storyId) || {};
    const systemPrompt = personaEngine.getSystemPrompt('novelist');
    const targetWords = config.wordTarget || 8000;

    // Phase 1: Scene Architecture
    const architecturePrompt = `
You are planning Chapter ${chapterNumber} of a novel.

STORY CONTEXT:
${context.title ? `Title: ${context.title}` : ''}
${context.genre ? `Genre: ${context.genre}` : ''}
${context.setting ? `Setting: ${context.setting}` : ''}
${context.previousSummary ? `Previous Chapter Summary: ${context.previousSummary}` : ''}

CHAPTER OUTLINE:
${outline}

Create detailed SCENE ARCHITECTURE for this chapter:

1. SETTING DETAILS
   - Physical environment
   - Time of day/season
   - Atmosphere and mood

2. CHARACTER STATES
   - Who appears in this chapter
   - Their emotional state entering
   - Their goals and conflicts
   - Key relationships in play

3. PLOT MECHANICS
   - Story function of this chapter
   - Key events/revelations
   - Foreshadowing elements
   - Pacing structure (rising/falling action)

4. SENSORY PALETTE
   - Key visual details
   - Sound landscape
   - Smells and textures
   - Physical sensations

5. DIALOGUE INTENTIONS
   - Key conversations needed
   - Subtext in each
   - Voice distinctions

6. CHAPTER ARC
   - Opening hook
   - Mid-chapter turn
   - Closing hook for next chapter

Provide comprehensive scene planning:`;

    const architecture = await modelRouter.generateSingle('claude', architecturePrompt, systemPrompt);

    // Phase 2: Generate prose
    const prosePrompt = `
Write Chapter ${chapterNumber} based on this scene architecture:

${architecture.content}

WRITING REQUIREMENTS:
- Target: ${targetWords} words
- Show, don't tell - reveal character through action
- Rich sensory details grounded in physical reality
- Varied sentence rhythm and length
- Layer meaning through subtext
- Strong opening hook
- Compelling chapter ending
- Maintain consistent voice and tone

${context.characters?.length ? `
CHARACTER VOICES TO MAINTAIN:
${context.characters.map(c => `- ${c.name}: ${c.voice || c.traits.join(', ')}`).join('\n')}
` : ''}

Begin the chapter now. Write the full ${targetWords}+ words:`;

    const prose = await modelRouter.generateSingle('claude', prosePrompt, systemPrompt);

    // Update context
    context.currentChapter = chapterNumber;
    context.previousSummary = await this.summarizeChapter(prose.content);
    this.storyContexts.set(storyId, context);

    return prose.content;
  }

  async generateScene(
    description: string,
    characters: string[],
    mood: string,
    wordTarget: number = 2000
  ): Promise<string> {
    const systemPrompt = personaEngine.getSystemPrompt('novelist');

    const prompt = `
Write a vivid, immersive scene with the following parameters:

SCENE DESCRIPTION: ${description}
CHARACTERS PRESENT: ${characters.join(', ')}
MOOD/ATMOSPHERE: ${mood}
TARGET LENGTH: ${wordTarget} words

Requirements:
- Open with immediate sensory immersion
- Show character through action and dialogue
- Build tension or emotional resonance
- End with a moment of significance
- Use varied sentence structures
- Ground abstract emotions in physical details

Write the scene now:`;

    const result = await modelRouter.generateSingle('claude', prompt, systemPrompt);
    return result.content;
  }

  async generateDialogue(
    characters: CharacterProfile[],
    situation: string,
    subtext: string,
    length: 'short' | 'medium' | 'long' = 'medium'
  ): Promise<string> {
    const systemPrompt = personaEngine.getSystemPrompt('novelist');

    const characterDescriptions = characters.map(c =>
      `${c.name} (${c.role}): ${c.traits.join(', ')}. Voice: ${c.voice || 'distinctive'}`
    ).join('\n');

    const wordCounts = { short: 500, medium: 1500, long: 3000 };

    const prompt = `
Write a dialogue scene between these characters:

CHARACTERS:
${characterDescriptions}

SITUATION: ${situation}
UNDERLYING SUBTEXT: ${subtext}
TARGET LENGTH: ${wordCounts[length]} words

Requirements:
- Each character must have a distinctive voice
- Include action beats between dialogue
- Subtext should be felt but not stated
- Build tension or reveal character
- Use dialogue tags sparingly
- Show power dynamics through word choice

Write the dialogue scene:`;

    const result = await modelRouter.generateSingle('claude', prompt, systemPrompt);
    return result.content;
  }

  async developCharacter(
    name: string,
    role: string,
    initialTraits: string[]
  ): Promise<CharacterProfile> {
    const prompt = `
Develop a deep character profile for:

NAME: ${name}
ROLE IN STORY: ${role}
INITIAL TRAITS: ${initialTraits.join(', ')}

Create comprehensive profile including:

1. CORE IDENTITY
   - Defining traits (expand on initial)
   - Core values and beliefs
   - Greatest fear and deepest desire
   - Fatal flaw and greatest strength

2. BACKSTORY
   - Key formative experiences
   - Important relationships (past)
   - Secrets or hidden history
   - What shaped their worldview

3. VOICE AND MANNER
   - Speech patterns and vocabulary
   - Physical mannerisms
   - How they express emotion
   - Distinctive phrases or habits

4. GOALS AND CONFLICTS
   - External goals (plot-driven)
   - Internal goals (character arc)
   - What they want vs. what they need
   - Sources of internal conflict

5. RELATIONSHIPS
   - How they relate to others
   - Trust patterns
   - Communication style
   - Vulnerabilities in relationships

Provide detailed, usable character profile:`;

    const result = await modelRouter.generateSingle('claude', prompt, personaEngine.getSystemPrompt('novelist'));

    // Parse into structured profile
    return {
      name,
      role,
      traits: initialTraits,
      backstory: result.content,
      voice: `Character voice for ${name} - see full profile`,
      goals: []
    };
  }

  async buildWorld(
    genre: string,
    setting: string,
    scope: 'focused' | 'expansive' = 'focused'
  ): Promise<string> {
    const prompt = `
Create a world-building document for a ${genre} story set in ${setting}.

SCOPE: ${scope === 'expansive' ? 'Comprehensive world with deep history and systems' : 'Focused setting with essential details'}

Include:

1. PHYSICAL WORLD
   - Geography and key locations
   - Climate and environment
   - How setting affects daily life

2. SOCIETY AND CULTURE
   - Social structures and hierarchies
   - Customs and traditions
   - What people value and fear

3. RULES OF THE WORLD
   - What's possible and impossible
   - Unique elements (magic, technology, etc.)
   - Constraints that drive conflict

4. HISTORY
   - Key events that shaped the present
   - Conflicts (past and ongoing)
   - Legends or shared stories

5. ATMOSPHERE
   - Dominant moods and feelings
   - Sensory signature of this world
   - What makes it distinctive

6. STORY POTENTIAL
   - Built-in conflicts
   - Character archetypes that fit
   - Themes the world supports

Create immersive world document:`;

    const result = await modelRouter.generateSingle('claude', prompt, personaEngine.getSystemPrompt('novelist'));
    return result.content;
  }

  async generatePlotOutline(
    premise: string,
    genre: string,
    chapters: number = 20
  ): Promise<string> {
    const prompt = `
Create a detailed plot outline for a ${genre} novel:

PREMISE: ${premise}
TARGET CHAPTERS: ${chapters}

Structure the outline with:

1. HOOK (Chapter 1-2)
   - Opening scene/situation
   - Inciting incident
   - Stakes establishment

2. RISING ACTION (Chapters 3-${Math.floor(chapters * 0.4)})
   - Key plot points
   - Character development beats
   - Escalating challenges

3. MIDPOINT (Chapter ${Math.floor(chapters * 0.5)})
   - Major revelation or shift
   - Point of no return

4. COMPLICATIONS (Chapters ${Math.floor(chapters * 0.5) + 1}-${Math.floor(chapters * 0.75)})
   - Increasing obstacles
   - Character tests
   - Subplot convergence

5. CLIMAX (Chapters ${Math.floor(chapters * 0.75) + 1}-${Math.floor(chapters * 0.9)})
   - Final confrontation
   - Peak tension

6. RESOLUTION (Final chapters)
   - Aftermath
   - Character transformation shown
   - Thematic resonance

For each chapter, provide:
- Chapter title
- Key events (2-3 sentences)
- Character focus
- Emotional arc

Create the complete outline:`;

    const result = await modelRouter.generateSingle('claude', prompt, personaEngine.getSystemPrompt('novelist'));
    return result.content;
  }

  async styleTransfer(
    text: string,
    targetStyle: string
  ): Promise<string> {
    const prompt = `
Rewrite the following text in the style of ${targetStyle}:

ORIGINAL TEXT:
${text}

Maintain the core meaning and plot points while transforming:
- Sentence structure and rhythm
- Word choice and vocabulary
- Narrative voice and tone
- Descriptive approach

Rewritten version:`;

    const result = await modelRouter.generateSingle('claude', prompt, personaEngine.getSystemPrompt('novelist'));
    return result.content;
  }

  private async summarizeChapter(content: string): Promise<string> {
    const prompt = `
Summarize this chapter in 2-3 paragraphs, capturing:
- Key plot events
- Character developments
- Emotional beats
- Setup for future chapters

Chapter content:
${content.slice(0, 10000)}...

Provide summary:`;

    const result = await modelRouter.generateSingle('claude', prompt);
    return result.content;
  }

  initializeStory(storyId: string, context: StoryContext): void {
    this.storyContexts.set(storyId, context);
  }

  getStoryContext(storyId: string): StoryContext | undefined {
    return this.storyContexts.get(storyId);
  }
}

export const creativeEngine = new CreativeEngine();
