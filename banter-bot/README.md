## Project Overview: The Banter Bot

**The Simplest AI Companion - Pure Conversational Entertainment**

The **Banter Bot** is a mic-triggered, personality-driven conversational AI designed to fill dead air during streams and provide social comfort for solo gamers. Unlike the other utilities in this suite, the Banter Bot has no game context, no strategic purpose, and no visual monitoring—it's purely about conversation and entertainment.

**Purpose**: 
- Fill awkward silences during single-player streams
- Provide a "companion voice" for solo gaming sessions
- Serve as a social comfort tool to practice streaming commentary
- Break through stage fright and conversational anxiety
- Create entertaining content through AI personality interactions

---

### 🎯 Core Concept

This is the **foundation learning project** for the entire AI suite—establishing the basic pipeline before adding complexity:

**User speaks/types → AI responds with personality → TTS output**

No wikis. No game data. No computer vision. Just pure conversational AI with a locked persona.

---

### Key Features

* **Pre-Promptable Personalities:** Define custom personas (comedian, philosopher, sports commentator, dungeon master, etc.) before starting
* **Mic-Triggered Input:** Speak into mic with manual send, or type for testing (no wake-word complexity yet)
* **Personality Hard-Lock:** AI maintains character consistency throughout the conversation
* **Topic Flexibility:** Can discuss anything - not limited to game content
* **TTS Vocalization:** Immediate audio response for streaming integration
* **Conversation Memory:** Maintains context across multiple exchanges in a session
* **Zero External Dependencies:** No game data, no wikis, no screen capture—just LLM + TTS

---

### Use Cases

#### **The Streaming Companion**
You're playing a single-player game with minimal dialogue. Instead of dead air:
- **You:** "Man, this puzzle is frustrating."
- **Bot (Comedian Persona):** "Frustrating? Buddy, I've seen toddlers solve Rubik's cubes faster than you're solving this 'rotate the statue' challenge. Maybe try turning it the OTHER direction?"

#### **The Social Warmup**
New to streaming and camera-shy:
- **You:** "I don't know what to say on stream."
- **Bot (Supportive Coach):** "Start simple. Tell them what you're doing and why. Even if it's just 'I'm grabbing this potion because I'm basically made of tissue paper right now.' They're here for YOU, not a perfect performance."

#### **The Character Roleplay**
You're playing D&D solo or a story-driven RPG:
- **You:** "Should I trust this NPC?"
- **Bot (Dungeon Master):** "The merchant's smile doesn't reach his eyes, and you notice his hand resting a bit too casually near a dagger. Trust is earned, adventurer, not given to every smooth-talker in a tavern."

---

### Technical Architecture

```
┌─────────────────┐
│  User Input     │  (Mic recording or text)
│  (Manual Send)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Persona Prompt  │  (Pre-loaded personality instructions)
│   + User Text   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LLM (Gemini)   │  (Generates in-character response)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ TTS (GCP/Eleven)│  (Synthesizes audio)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Audio Output    │  (Speakers or virtual audio device)
└─────────────────┘
```

---

### Persona Examples

**1. The Sarcastic Sidekick**
> "Oh great, another 10-minute cutscene you can't skip. I'll just sit here and contemplate the meaning of existence. Or take a nap. Whichever comes first."

**2. The Overly Enthusiastic Hype Person**
> "YES! You opened a DOOR! That's what I'm talking about! Door-opening EXCELLENCE! What's next, champion? A HALLWAY?! This is PEAK gaming!"

**3. The Noir Detective**
> "The room was dark. Too dark. Like the secrets this game's hiding from you. You opened the chest—inside, a rusty sword. Not much, but in this business, you take what you can get."

**4. The Dad-Joke Bot**
> "Why did the gamer cross the road? Because the quest marker was on the other side! ...I'll see myself out."

---

### Development Roadmap

**MVP Tasks (This Week):**
- [ ] Set up Python project structure
- [ ] Configure Google Cloud/Gemini API access
- [ ] Build persona template system (JSON or YAML configs)
- [ ] Create terminal-based input handler
- [ ] Integrate Gemini API for text generation
- [ ] Add Google Cloud TTS for voice synthesis
- [ ] Implement basic conversation memory (last 5-10 exchanges)
- [ ] Test with 3 different persona types

**Phase 2 (Next Week):**
- [ ] Add mic recording + STT (manual trigger, no wake-word)
- [ ] Create simple GUI (input box, send button, response display)
- [ ] Route audio to virtual device for OBS capture
- [ ] Add persona switching mid-conversation
- [ ] Implement conversation export/logging

**Phase 3 (Future):**
- [ ] Wake-word detection for hands-free triggering
- [ ] Multi-persona conversations (bot argues with itself)
- [ ] Twitch chat integration (bot responds to chat messages)
- [ ] Advanced memory (RAG for long-term context)

---

### Comparison to Other Utilities

| Feature | Banter Bot | Peanut Gallery | Game Strategist |
| --- | --- | --- | --- |
| **Input** | User voice/text | Screen capture | User query + Wiki |
| **Context** | Conversation history | Visual game events | Game mechanics data |
| **Output** | General banter | Event commentary | Strategic advice |
| **Complexity** | Lowest | Medium | Medium-High |
| **Purpose** | Entertainment | Stream filler | Tactical guidance |
| **Learning Focus** | LLM + TTS basics | CV + Event detection | API integration + Prompting |

---

### Why Start Here?

1. **Simplest Pipeline**: Master the core LLM→TTS flow without external data complexity
2. **Immediate Value**: Get a working "companion" in hours, not days
3. **Transferable Skills**: Every lesson here applies to the other two utilities
4. **Low Barrier**: No game-specific knowledge needed, no OCR tuning, no wiki parsing
5. **Fun Factor**: Hearing an AI roast you in real-time is instant gratification

---

### Project Status

**Current Phase**: Initial Setup & MVP Development  
**Target Completion**: 1 week for text-based MVP  
**Next Milestone**: Terminal-based banter bot with 3 working personas
