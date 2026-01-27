# Getting Started - Quick Setup

## Step 1: Install Dependencies (1 minute)

```powershell
cd "s:\Programming\Gaming Projects\Streaming Coplayer Project\banter-bot"
pip install -r requirements.txt
```

**Note:** If you get PyAudio errors, don't worry! For text-only testing, you don't need it yet.

---

## Step 2: Get Gemini API Key (2 minutes)

1. Open: https://aistudio.google.com/app/apikey
2. Click "Create API Key" 
3. Copy the key (starts with `AIza...`)

---

## Step 3: Configure Environment (1 minute)

```powershell
# Copy the example file
Copy-Item .env.example .env

# Open .env in VS Code
code .env
```

Add your Gemini API key:
```env
GEMINI_API_KEY=AIzaSy...your_actual_key_here
```

**For text-only testing, that's all you need!** (TTS/STT setup can wait)

---

## Step 4: Quick Test (30 seconds)

Test the core functionality without audio:

```powershell
python quick_test.py
```

This will:
- ✓ Verify your Gemini API key works
- ✓ Test Gary persona responses  
- ✓ Simulate gaming commentary scenarios
- ✓ Show conversation context tracking

---

## Step 5: Interactive Text Mode

Once quick test passes, run the full app:

```powershell
python src/main.py
```

1. Select persona: **1** (Gary)
2. Commentary mode: **N** (no - use trigger only)
3. Voice input: **N** (no - text mode)

Then try these test phrases:

```
Gary, that jump scare got me so bad
I need to heal like right now
The game is broken, not me
```

Type `quit` to exit.

---

## Troubleshooting

### "GEMINI_API_KEY not found"
- Make sure `.env` file exists (not `.env.example`)
- Check there's no space around the `=` sign
- Verify the key is pasted correctly

### "ModuleNotFoundError: google.generativeai"
```powershell
pip install google-generativeai
```

### PyAudio installation fails
- **For text mode**: Ignore it! You don't need audio yet
- **For voice mode later**: We'll install it separately

### "No personas found"
- Make sure you're running from the `banter-bot` folder
- Check that `config/personas/gary.json` exists

---

## Next Steps After Text Testing Works

1. ✅ **Test text mode thoroughly** - Try different scenarios
2. 📝 **Create custom personas** - Copy gary.json and customize
3. 🔊 **Set up GCP for TTS** (optional) - For voice responses
4. 🎤 **Add voice input** (optional) - For hands-free operation

---

## GCP Setup (For Voice Features)

Only needed if you want TTS/STT later:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select project: `rts-labs-f3981`
3. Enable APIs:
   - Cloud Text-to-Speech API
   - Cloud Speech-to-Text API
4. Create service account key:
   - IAM & Admin → Service Accounts
   - Create Service Account
   - Grant roles: "Cloud Speech Client", "Cloud Text-to-Speech Client"  
   - Keys → Add Key → JSON
   - Download the JSON file

5. Update `.env`:
```env
GCP_PROJECT_ID=rts-labs-f3981
GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\service-account-key.json
```

---

## Test Phrases Reference

See [test_phrases.md](test_phrases.md) for a full list of gaming scenarios to test with!

**Example conversation:**
```
> Gary, that jump scare got me so bad
Gary: Oh yeah, I'm sure that was totally unexpected in the horror game. Who could've seen that coming?

> I need to heal like right now
Gary: Maybe if you paid attention to your health bar instead of walking into every trap, you wouldn't be in this mess.

> The game is broken, not me  
Gary: Sure, blame the game. That's definitely what happened here.
```

---

**Ready? Run `python quick_test.py` to get started!**
