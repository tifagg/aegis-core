import asyncio
import os
import re
import subprocess
import webbrowser

import requests
from bs4 import BeautifulSoup
from dotenv import dotenv_values
from groq import Groq
from pywhatkit import search, playonyt
from rich import print

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_vars = dotenv_values(os.path.join(current_dir, ".env"))
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

SystemChatBot = [
    {"role": "system", "content": "You are a content writer. Write letters, code, essays, emails, poems, etc. as requested."}
]
messages = []

# ── Helpers ──────────────────────────────────────────────────────────────────

def GoogleSearch(topic: str) -> bool:
    search(topic)
    return True


def YoutubeSearch(topic: str) -> bool:
    webbrowser.open(f"https://www.youtube.com/results?search_query={topic}")
    return True


def playYoutube(query: str) -> bool:
    playonyt(query)
    return True


# ── Windows: open / close apps ───────────────────────────────────────────────

def OpenApp(app: str) -> bool:
    """Open an application on Windows using 'start' command, fallback to browser."""
    try:
        # Try running by name (works for apps in PATH like notepad, calc, etc.)
        subprocess.Popen(["cmd", "/c", "start", "", app], shell=False)
        return True
    except Exception:
        pass
    # Fallback: open a Google search for the app
    webbrowser.open(f"https://www.google.com/search?q={app}+download")
    return True


def CloseApp(app: str) -> bool:
    """Kill a process by name on Windows."""
    try:
        # taskkill works for most Windows processes
        subprocess.run(
            ["taskkill", "/F", "/IM", f"{app}.exe"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except Exception as e:
        print(f"[Automation] CloseApp error: {e}")
        return False


# ── System commands ───────────────────────────────────────────────────────────

def System(command: str) -> bool:
    cmd = command.lower().strip()

    if cmd == "mute":
        # Windows: use nircmd if available, else PowerShell
        _set_volume_mute(True)
    elif cmd == "unmute":
        _set_volume_mute(False)
    elif cmd == "volume up":
        _change_volume(+10)
    elif cmd == "volume down":
        _change_volume(-10)
    else:
        print(f"[Automation] Unknown system command: {command}")
    return True


def _set_volume_mute(mute: bool):
    state = "1" if mute else "0"
    ps = (
        f"$obj = New-Object -ComObject WScript.Shell; "
        f"$code = 0x{173 if mute else 173:04X}; "  # VK_VOLUME_MUTE
    )
    # Simpler: use PowerShell to toggle mute via SendKeys
    action = "Mute" if mute else "Unmute"
    try:
        subprocess.run(
            ["powershell", "-command",
             f"(New-Object -ComObject WScript.Shell).SendKeys([char]173)"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"[Automation] {action} error: {e}")


def _change_volume(delta: int):
    key = "[volume_up]" if delta > 0 else "[volume_down]"
    steps = abs(delta) // 2
    try:
        for _ in range(steps):
            subprocess.run(
                ["powershell", "-command",
                 f"(New-Object -ComObject WScript.Shell).SendKeys([char]{175 if delta > 0 else 174})"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
    except Exception as e:
        print(f"[Automation] Volume change error: {e}")


# ── Content writer ────────────────────────────────────────────────────────────

def Content(topic: str) -> bool:
    topic = topic.replace("content", "").strip()

    messages.append({"role": "user", "content": topic})
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=SystemChatBot + messages,
        max_tokens=2048,
        temperature=0.7,
        stream=True,
    )
    answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            answer += chunk.choices[0].delta.content
    answer = answer.replace("</s>", "")
    messages.append({"role": "assistant", "content": answer})

    data_dir = os.path.join(current_dir, "Data")
    os.makedirs(data_dir, exist_ok=True)
    safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', topic.lower())[:50]
    file_path = os.path.join(data_dir, f"{safe_name}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(answer)

    # Open with default text editor on Windows (notepad)
    try:
        os.startfile(file_path)
    except Exception as e:
        print(f"[Automation] Could not open file: {e}")
    return True


# ── Async dispatcher ──────────────────────────────────────────────────────────

async def TranslateAndExecute(commands: list):
    funcs = []

    for command in commands:
        if not isinstance(command, str):
            continue

        if command.startswith("open ") and command not in ("open it", "open file"):
            funcs.append(asyncio.to_thread(OpenApp, command[5:]))

        elif command.startswith("close "):
            funcs.append(asyncio.to_thread(CloseApp, command[6:]))

        elif command.startswith("play "):
            funcs.append(asyncio.to_thread(playYoutube, command[5:]))

        elif command.startswith("content "):
            funcs.append(asyncio.to_thread(Content, command[8:]))

        elif command.startswith("google search "):
            funcs.append(asyncio.to_thread(GoogleSearch, command[14:]))

        elif command.startswith("youtube search "):
            funcs.append(asyncio.to_thread(YoutubeSearch, command[15:]))

        elif command.startswith("system "):
            funcs.append(asyncio.to_thread(System, command[7:]))

        elif command.startswith("general ") or command.startswith("realtime "):
            pass  # handled in Main.py

        else:
            print(f"[Automation] No handler for: {command}")

    results = await asyncio.gather(*funcs, return_exceptions=True)
    for r in results:
        if isinstance(r, Exception):
            print(f"[Automation] Task error: {r}")


async def Automation(commands: list) -> bool:
    await TranslateAndExecute(commands)
    return True


if __name__ == "__main__":
    asyncio.run(Automation(["open notepad"]))

