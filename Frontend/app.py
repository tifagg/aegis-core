import sys
import os

# Add parent directory to path so Backend module can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from Backend.Chatbot import ChatBot
import time

# ============================================================================
# PAGE CONFIGURATION & THEME
# ============================================================================

st.set_page_config(
    page_title="M8 AI Assistant",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CUSTOM DARK THEME STYLING
# ============================================================================

st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0e1a 0%, #1a1f3a 100%);
        color: #ffffff;
    }
    
    [data-testid="stMainBlockContainer"] {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Chat Messages */
    .user-message {
        background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
        border-radius: 18px;
        padding: 12px 16px;
        margin: 8px 0;
        width: fit-content;
        max-width: 75%;
        margin-left: auto;
        word-wrap: break-word;
        box-shadow: 0 4px 15px rgba(30, 64, 175, 0.3);
        animation: slideInRight 0.3s ease-out;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        border-radius: 18px;
        padding: 12px 16px;
        margin: 8px 0;
        width: fit-content;
        max-width: 75%;
        margin-right: auto;
        word-wrap: break-word;
        border: 1px solid #374151;
        box-shadow: 0 4px 15px rgba(200, 200, 200, 0.1);
        animation: slideInLeft 0.3s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(50px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideInLeft {
        from {
            transform: translateX(-50px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.7;
        }
    }
    
    @keyframes glow {
        0%, 100% {
            box-shadow: 0 0 20px rgba(96, 165, 250, 0.5), inset 0 0 20px rgba(96, 165, 250, 0.2);
        }
        50% {
            box-shadow: 0 0 40px rgba(96, 165, 250, 0.8), inset 0 0 20px rgba(96, 165, 250, 0.3);
        }
    }
    
    .listening-indicator {
        animation: glow 1.5s ease-in-out infinite;
    }
    
    .orb {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, #60a5fa, #3b82f6, #1e40af);
        margin: 0 auto;
        box-shadow: 0 0 30px rgba(96, 165, 250, 0.6), inset -2px -2px 5px rgba(0, 0, 0, 0.5), inset 2px 2px 5px rgba(255, 255, 255, 0.1);
    }
    
    .orb.active {
        animation: glow 1.5s ease-in-out infinite;
    }
    
    /* Input Box */
    .stTextInput > div > div > input {
        border-radius: 12px;
        background-color: #1f2937 !important;
        border: 1px solid #374151 !important;
        color: #ffffff !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border: 1px solid #60a5fa !important;
        box-shadow: 0 0 10px rgba(96, 165, 250, 0.3) !important;
    }
    
    /* Buttons */
    .mode-button {
        background: linear-gradient(135deg, #374151 0%, #1f2937 100%);
        border: 1px solid #4b5563;
        color: #ffffff;
        padding: 10px 20px;
        border-radius: 10px;
        cursor: pointer;
        font-size: 13px;
        font-weight: 600;
        transition: all 0.3s ease;
        margin: 0 4px;
    }
    
    .mode-button:hover {
        background: linear-gradient(135deg, #4b5563 0%, #374151 100%);
        border: 1px solid #60a5fa;
    }
    
    .mode-button.active {
        background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
        border: 1px solid #60a5fa;
        box-shadow: 0 0 15px rgba(96, 165, 250, 0.4);
    }
    
    /* Status indicators */
    .status-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-top: 8px;
    }
    
    .status-listening {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: #ffffff;
    }
    
    .status-ready {
        background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
        color: #ffffff;
    }
    
    /* Text styling */
    .title {
        font-size: 32px;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        font-size: 13px;
        color: #9ca3af;
        text-align: center;
        margin: 4px 0 0 0;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    .loading-text {
        color: #60a5fa;
        font-size: 14px;
        text-align: center;
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    /* Chat container */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 8px;
        padding: 16px 0;
        min-height: 300px;
        max-height: 500px;
        overflow-y: auto;
    }
    
    /* Remove Streamlit defaults */
    .stChatMessage {
        background: transparent !important;
        padding: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "is_voice_mode" not in st.session_state:
    st.session_state.is_voice_mode = False

if "is_listening" not in st.session_state:
    st.session_state.is_listening = False

if "loading" not in st.session_state:
    st.session_state.loading = False

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def add_message(role: str, content: str):
    """Add a message to chat history."""
    st.session_state.messages.append({"role": role, "content": content})


def render_chat_message(role: str, content: str):
    """Render a single chat message with proper styling."""
    if role == "user":
        st.markdown(
            f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 16px;">
                <div class="user-message">{content}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="display: flex; justify-content: flex-start; margin-bottom: 16px;">
                <div class="assistant-message">{content}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_orb(is_listening: bool = False):
    """Render the glowing orb visual element."""
    active_class = "active" if is_listening else ""
    st.markdown(
        f"""
        <div style="text-align: center; margin: 24px 0;">
            <div class="orb {active_class}"></div>
        </div>
        """,
        unsafe_allow_html=True
    )


def get_status_badge(is_voice: bool, is_listening: bool) -> str:
    """Get appropriate status badge HTML."""
    if is_voice and is_listening:
        return '<span class="status-badge status-listening">🎤 LISTENING</span>'
    elif is_voice:
        return '<span class="status-badge status-ready">🔴 READY</span>'
    else:
        return '<span class="status-badge status-ready">✓ READY</span>'


def process_user_input(user_input: str):
    """Process user input and get AI response."""
    if not user_input.strip():
        return
    
    # Add user message
    add_message("user", user_input)
    
    # Set loading state
    st.session_state.loading = True
    st.rerun()


def get_ai_response(user_input: str) -> str:
    """Get response from ChatBot backend."""
    try:
        response = ChatBot(user_input)
        return response
    except Exception as e:
        return f"Error: Unable to process your request. {str(e)}"


# ============================================================================
# UI HEADER
# ============================================================================

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    st.markdown('<p class="title">M8</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI Assistant</p>', unsafe_allow_html=True)

# Glowing Orb
render_orb(is_listening=st.session_state.is_listening)

# ============================================================================
# MODE CONTROLS
# ============================================================================

mode_col1, mode_col2, mode_col3 = st.columns([1, 1, 1])

with mode_col1:
    if st.button(
        "💬 Chat Mode",
        key="chat_mode_btn",
        use_container_width=True,
        disabled=not st.session_state.is_voice_mode
    ):
        st.session_state.is_voice_mode = False
        st.session_state.is_listening = False
        st.rerun()

with mode_col3:
    if st.button(
        "🎤 Voice Mode",
        key="voice_mode_btn",
        use_container_width=True,
        disabled=st.session_state.is_voice_mode
    ):
        st.session_state.is_voice_mode = True
        st.rerun()

# Show status
status_html = get_status_badge(st.session_state.is_voice_mode, st.session_state.is_listening)
st.markdown(f"<div style='text-align: center;'>{status_html}</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

# ============================================================================
# CHAT DISPLAY
# ============================================================================

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown(
        """
        <div style='text-align: center; color: #9ca3af; padding: 40px 20px;'>
            <p style='font-size: 14px; margin: 0;'>Start a conversation</p>
            <p style='font-size: 12px; margin: 8px 0 0 0; color: #6b7280;'>Type or speak your question</p>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    for msg in st.session_state.messages:
        render_chat_message(msg["role"], msg["content"])

st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# PROCESSING RESPONSES
# ============================================================================

if st.session_state.loading and st.session_state.messages:
    last_message = st.session_state.messages[-1]
    
    if last_message["role"] == "user":
        with st.spinner(""):
            st.markdown(
                "<p class='loading-text'>✨ Thinking...</p>",
                unsafe_allow_html=True
            )
            
            # Get AI response
            response = get_ai_response(last_message["content"])
            
            # Add assistant message
            add_message("assistant", response)
            
            # Reset loading state
            st.session_state.loading = False
            
            # Rerun to display response
            st.rerun()

# ============================================================================
# INPUT & INTERACTION
# ============================================================================

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

input_col1, input_col2 = st.columns([1, 0.12], gap="small")

with input_col1:
    user_input = st.chat_input(
        placeholder="Type your message..." if not st.session_state.is_voice_mode else "Say something...",
        key="user_input"
    )
    
    if user_input:
        process_user_input(user_input)

with input_col2:
    if st.session_state.is_voice_mode:
        if st.button("🎙️", key="mic_toggle", help="Toggle microphone", use_container_width=True):
            st.session_state.is_listening = not st.session_state.is_listening
            st.rerun()

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: center; color: #6b7280; font-size: 11px; margin-top: 12px;'>
        <p style='margin: 0;'>Powered by M8 Intelligence</p>
    </div>
    """,
    unsafe_allow_html=True
)

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Call your chatbot
    response = ChatBot(user_input)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})