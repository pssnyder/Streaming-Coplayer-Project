## Project Overview: The AI Strategist & Banter-Box

The **Coplayer Strategist** is an interactive, voice-activated AI utility designed for deep tactical collaboration and immersive roleplay. While the *Peanut Gallery* observes and comments, the *Strategist* listens and engages. It serves as an evolving sandbox for learning AI call-and-response patterns, allowing you to move from simple "observation" to a dynamic, bidirectional "conversation" with a custom-defined persona.

---

### Core Functionality

* **Wake-Word Activation:** Custom trigger word support (e.g., *"Listen, Captain..."*) to initiate a user-to-AI prompt without manual hotkeys.
* **Voice-to-Voice Banter:** Integrated STT (Speech-to-Text) allows you to talk to the AI, which responds via your chosen TTS persona.
* **Deep Strategy Ingestion:** Simultaneously monitors game state (RAM, logs, or OCR) and your voice input to provide contextually aware advice.
* **Persona Hard-Lock:** Pre-prompted personality constraints ensure the AI never breaks character, whether it’s a rum-obsessed pirate or a cold, calculating military AI.

---

### Comparison: Part 1 vs. Part 2

| Feature | Part 1: Peanut Gallery | Part 2: Strategist (Stage 1) | Part 2: Strategist (Stage 2) |
| --- | --- | --- | --- |
| **Primary Input** | Video / Game Data | **User Text/Manual** | **User Voice** + Game Data |
| **Communication** | One-way (Commentary) | **Two-way (Q&A)** | **Two-way (Conversation)** |
| **Trigger** | Event-based | **Manual send** | **Wake-word based** |
| **Context Source** | Game visuals | **Game wikis** | **Wikis + Live game state** |
| **Complexity** | Observation | **Contextual Q&A** | **Strategic problem solving** |

---

### Technical Architecture (Stage 1)

1. **Input Handler:** Accepts text input or mic recording (manually submitted by user)
2. **Wiki Integration Layer:** Fetches relevant data from Pacific Drive wikis/APIs based on query keywords
3. **Context Assembly:** Bundles user question + wiki data + persona instructions into LLM prompt
4. **Persona-Locked Response:** LLM generates short, character-consistent answer (e.g., "That Anomaly Junction will fry your battery faster than a tourist at a lightning storm. Grab a junction bypass if you value your alternator.")
5. **TTS Vocalization:** Response is synthesized and played through speakers or virtual audio device
6. **Local-First Execution:** Runs as terminal application or simple desktop UI for testing and iteration

---

### Use Case: "The Mechanic's Assistant" (Pacific Drive)

**Persona**: A sarcastic but knowledgeable mechanic with gallows humor about the Zone

* **User Types/Says:** *"What's the deal with Electro-Anomalies?"*
* **AI (Mechanic Persona):** *"Oh, those sparkly bastards? They'll turn your car into a light show and your battery into toast. Slap on some rubber panels or just drive faster than physics allows. Your call, Speed Racer."*

* **User Types/Says:** *"I need to find junction boxes"*
* **AI:** *"Junction boxes, huh? Check abandoned garages in the Mid-Zone. And for the love of all that's electrical, don't open 'em bare-handed unless you enjoy spontaneous cardiac arrest."*

---

### Project Documentation

**Idea:** A progressive AI companion system that starts with wiki-enhanced text banter and evolves toward full voice interaction.

**Stage 1 Goal:** Build a robust text-based Q&A system with game wiki integration, persona consistency, and TTS output to establish the core interaction loop.

**Stage 2 Goal:** Layer in wake-word detection and STT for seamless voice-to-voice conversation.
**Benefit:** 
- **Learning Path**: Progress from simple API calls → advanced voice processing
- **Streaming Value**: Creates engaging "co-player" content without needing another human
- **Modular Design**: Each stage builds on the previous without throwing away work

**Priority:** High (Active Development - Stage 1 Implementation)

---

### Development Roadmap

**Stage 1 Tasks:**
- [ ] Set up Python project structure with GCP/Gemini integration
- [ ] Implement game wiki scraper/API client for Pacific Drive
- [ ] Build persona prompt templates with context injection
- [ ] Create text input handler (terminal or basic GUI)
- [ ] Integrate Google Cloud TTS for voice output
- [ ] Route audio to virtual device for OBS capture
- [ ] Test with multiple persona types (mechanic, scientist, AI core, etc.)

**Stage 2 Tasks (Future):**
- [ ] Integrate wake-word detection (Porcupine)
- [ ] Add Google Cloud STT for voice input
- [ ] Implement conversation memory/context tracking
- [ ] Layer in game state monitoring (OCR/memory reading)