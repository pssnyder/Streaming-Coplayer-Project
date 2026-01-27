# Banter Bot - Setup Guide

## 🚀 Quick Start

### 1. Install Dependencies

```powershell
cd "s:\Programming\Gaming Projects\Streaming Coplayer Project\banter-bot"
pip install -r requirements.txt
```

### 2. Get Your API Keys

#### Google Gemini API Key (Required)
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Get API Key" or "Create API Key"
3. Copy the key

#### Google Cloud Setup (Required for TTS/STT)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select project: `rts-labs-f3981`
3. Enable these APIs:
   - Cloud Text-to-Speech API
   - Cloud Speech-to-Text API
4. Create a service account:
   - IAM & Admin → Service Accounts → Create Service Account
   - Grant roles: "Cloud Speech Client", "Cloud Text-to-Speech Client"
   - Create JSON key and download it

### 3. Configure Environment

Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```

Edit `.env` and add your keys:
```env
GEMINI_API_KEY=your_actual_gemini_key_here
GCP_PROJECT_ID=rts-labs-f3981
GOOGLE_APPLICATION_CREDENTIALS=path\to\your\service-account-key.json
```

### 4. Run the Bot

```powershell
python src/main.py
```

---

## 🎮 Usage

### Text Mode (Recommended for Testing)
1. Select a persona (Gary, Hype, Coach)
2. Choose settings (commentary mode on/off)
3. Type messages in the terminal
4. Use trigger name to start conversations

**Example Session:**
```
> Hey Gary, I just took a ton of damage!
Gary: Yeah I don't know why you'd try that, maybe next time just chill.

> We have no chill here bro
Gary: Alright, suit yourself. Who needs health, right?

> Now you're just being negative
Gary: Yeah, just like your health is about to be.
```

### Voice Mode
- Same as text mode, but speak instead of type
- STT transcribes your speech in real-time
- Interim results shown as you speak

---

## ⚙️ Features

### Trigger Mode (Default)
- AI only responds when you say its trigger name
- Example: "Hey **Gary**, that was close!"
- Conversation stays active for 5 minutes after last interaction
- Follow-up responses don't need trigger name

### Commentary Mode
- AI responds to ANY statement you make
- Use for constant banter and reactions
- Great for filling stream dead air
- Example: "Oops that hurt" → AI responds even without trigger

---

## 🎭 Personas

### Gary (Sarcastic Sidekick)
- **Trigger:** "Gary"
- **Style:** Witty, sarcastic, roasts your mistakes
- **Best For:** Comedy streams, lighthearted banter

### Hype (Enthusiasm Bot)
- **Trigger:** "Hype"
- **Style:** Overly enthusiastic, positive about everything
- **Best For:** High-energy content, motivation

### Coach (Supportive Mentor)
- **Trigger:** "Coach"
- **Style:** Honest but supportive, practical advice
- **Best For:** Learning streams, practice sessions

---

## 🛠️ Customization

### Create Your Own Persona

1. Copy an existing persona file:
```powershell
Copy-Item config/personas/gary.json config/personas/yourname.json
```

2. Edit the JSON:
```json
{
  "name": "Your Bot Name",
  "trigger_name": "YourTrigger",
  "personality": {
    "description": "Your personality description...",
    "tone": "your tone style",
    "response_style": "how it responds"
  },
  "directives": [
    "Keep responses to 1-2 sentences",
    "Your specific rules..."
  ]
}
```

3. Restart the bot and select your new persona!

---

## 🎤 Audio Setup

### For OBS Streaming

1. Install [VB-Audio Virtual Cable](https://vb-audio.com/Cable/)
2. Set Banter Bot to output to virtual cable
3. Add virtual cable as audio source in OBS
4. Your stream hears the AI, but you hear it through monitors

### Voice Configuration

Edit `src/tts_client.py` to change voices:
```python
# Available voices:
# en-US-Neural2-A (female)
# en-US-Neural2-C (female)  
# en-US-Neural2-D (male)
# en-US-Neural2-J (male) # Current default
```

---

## 🐛 Troubleshooting

### "GEMINI_API_KEY not found"
- Make sure `.env` file exists (copy from `.env.example`)
- Check that the key is correctly pasted

### "Audio recording error"
- Check microphone permissions
- Ensure PyAudio is installed: `pip install pyaudio`
- On Windows, may need to install [PortAudio](http://www.portaudio.com/)

### "TTS test failed"
- Verify `GOOGLE_APPLICATION_CREDENTIALS` path is correct
- Make sure service account has TTS permissions
- Check that Cloud Text-to-Speech API is enabled

### No audio output
- Check default audio device
- Verify `pydub` and audio backend installed
- Windows: `pip install pydub`
- May need ffmpeg: `choco install ffmpeg`

---

## 📊 Free Tier Limits

### Google Gemini
- 1,500 requests per day (free tier)
- Rate limit: 15 requests per minute

### Google Cloud TTS
- 1 million characters per month (free)
- ~16,000 responses at 60 chars each

### Google Cloud STT  
- 60 minutes per month (free)
- Enough for ~30 hours if used efficiently

---

## 🎯 Next Steps

1. **Test with text mode first** - Get comfortable with the flow
2. **Try different personas** - See which style you like
3. **Enable voice input** - More natural for streaming
4. **Create custom personas** - Match your stream's vibe
5. **Integrate with OBS** - Route audio for your viewers

---

## 💡 Tips

- **Keep responses short**: Personas are configured for 1-2 sentence responses
- **Use commentary mode sparingly**: Can get chatty quickly
- **Adjust conversation timeout**: Edit `.env` if 5 minutes is too short/long
- **Test voice triggers**: Make sure your mic picks up the trigger name clearly
- **Combine with game audio**: Set volume so AI doesn't overpower gameplay

Happy streaming! 🎮🎤
