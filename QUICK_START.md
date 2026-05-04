# 🚀 M8 AI Assistant - Quick Start Guide

## **ONE MINUTE SETUP**

### 1️⃣ Install Dependencies
```bash
pip install -r Frontend/requirements.txt
```

### 2️⃣ Verify .env File
Make sure your project root has `.env` with:
```
GroqAPIKey=your_api_key_here
Username=You
Assistantname=M8
```

### 3️⃣ Run the App
```bash
streamlit run Frontend/app.py
```

✅ **Done!** App opens at `http://localhost:8501`

---

## **WHAT YOU GET**

### 🎯 Features
- ✨ **Modern Dark UI** - Black, silver, white theme
- 🔮 **Glowing Orb** - Animated visual element
- 💬 **Chat Interface** - Beautiful message bubbles
- 🎤 **Voice Mode** - Toggle microphone (UI ready)
- 📊 **Chat History** - Persists during session
- ⚡ **Smooth Animations** - Slide-in effects
- 🔔 **Status Indicators** - Real-time feedback

### 🎨 Design Highlights
- Centered, minimal layout
- Futuristic aesthetic
- Smooth spacing
- Rounded elements
- Responsive design

---

## **HOW TO USE**

### 💬 Chat Mode (Default)
1. Type your message in the input box
2. Press Enter or click Send
3. Wait for AI response
4. See conversation grow

### 🎤 Voice Mode
1. Click "🎤 Voice Mode" button
2. Click microphone icon to toggle listening
3. Speak your question
4. See "🎤 LISTENING" indicator
5. Response appears automatically

---

## **FILE GUIDE**

| File | Purpose |
|------|---------|
| `Frontend/app.py` | Main Streamlit app |
| `Frontend/voice_utils.py` | Voice integration helpers |
| `Frontend/requirements.txt` | Python dependencies |
| `Frontend/CUSTOMIZATION_GUIDE.md` | Theme & styling options |
| `README_STREAMLIT.md` | Full documentation |

---

## **CUSTOMIZATION QUICK LINKS**

### Colors 🎨
Edit line ~68 in `app.py` under `<style>`:
- Blue bubbles: Search `#1e40af`
- Gray bubbles: Search `#1f2937`
- Glow effect: Search `#60a5fa`

### Animations ⚡
Edit animations in `<style>`:
- Speed: Change `0.3s` or `1.5s` values
- Direction: Modify `slideInLeft` or `slideInRight`

### Size 📐
- Orb size: Edit `.orb` class width/height
- Chat height: Edit `.chat-container` max-height
- Message width: Edit `.user-message` max-width

See `CUSTOMIZATION_GUIDE.md` for complete reference.

---

## **TROUBLESHOOTING**

### ❌ "GroqAPIKey not found"
→ Create/update `.env` file with valid API key

### ❌ "Module not found: Chatbot"
→ Run from project root: `streamlit run Frontend/app.py`

### ❌ App not responding
→ Check terminal for errors: Look at console output

### ❌ Chat not working
→ Test backend: `python Backend/Chatbot.py`

---

## **COMMON COMMANDS**

| Command | Purpose |
|---------|---------|
| `streamlit run Frontend/app.py` | Start app |
| `streamlit run Frontend/app.py --logger.level=debug` | Debug mode |
| `pip install -r Frontend/requirements.txt` | Install deps |
| `python Frontend/voice_utils.py` | Test voice setup |

---

## **KEYBOARD SHORTCUTS (In Streamlit)**

| Key | Action |
|-----|--------|
| `Control+C` | Stop server |
| `F` | Fullscreen mode |
| `R` | Rerun script |
| `S` | Save screenshot |

---

## **NEXT STEPS**

### ✅ Immediate
1. 🎯 Run the app
2. 💬 Try chatting
3. 🎤 Explore voice mode UI

### 🔄 Short Term
1. Customize colors in `CUSTOMIZATION_GUIDE.md`
2. Adjust animations to your taste
3. Modify status messages

### 🚀 Future
1. Implement voice input (see `voice_utils.py`)
2. Add chat export feature
3. Create custom themes
4. Add user preferences

---

## **TIPS & TRICKS**

💡 **Pro Tips:**
- Streamlit auto-reloads on file save
- Session state resets on page refresh
- Chat history saved in `Data/ChatLog.json`
- Add print() statements for debugging
- Edit CSS live without restarting app

🎯 **Best Practices:**
- Keep backend functions in `Backend/`
- All UI in `Frontend/app.py` only
- Use session state for temp data
- Document custom functions

---

## **FILE STRUCTURE**
```
M8/
├── Frontend/
│   ├── app.py                    ← Main app (RUN THIS)
│   ├── voice_utils.py            ← Voice helpers
│   ├── requirements.txt          ← Dependencies
│   ├── CUSTOMIZATION_GUIDE.md    ← Styling options
│   ├── Files/                    ← User uploads
│   └── Frontend/                 ← Assets (if needed)
├── Backend/
│   ├── Chatbot.py               ← AI logic
│   └── ...
├── Data/
│   └── ChatLog.json             ← Conversations
└── .env                         ← API keys
```

---

## **SUPPORT**

📖 **Documentation:**
- `README_STREAMLIT.md` - Full features & setup
- `CUSTOMIZATION_GUIDE.md` - Theme & colors
- Inline comments in `app.py` - Code documentation

🔧 **Help:**
- Check terminal output for errors
- Review backend `Chatbot.py` for logic issues
- Test voice setup: `python Frontend/voice_utils.py`

---

## **QUICK REFERENCE**

**Install:** `pip install -r Frontend/requirements.txt`  
**Run:** `streamlit run Frontend/app.py`  
**Customize:** Edit CSS in `Frontend/app.py` (lines 29-111)  
**Deploy:** See Streamlit cloud deployment docs

---

**Ready to use M8? Run `streamlit run Frontend/app.py` now!** 🚀
