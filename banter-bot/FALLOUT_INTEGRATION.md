# Banter Bot + Mantella Integration Guide

## 🎮 The Setup

You're creating a **dual AI personality system** for Fallout 4:

1. **Mantella** → NPC dialogue (characters in the game world)
2. **Banter Bot** → Internal monologue (your character's thoughts/voice in your head)

This creates an immersive experience where:
- NPCs respond to you with AI-generated dialogue
- Your "inner voice" (Gary, Hype, Coach) comments on everything
- Both systems hear you speak naturally while gaming

---

## 🎤 Open Mic Mode

### How It Works:

1. **Voice Activity Detection (VAD)**
   - Banter Bot listens continuously via your mic
   - Detects when you're speaking vs. silence
   - Only processes speech above energy threshold (ignores game audio bleed)

2. **Trigger Modes:**
   - **Trigger Mode**: Say "Gary" to start conversation, then chat naturally
   - **Commentary Mode**: AI comments on ANYTHING you say (be warned: very chatty!)

3. **Smart Response Logic:**
   ```
   You: "What the hell was that?!"
   Gary: "That would be a Deathclaw. Probably should've looked before you walked in here."
   
   [Conversation active - no trigger needed]
   You: "I need more ammo"
   Gary: "Yeah, might wanna stop missing so much. Just a thought."
   ```

---

## ⚙️ Configuration for Gaming

### Adjust VAD Sensitivity (`.env`):

```env
# Higher threshold = less sensitive (good for noisy game audio)
VAD_ENERGY_THRESHOLD=800

# How long to wait after you stop talking
VAD_SILENCE_DURATION=2.0

# Ignore very short utterances (grunts, sighs)
VAD_MIN_SPEECH_DURATION=0.5
```

### Recommended Personas for Fallout 4:

**Gary (Sarcastic Survivor)**
- Comments on your bad decisions
- Roasts your combat skills
- Dark humor about the wasteland

**Lone Wanderer (Internal Monologue)**
- Create a custom persona that sounds like your character's thoughts
- Survival-focused, pragmatic
- References Fallout lore

**VATS (AI Companion)**
- Technical, analytical
- Comments on stats and probabilities
- Like having Codsworth in your head

---

## 🔊 Audio Routing for Streaming

### Option 1: Simple (Hear Everything)
- Banter Bot → Default speakers
- Game audio → Default speakers
- Stream hears both

### Option 2: Advanced (Separate Channels)
1. Install **VB-Audio Virtual Cable**
2. Route Banter Bot TTS → Virtual Cable
3. Route Virtual Cable → OBS as separate audio source
4. Mix in OBS for perfect balance

This lets you:
- Control AI volume independently
- Mute AI without affecting game
- Apply different audio effects

---

## 🎯 Integration Points with Mantella

### Current State:
- Banter Bot = standalone voice assistant
- Mantella = NPC dialogue system

### Future Enhancements:

1. **Shared Context**
   - Pass current quest/location to Banter Bot
   - AI comments are contextually aware
   - "Oh great, back to Diamond City. Your favorite place."

2. **Dialogue Awareness**
   - Banter Bot can "hear" NPC responses
   - Comments AFTER NPC speaks
   - "Did that settler just ask YOU for help? The irony."

3. **Game State Hooks**
   - Read Fallout 4 memory for health, location, inventory
   - "You're at 20% health and still running toward gunfire. Bold strategy."

---

## 🚀 Launch Sequence

### 1. Start Ollama (if not running)
```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" serve
```

### 2. Launch Banter Bot
```powershell
cd "S:\Programming\Gaming Projects\Streaming Coplayer Project\banter-bot"
.\venv\Scripts\Activate.ps1
python src/gui_app.py
```

### 3. Configure Settings
- Select persona (Gary for sarcasm)
- Enable **🎤 Voice Mode** (checkbox)
- Choose Commentary Mode on/off
- Start Fallout 4

### 4. Test It
- Speak: "Gary, I'm heading into Sanctuary"
- Listen for response
- Continue playing - AI will respond when triggered

---

## 🎮 Fallout 4 Specific Tips

### Good Test Phrases:
- "Gary, should I side with the Brotherhood?"
- "This raider has way too much health"
- "Where's the damn door"
- "I'm definitely going to die here"

### What Works Well:
- ✅ Combat commentary ("Nice shot!" "You missed.")
- ✅ Exploration ("Been here before")
- ✅ Decision making ("That seems like a bad idea")
- ✅ Loot reactions ("Ooh, legendary!")

### What to Avoid:
- ❌ Asking about specific quest details (AI doesn't have game state yet)
- ❌ Expecting AI to remember previous sessions (no persistence yet)

---

## 🛠️ Troubleshooting

### "No response when I speak"
- Check Voice Mode is ON (checkbox checked)
- Verify mic permissions
- Adjust `VAD_ENERGY_THRESHOLD` lower

### "AI responds to game audio"
- Increase `VAD_ENERGY_THRESHOLD` to 1000+
- Use push-to-talk mode (hold key to trigger)
- Position mic closer to you, farther from speakers

### "Responses are slow"
- Use smaller Ollama model: `llama3.2:1b`
- Check Ollama is running: `ollama list`

### "AI is TOO chatty"
- Disable Commentary Mode
- Only use trigger word ("Gary") when you want response

---

## 🎭 Creating Custom Personas for Fallout

Edit `config/personas/yourpersona.json`:

```json
{
  "name": "Lone Wanderer",
  "trigger_name": "Hey",
  "personality": {
    "description": "The hardened internal voice of a Vault Dweller surviving the wasteland. Pragmatic, cynical, but with a dark sense of humor.",
    "tone": "gritty, survival-focused, wasteland slang",
    "response_style": "short observations, gallows humor, occasional wisdom"
  },
  "directives": [
    "Keep responses to 1-2 sentences",
    "Use Fallout universe terminology when relevant",
    "Comment on survival situations",
    "Reference radiation, caps, stimpaks naturally",
    "Never break immersion - you ARE the character's thoughts"
  ]
}
```

---

**Ready to give your Sole Survivor a voice? Fire it up!** 🎮🎤
