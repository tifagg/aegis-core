import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import mtranslate as mt

# Resolve paths relative to project root
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_vars = dotenv_values(os.path.join(current_dir, ".env"))
InputLanguage = env_vars.get("InputLanguage", "en-US")

TempDirPath = os.path.join(current_dir, "Frontend", "Files")
os.makedirs(TempDirPath, exist_ok=True)
os.makedirs(os.path.join(current_dir, "Data"), exist_ok=True)

HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head><title>Speech Recognition</title></head>
<body>
    <button id="start" onclick="startRecognition()">Start</button>
    <button id="end" onclick="stopRecognition()">Stop</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;
        function startRecognition() {
            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'LANG_PLACEHOLDER';
            recognition.continuous = true;
            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };
            recognition.onend = function() { recognition.start(); };
            recognition.start();
        }
        function stopRecognition() {
            if (recognition) recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

HtmlCode = HtmlCode.replace("LANG_PLACEHOLDER", InputLanguage)

html_file_path = os.path.join(current_dir, "Data", "Voice.html")
with open(html_file_path, "w", encoding="utf-8") as f:
    f.write(HtmlCode)

# Use forward slashes for Windows file URL
file_url = "file:///" + html_file_path.replace("\\", "/")

# --- Chrome driver setup (Windows compatible) ---
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-file-access-from-files")
chrome_options.add_argument("--log-level=3")          # suppress console noise
chrome_options.add_argument("--headless=new")          # headless on Windows
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
except Exception as e:
    print(f"[SpeechToText] ChromeDriver init failed: {e}")
    driver = None


def SetAssistantStatus(status: str):
    path = os.path.join(TempDirPath, "Status.data")
    with open(path, "w", encoding="utf-8") as f:
        f.write(status)


def QueryModifier(Query: str) -> str:
    query = Query.lower().strip()
    words = query.split()
    question_words = ["how", "what", "who", "where", "why", "which",
                      "whose", "whom", "can you", "what's", "where's", "how's"]
    if any(query.startswith(w) for w in question_words):
        if words and words[-1][-1] in [".", "?", "!"]:
            query = query[:-1] + "?"
        else:
            query += "?"
    else:
        if words and words[-1][-1] in [".", "?", "!"]:
            query = query[:-1] + "."
        else:
            query += "."
    return query.capitalize()


def UniversalTranslator(text: str) -> str:
    translated = mt.translate(text, "en", "auto")
    return translated.capitalize()


def SpeechRecognition() -> str:
    if driver is None:
        return "Speech recognition unavailable: ChromeDriver not initialized."
    try:
        driver.get(file_url)
        time.sleep(1)
        driver.find_element(By.ID, "start").click()

        for _ in range(30):
            try:
                text = driver.find_element(By.ID, "output").text.strip()
                if text:
                    driver.find_element(By.ID, "end").click()
                    if "en" in InputLanguage.lower():
                        return QueryModifier(text)
                    else:
                        SetAssistantStatus("Translating...")
                        return QueryModifier(UniversalTranslator(text))
            except Exception:
                pass
            time.sleep(1)

        return "I couldn't hear anything. Please try again."
    except Exception as e:
        print(f"[SpeechToText] Error: {e}")
        return "Speech recognition error. Please try again."


if __name__ == "__main__":
    while True:
        print(SpeechRecognition())
