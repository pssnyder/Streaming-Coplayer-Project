# Project Overview: The AI Peanut Gallery (Part 1)

**The Foundation of the Streamer Coplayer AI Suite**

The **Peanut Gallery AI** is an automated, personality-driven commentary layer. It serves as the "eyes" of your AI companion, providing real-time observations of your gameplay. This project is designed as the **Level 1 Implementation**, focusing on one-way AI callouts to establish the core pipeline: *Ingestion -> Analysis -> Vocalization.*

---

### 🔄 The Coplayer Ecosystem

This utility is designed to work in tandem with the **Part 2: Strategist Utility**.

* **Peanut Gallery:** Handles the *Passive* stream (The AI watches you).
* **Strategist:** Handles the *Active* stream (The AI listens to you).

---

### Updated Key Features

* **Unsolicited Commentary:** Triggered by visual or data cues (e.g., a "Game Over" screen or a health drop) without needing user input.
* **Persona Synchronization:** Shared configuration files allow the Peanut Gallery and the Strategist to share the same "soul"—ensuring the voice that roasts you is the same voice you later ask for strategy.
* **Modular Ingestion Engine:** Supports screen-scraping (OCR) and game-state data feeds, providing the foundational context for the entire AI suite.

---

### Updated Technical Workflow

1. **Passive Monitoring:** Continuously scrapes the screen or monitors log files for "Hook Events" (kills, deaths, loot).
2. **Context Injection:** Feeds the event to the LLM (e.g., "The player just missed a headshot").
3. **Vocalized Reaction:** The AI reacts immediately to the broadcast, filling "dead air" for the streamer.

---

### Project Roadmap Integration

**Idea:** A passive observation bot that provides unsolicited live commentary based on visual and data-driven gaming events.
**Goal:** Establish the baseline "Reaction Engine" and TTS pipeline that will eventually support the voice-interactive Strategist.
**Benefit:** Eliminates "dead air" during streams and provides an immediate learning playground for computer vision and LLM prompt-tuning.
**Tasks:**

* [ ] Implement screen-capture / OCR hook for specific game events.
* [ ] Setup basic LLM prompt templates for the "Roast" and "Hype" personas.
* [ ] Route TTS audio to a virtual output for OBS testing.
**Priority:** Need to Have (The foundation for all future modules).

---

### ⚠️ A Note on Workflow

> Since we are building this as a progression, this module’s configuration should be kept **minimalist and modular** so it can easily feed its data "upstairs" to the Strategist module later.

---

Would you like me to draft a **Tasks** list specifically for setting up the "Hook Events" (the triggers that tell the AI when to speak) for a specific game you're playing?