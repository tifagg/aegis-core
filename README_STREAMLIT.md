# M8 AI Assistant - Streamlit Web App

A clean, modern AI assistant web application built with Streamlit. Features a dark theme, real-time chat, and voice mode capabilities.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Streamlit installed (`pip install streamlit`)
- All backend dependencies installed (see main project requirements)

### Installation

1. **Install Streamlit** (if not already installed):
   ```bash
   pip install streamlit
   ```

2. **Ensure all backend dependencies are installed**:
   ```bash
   pip install groq python-dotenv
   ```

3. **Verify `.env` file** exists in the project root with:
   ```
   GroqAPIKey=your_api_key_here
   Username=Your_Username
   Assistantname=M8
   ```

### Running the App

Navigate to the project directory and run:

```bash
streamlit run Frontend/app.py
```

The app will open in your default browser at `http://localhost:8501`

---

## 🎯 Features

### UI/Design
- **Dark Theme**: Black, silver, and white color scheme
- **Glowing Orb**: Animated visual element that pulses when listening
- **Centered Layout**: Minimal, futuristic design
- **Smooth Animations**: Slide-in effects for messages, pulse patterns
- **Modern Typography**: Clean, readable fonts with proper spacing

### Core Functionality
- **Chat Interface**: Send and receive messages with beautiful chat bubbles
- **Voice Mode**: Toggle microphone on/off (ready for integration)
- **Mode Switching**: Toggle between Chat and Voice modes
- **Chat History**: Persistent chat maintained during session
- **Status Indicators**: Visual feedback for listening/ready states
- **Loading State**: "Thinking..." indicator while processing

### Backend Integration
- **ChatBot Function**: Connects to `Backend.Chatbot.ChatBot()` function
- **Groq API**: Uses Groq's OpenAI-compatible API for responses
- **Chat Logging**: Automatic conversation logging in `Data/ChatLog.json`
- **Context Awareness**: Real-time datetime context in responses

---

## 🎨 Customization

### Change Theme Colors
Edit the CSS in `Frontend/app.py` - look for the `<style>` section:
- **Primary Blue**: `#1e40af` → Change for user message color
- **Dark Gray**: `#1f2937` → Change for assistant message color
- **Accent Blue**: `#60a5fa` → Change for accents/glow effects

### Modify Orb Size
In the `.orb` CSS class, change:
```css
width: 120px;    /* Change this */
height: 120px;   /* And this */
```

### Adjust Animation Speed
Modify animation durations in the CSS, e.g.:
```css
animation: glow 1.5s ease-in-out infinite;  /* Change 1.5s for faster/slower */
```

---

## 📱 Voice Mode (Future Enhancement)

Currently, the voice mode toggle is available and shows listening status. To implement voice input:

1. Install `SpeechRecognition`: `pip install SpeechRecognition pyaudio`
2. Use backend's `SpeechToText()` function for voice input processing
3. Modify the voice toggle button to capture audio and transcribe

Example integration would be in the voice mode section of `app.py`.

---

## 🔧 Architecture

### Frontend (`Frontend/app.py`)
- **Pure Streamlit UI** - No business logic, only display
- **Session State Management** - Chat history, mode switching
- **Helper Functions** - Message rendering, status badges
- **Custom CSS** - All styling in one place for easy modification

### Backend (`Backend/Chatbot.py`)
- **ChatBot Function** - Single entry point for AI responses
- **Groq Integration** - API calls for LLM
- **Chat Logging** - Automatic conversation history
- **Error Handling** - Graceful error messages

### Separation of Concerns
✅ Frontend handles **UI only**  
✅ Backend handles **logic only**  
✅ No Tkinter or desktop GUI  
✅ Clean imports and no circular dependencies  

---

## 🛑 Troubleshooting

### "GroqAPIKey not found in .env file"
- Create/update `.env` file in project root
- Add `GroqAPIKey=your_actual_api_key`

### App doesn't start
- Run: `streamlit run --logger.level=debug Frontend/app.py`
- Check Python version: `python --version` (need 3.8+)

### Chat not working
- Verify backend Chatbot.py works: `python Backend/Chatbot.py`
- Check internet connection for Groq API calls

---

## 📝 File Structure

```
M8/
├── Frontend/
│   └── app.py                 ← Main Streamlit app (MODIFIED)
├── Backend/
│   ├── Chatbot.py             ← ChatBot() function
│   └── ... other modules
├── Data/
│   └── ChatLog.json           ← Conversation history
└── .env                       ← API keys (required)
```

---

## 💡 Tips

- **Fast Reloads**: Streamlit auto-reloads on file changes
- **Debug Mode**: Add print statements - they appear in terminal
- **Full Screen**: Press `F` in the app for fullscreen mode
- **Chat History**: Located in `Data/ChatLog.json`

---

## 📦 Dependencies Summary

| Package | Purpose |
|---------|---------|
| `streamlit` | Web UI framework |
| `groq` | Groq API client |
| `python-dotenv` | Environment variables |

Install all at once:
```bash
pip install streamlit groq python-dotenv
```

---

**Enjoy your M8 AI Assistant!** 🚀
