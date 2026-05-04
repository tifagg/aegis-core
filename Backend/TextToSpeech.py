import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(current_dir, "Data"), exist_ok=True)
os.makedirs(os.path.join(current_dir, "Frontend", "Files"), exist_ok=True)

env_vars = dotenv_values(os.path.join(current_dir, ".env"))
AssistantVoice = env_vars.get("AssistantVoice", "en-US-GuyNeural")  # Windows-friendly default


async def TextToAudioFile(text: str) -> None:
    file_path = os.path.join(current_dir, "Data", "speech.mp3")
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"[TTS] Could not remove old speech file: {e}")

    communicate = edge_tts.Communicate(text, AssistantVoice, pitch="+5Hz", rate="+13%")
    await communicate.save(file_path)

    if not os.path.exists(file_path):
        raise RuntimeError("Speech file was not created.")


def TTS(text: str, func=lambda r=None: True) -> bool:
    try:
        # Run async audio generation
        asyncio.run(TextToAudioFile(text))

        file_path = os.path.join(current_dir, "Data", "speech.mp3")

        # Reset pygame mixer safely
        try:
            pygame.mixer.quit()
        except Exception:
            pass

        pygame.mixer.init(frequency=44100)
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            if func() is False:
                break
            pygame.time.Clock().tick(10)

        return True

    except Exception as e:
        print(f"[TTS] Error: {e}")
        return False

    finally:
        try:
            func(False)
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception:
            pass


def TextToSpeech(text: str, func=lambda r=None: True) -> bool:
    if not text or not isinstance(text, str):
        print("[TTS] Invalid text input.")
        return False

    try:
        sentences = text.split(".")
        if len(sentences) > 4 and len(text) > 250:
            short = " ".join(text.split(".")[:2]) + ". "
            tail = random.choice([
                "The rest of the result has been printed to the chat screen.",
                "You can find the complete text on the chat screen.",
                "Please check the chat screen for the full response.",
            ])
            return TTS(short + tail, func)
        else:
            return TTS(text, func)

    except Exception as e:
        print(f"[TTS] TextToSpeech error: {e}")
        return False


if __name__ == "__main__":
    while True:
        try:
            text = input("Enter text: ")
            if text.lower() in ("exit", "quit"):
                break
            TextToSpeech(text)
        except KeyboardInterrupt:
            break
