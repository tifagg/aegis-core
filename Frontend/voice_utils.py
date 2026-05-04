"""
Voice Integration Utilities for M8 AI Assistant

This module provides helper functions for voice input/output integration.
Currently optional - can be integrated into Frontend/app.py when needed.

Requirements:
    - For voice input: pip install SpeechRecognition pyaudio
    - For voice output: pip install pyttsx3 (already available in backend)
"""

import os
import sys

# ============================================================================
# VOICE INPUT (Speech-to-Text)
# ============================================================================

def transcribe_voice_input(timeout_seconds: int = 10) -> str:
    """
    Capture and transcribe voice input using System Microphone
    
    Args:
        timeout_seconds: Max time to listen (default 10 seconds)
    
    Returns:
        Transcribed text or empty string if failed
    
    Requirements:
        pip install SpeechRecognition pyaudio
    """
    try:
        import speech_recognition as sr
        
        recognizer = sr.Recognizer()
        
        with sr.Microphone() as source:
            print("Listening...")
            try:
                # Adjust for background noise
                recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Capture audio
                audio = recognizer.listen(
                    source,
                    timeout=timeout_seconds,
                    phrase_time_limit=timeout_seconds
                )
                
                # Transcribe using Google Speech Recognition (free)
                text = recognizer.recognize_google(audio)
                return text
                
            except sr.UnknownValueError:
                print("Could not understand audio. Please speak clearly.")
                return ""
            except sr.RequestError as e:
                print(f"Microphone error: {e}")
                return ""
                
    except ImportError:
        print("Error: SpeechRecognition not installed.")
        print("Install with: pip install SpeechRecognition pyaudio")
        return ""
    except Exception as e:
        print(f"Voice input error: {e}")
        return ""


def check_microphone_available() -> bool:
    """
    Check if microphone is available on system
    
    Returns:
        True if microphone detected, False otherwise
    """
    try:
        import speech_recognition as sr
        
        # List available microphones
        microphones = sr.Microphone.list_microphone_indexes()
        return len(microphones) > 0
        
    except Exception:
        return False


# ============================================================================
# INTEGRATION WITH STREAMLIT
# ============================================================================

def get_voice_input_widget():
    """
    Generate Streamlit voice input widget code (helper)
    
    Usage in Frontend/app.py:
    
        if st.session_state.is_listening:
            with st.spinner("Listening..."):
                user_voice = transcribe_voice_input(timeout_seconds=15)
                if user_voice:
                    process_user_input(user_voice)
    """
    return """
    # Add to voice mode section of Frontend/app.py
    if st.session_state.is_listening:
        col1, col2 = st.columns([1, 0.15])
        
        with col1:
            st.markdown('<p class="loading-text">🎤 Recording...</p>', unsafe_allow_html=True)
        
        with col2:
            if st.button("Stop", key="stop_listening"):
                st.session_state.is_listening = False
                st.rerun()
    """


# ============================================================================
# TESTING & DIAGNOSTICS
# ============================================================================

def test_voice_setup() -> dict:
    """
    Test if voice components are properly set up
    
    Returns:
        Dictionary with setup status information
    """
    results = {
        "speech_recognition": False,
        "microphone_available": False,
        "errors": []
    }
    
    try:
        import speech_recognition as sr
        results["speech_recognition"] = True
    except ImportError:
        results["errors"].append(
            "SpeechRecognition not installed. Run: pip install SpeechRecognition pyaudio"
        )
    
    if results["speech_recognition"]:
        try:
            if check_microphone_available():
                results["microphone_available"] = True
            else:
                results["errors"].append("No microphone detected on system")
        except Exception as e:
            results["errors"].append(f"Microphone check failed: {str(e)}")
    
    return results


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("Voice Integration Utilities for M8 AI Assistant\n")
    
    # Test setup
    print("Testing voice setup...")
    test_results = test_voice_setup()
    
    print(f"  ✓ SpeechRecognition: {'Available' if test_results['speech_recognition'] else 'Not installed'}")
    print(f"  ✓ Microphone: {'Available' if test_results['microphone_available'] else 'Not available'}")
    
    if test_results["errors"]:
        print("\nErrors found:")
        for error in test_results["errors"]:
            print(f"  ⚠ {error}")
    else:
        print("\n✓ All voice components ready!")
        
        # Try recording
        print("\nTesting voice input (speak something)...")
        text = transcribe_voice_input(timeout_seconds=5)
        if text:
            print(f"Transcribed: {text}")
        else:
            print("No input captured")
