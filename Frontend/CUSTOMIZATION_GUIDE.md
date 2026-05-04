# M8 AI Assistant - Customization & Configuration Guide

## 🎨 Visual Customization

### Color Scheme

All colors are defined in the `<style>` section of `Frontend/app.py`. You can customize:

#### Dark Theme Colors
```css
/* Primary background gradient */
background: linear-gradient(135deg, #0a0e1a 0%, #1a1f3a 100%);

/* Update colors: */
#0a0e1a  → Darker black (#000000 for pure black)
#1a1f3a  → Dark blue (#0f1729 for darker)
```

#### Message Bubbles
```css
/* User message (blue) */
.user-message {
    background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
    box-shadow: 0 4px 15px rgba(30, 64, 175, 0.3);
}

/* Assistant message (gray) */
.assistant-message {
    background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
    border: 1px solid #374151;
    box-shadow: 0 4px 15px rgba(200, 200, 200, 0.1);
}

/* Customize:
   #1e40af → User message color (try #2563eb for lighter, #1e3a8a for darker)
   #1f2937 → Assistant message color
   #374151 → Border color
*/
```

#### Accent Colors (Glow Effects)
```css
/* Primary accent for glows and highlights */
rgba(96, 165, 250, ...)  /* Change 96, 165, 250 for different color */

/* Examples:
   Green glow: rgba(16, 185, 129, ...)
   Purple glow: rgba(168, 85, 247, ...)
   Red glow: rgba(239, 68, 68, ...)
*/
```

---

## 🎬 Animation Customization

### Chat Message Animations

```css
@keyframes slideInRight {
    from {
        transform: translateX(50px);    /* Change 50px for distance */
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

animation: slideInRight 0.3s ease-out;  /* Change 0.3s for speed */
```

**Animation Speeds:**
- `0.1s` - Very fast
- `0.3s` - Fast (current)
- `0.5s` - Medium
- `1.0s` - Slow
- `2.0s` - Very slow

### Pulsing/Glowing Effects

```css
@keyframes glow {
    0%, 100% {
        box-shadow: 0 0 20px rgba(96, 165, 250, 0.5), inset 0 0 20px rgba(96, 165, 250, 0.2);
    }
    50% {
        box-shadow: 0 0 40px rgba(96, 165, 250, 0.8), inset 0 0 20px rgba(96, 165, 250, 0.3);
    }
}

animation: glow 1.5s ease-in-out infinite;  /* Change 1.5s */
```

**Glow Patterns:**
- `1.0s` - Fast pulse
- `1.5s` - Medium pulse (current)
- `2.0s` - Slow pulse
- `3.0s` - Very slow, relaxing

---

## 🔮 Orb Customization

### Change Orb Size

```python
# In render_orb() function, modify the CSS:

<div class="orb"></div>

# In .orb CSS class:
.orb {
    width: 120px;    # Change this
    height: 120px;   # Match this
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #60a5fa, #3b82f6, #1e40af);
}
```

**Size Options:**
- `80px` - Small
- `100px` - Medium
- `120px` - Large (current)
- `150px` - Very large

### Change Orb Gradient

```css
background: radial-gradient(circle at 30% 30%, #60a5fa, #3b82f6, #1e40af);
                              ↑          ↑      ↑       ↑       ↑
                           grad pos   colors (lightest → darkest)
```

**Gradient Examples:**
```css
/* Purple */
radial-gradient(circle at 30% 30%, #a78bfa, #7c3aed, #5b21b6)

/* Green */
radial-gradient(circle at 30% 30%, #86efac, #22c55e, #15803d)

/* Red/Orange */
radial-gradient(circle at 30% 30%, #fca5a5, #f87171, #dc2626)

/* Cyan */
radial-gradient(circle at 30% 30%, #67e8f9, #06b6d4, #0891b2)
```

---

## 📝 Text & Typography

### Title & Subtitle

```python
# In UI HEADER section:

st.markdown('<p class="title">M8</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI Assistant</p>', unsafe_allow_html=True)

# Customize in CSS:
.title {
    font-size: 32px;        # Change size
    font-weight: 700;       # 400=light, 700=bold, 900=extra bold
    color: #ffffff;         # Change color
    letter-spacing: -0.5px; # Adjust letter spacing
}

.subtitle {
    font-size: 13px;
    letter-spacing: 1px;    # Increase for spread out text
    text-transform: uppercase;  # Remove for normal case
}
```

### Input Placeholder

```python
# In INPUT & INTERACTION section:

user_input = st.chat_input(
    placeholder="Type your message...",  # Change this
    key="user_input"
)
```

---

## 🎯 UI Layout

### Adjust Chat Container Size

```css
.chat-container {
    min-height: 300px;   # Minimum height
    max-height: 500px;   # Maximum height
    overflow-y: auto;    # Scrollable
    gap: 8px;           # Space between messages
    padding: 16px 0;    # Top/bottom padding
}
```

### Adjust Message Width

```css
.user-message {
    max-width: 75%;      # How wide messages can be (% of screen)
}

.assistant-message {
    max-width: 75%;      # Change to 80%, 90%, 100% etc
}
```

---

## 🔘 Button Customization

### Mode Switch Buttons

```python
# In MODE CONTROLS section:

if st.button(
    "💬 Chat Mode",     # Change button text/emoji
    key="chat_mode_btn",
    use_container_width=True,
    disabled=not st.session_state.is_voice_mode
):
```

### Button Styling

```css
.mode-button {
    background: linear-gradient(135deg, #374151 0%, #1f2937 100%);
    border: 1px solid #4b5563;
    padding: 10px 20px;      # Adjust button padding
    border-radius: 10px;     # Make rounder: 15px, 20px, etc
    font-size: 13px;
}

.mode-button:hover {
    background: linear-gradient(135deg, #4b5563 0%, #374151 100%);
    border: 1px solid #60a5fa;
}

.mode-button.active {
    background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
    box-shadow: 0 0 15px rgba(96, 165, 250, 0.4);
}
```

---

## 🎤 Voice Mode Customization

### Change Voice Mode Status Messages

In the `get_status_badge()` function:

```python
def get_status_badge(is_voice: bool, is_listening: bool) -> str:
    if is_voice and is_listening:
        return '<span class="status-badge status-listening">🎤 LISTENING</span>'
                                                            ↑ Change
    elif is_voice:
        return '<span class="status-badge status-ready">🔴 READY</span>'
                                                          ↑ Change
    else:
        return '<span class="status-badge status-ready">✓ READY</span>'
                                                        ↑ Change
```

### Status Badge Colors

```css
.status-listening {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);  /* Green */
}

.status-ready {
    background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);  /* Gray */
}

/* Change to:
   Red: linear-gradient(135deg, #ef4444 0%, #dc2626 100%)
   Purple: linear-gradient(135deg, #a855f7 0%, #9333ea 100%)
   Yellow: linear-gradient(135deg, #eab308 0%, #ca8a04 100%)
*/
```

---

## 🚀 Performance Optimization

### Reduce Animation Size

```python
# In style section, reduce animation:

animation: glow 2.0s ease-in-out infinite;  # Slower = less CPU
```

### Limit Chat Display

```python
# In CHAT DISPLAY section, add:

# Only show last 50 messages
messages_to_show = st.session_state.messages[-50:]
for msg in messages_to_show:
    render_chat_message(msg["role"], msg["content"])
```

---

## 🔗 Integration Points

### Connect Different Backend

Currently using `Backend.Chatbot.ChatBot()`. To use different backend:

```python
# In PROCESSING RESPONSES section:

# Current:
response = ChatBot(last_message["content"])

# Custom function:
def custom_ai_function(user_input):
    # Your logic here
    return response

# Change to:
response = custom_ai_function(last_message["content"])
```

### Add Metadata Display

```python
# Add after title:

st.markdown(f"""
<div style='text-align: center; color: #60a5fa; font-size: 11px;'>
📍 Connected | 🔌 Ready | ⚡ Active
</div>
""", unsafe_allow_html=True)
```

---

## 🐛 Debugging Tips

### Show Debug Info

Add at the top of the script:

```python
if st.sidebar.checkbox("Debug Mode"):
    st.sidebar.write("Session State:", st.session_state)
    st.sidebar.write("Messages:", len(st.session_state.messages))
```

### Log Messages

```python
def add_message(role: str, content: str):
    print(f"[LOG] {role}: {content[:50]}...")  # Add this
    st.session_state.messages.append({"role": role, "content": content})
```

---

## 📊 Theme Presets

Quick copy-paste theme configurations:

### Dark Blue (Default)
Already configured - no changes needed

### Dark Purple
```css
Background: #1a0933 to #2d1b4e
User Message: #6d28d9 to #5b21b6
Accent: rgba(168, 85, 247, ...)
Glow: 0 0 30px rgba(168, 85, 247, 0.6)
```

### Dark Green
```css
Background: #0a2e1a to #1a3a2e
User Message: #059669 to #047857
Accent: rgba(16, 185, 129, ...)
Glow: 0 0 30px rgba(16, 185, 129, 0.6)
```

### Dark Red/Orange
```css
Background: #2e1a0a to #3a2a1a
User Message: #dc2626 to #b91c1c
Accent: rgba(239, 68, 68, ...)
Glow: 0 0 30px rgba(239, 68, 68, 0.6)
```

---

## 💾 Saving Custom Configurations

Create a `config.json`:

```json
{
  "theme": {
    "primary_color": "#1e40af",
    "accent_color": "#60a5fa",
    "background_dark": "#0a0e1a",
    "background_light": "#1a1f3a"
  },
  "animations": {
    "message_speed": "0.3s",
    "glow_speed": "1.5s"
  },
  "orb": {
    "size": 120,
    "gradient": "radial-gradient(circle at 30% 30%, #60a5fa, #3b82f6, #1e40af)"
  }
}
```

Load in `app.py`:

```python
import json

with open("Frontend/config.json") as f:
    config = json.load(f)

# Use config values
st.markdown(f"""
<style>
:root {{
    --primary: {config['theme']['primary_color']};
}}
</style>
""", unsafe_allow_html=True)
```

---

**Need help? Check the inline comments in `Frontend/app.py` for exact line numbers!**
