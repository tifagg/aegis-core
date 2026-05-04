import sys, os
sys.path.append(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "Backend"))
sys.path.append(os.path.join(BASE_DIR, "Frontend"))
import Frontend.GUI
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from Backend.EmailIntegration import EmailClient
from dotenv import dotenv_values
from asyncio import run
import subprocess
import threading
import json
import os
import sys
import time

print("ENV file path:", os.path.abspath(".env"))
print("File exists:", os.path.exists(".env"))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env_vars = dotenv_values(os.path.join(BASE_DIR, ".env"))
Username = env_vars.get("Username", "Tifa")
Assistantname = env_vars.get("Assistantname", "M8")

DefaultMessage = (
    f"{Username} : Hello {Assistantname}, How are you?\n"
    f"{Assistantname} : Welcome {Username}. I am doing well. How may I help you?"
)

Automation_Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

def ShowDefaultChatIfNoChats():
    chatlog_path = os.path.join(BASE_DIR, "Data", "ChatLog.json")
    try:
        os.makedirs(os.path.join(BASE_DIR, "Data"), exist_ok=True)
        if not os.path.exists(chatlog_path):
            with open(chatlog_path, "w", encoding="utf-8") as f:
                f.write("[]")
        with open(chatlog_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content or content == "[]":
            with open(Frontend.GUI.get_temp_path("Database.data"), "w", encoding="utf-8") as f:
                f.write(DefaultMessage)
            with open(Frontend.GUI.get_temp_path("Responses.data"), "w", encoding="utf-8") as f:
                f.write("")
    except Exception as e:
        print(f"[Main] ShowDefaultChatIfNoChats error: {e}")

def ReadChatLogJson() -> list:
    chatlog_path = os.path.join(BASE_DIR, "Data", "ChatLog.json")
    try:
        with open(chatlog_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def ChatLogIntegration():
    data = ReadChatLogJson()
    log = ""
    for entry in data:
        role = (entry.get("role") or "").lower()
        content = entry.get("content", "")
        if role == "user":
            log += f"{Username}: {content}\n"
        elif role == "assistant":
            log += f"{Assistantname}: {content}\n"
    try:
        with open(Frontend.GUI.get_temp_path("Database.data"), "w", encoding="utf-8") as f:
            f.write(Frontend.GUI.AnswerModifier(log))
    except Exception as e:
        print(f"[Main] ChatLogIntegration error: {e}")

def ShowChatsOnGUI():
    try:
        db_path = Frontend.GUI.get_temp_path("Database.data")
        if os.path.exists(db_path):
            with open(db_path, "r", encoding="utf-8") as f:
                data = f.read()
            with open(db_path, "w", encoding="utf-8") as f:
                f.write(data)
    except Exception as e:
        print(f"[Main] ShowChatsOnGUI error: {e}")

def InitialExecution():
    try:
        os.makedirs(os.path.join(BASE_DIR, "Data"), exist_ok=True)
        os.makedirs(os.path.join(BASE_DIR, "Frontend", "Files"), exist_ok=True)
        Frontend.GUI.SetAssistantStatus("Available...")
        Frontend.GUI.SetMicroPhoneStatus("True")
        Frontend.GUI.ShowTextToScreen("")
        ShowDefaultChatIfNoChats()
        ChatLogIntegration()
        ShowChatsOnGUI()
        with open(Frontend.GUI.get_temp_path("Responses.data"), "w", encoding="utf-8") as f:
            f.write("")
        print("[Main] Initialization complete.")
    except Exception as e:
        print(f"[Main] InitialExecution error: {e}")

InitialExecution()

def MainExecution():
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""
    EmailExecution = False

    Frontend.GUI.SetAssistantStatus("Listening ...")
    Query = SpeechRecognition()
    print(f"[Main] Query: {Query}")
    Frontend.GUI.ShowTextToScreen(f"{Username} : {Query}")

    Frontend.GUI.SetAssistantStatus("Thinking ...")
    Decision = FirstLayerDMM(Query) or []
    print(f"[Main] Decision: {Decision}")

    G = any(isinstance(i, str) and i.startswith("general") for i in Decision)
    R = any(isinstance(i, str) and i.startswith("realtime") for i in Decision)

    Merged_query = " and ".join(
        " ".join(i.split()[1:])
        for i in Decision
        if isinstance(i, str) and (i.startswith("general") or i.startswith("realtime"))
    ).strip()

    for q in Decision:
        if isinstance(q, str) and q.startswith("generate image"):
            ImageGenerationQuery = q.replace("generate image", "").strip()
            ImageExecution = True

    for q in Decision:
        if EmailExecution:
            break
        if isinstance(q, str) and q.startswith("email"):
            EmailExecution = True
            email_client = EmailClient()
            if q.startswith("email check"):
                Frontend.GUI.SetAssistantStatus("Checking emails...")
                result = email_client.check_emails(limit=5)
                if isinstance(result, str):
                    Answer = result
                else:
                    Answer = "Here are your recent emails:\n\n"
                    for i, em in enumerate(result):
                        Answer += f"{i+1}. From: {em.get('sender','')}\n   Subject: {em.get('subject','')}\n   Date: {em.get('date','')}\n\n"
                Frontend.GUI.ShowTextToScreen(f"{Assistantname} : {Answer}")
                Frontend.GUI.SetAssistantStatus("Answering ...")
                TextToSpeech("I have checked your emails. Here is what I found.")
            elif q.startswith("email summarize"):
                Frontend.GUI.SetAssistantStatus("Summarizing emails...")
                result = email_client.summarize_emails(limit=10)
                Frontend.GUI.ShowTextToScreen(f"{Assistantname} : {result}")
                Frontend.GUI.SetAssistantStatus("Answering ...")
                TextToSpeech("I have summarized your recent emails.")
            elif q.startswith("email send"):
                parts = q.replace("email send", "").strip().split(",", 2)
                if len(parts) >= 3:
                    Frontend.GUI.SetAssistantStatus("Sending email...")
                    result = email_client.send_email(parts[0].strip(), parts[1].strip(), parts[2].strip())
                    Frontend.GUI.ShowTextToScreen(f"{Assistantname} : {result}")
                    Frontend.GUI.SetAssistantStatus("Answering ...")
                    TextToSpeech("I have sent the email as requested.")
                else:
                    msg = "I could not parse the email command. Please provide recipient, subject, and message."
                    Frontend.GUI.ShowTextToScreen(f"{Assistantname} : {msg}")
                    TextToSpeech(msg)
            return True

    for q in Decision:
        if not TaskExecution and isinstance(q, str) and any(q.startswith(f) for f in Automation_Functions):
            try:
                run(Automation(list(Decision)))
            except Exception as e:
                print(f"[Main] Automation error: {e}")
            TaskExecution = True

    if ImageExecution:
        image_data_path = os.path.join(BASE_DIR, "Frontend", "Files", "ImageGeneration.data")
        image_gen_script = os.path.join(BASE_DIR, "Backend", "ImageGeneration.py")
        try:
            with open(image_data_path, "w", encoding="utf-8") as f:
                f.write(f"{ImageGenerationQuery},True")
            subprocess.Popen([sys.executable, image_gen_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            print(f"[Main] Image generation error: {e}")

    try:
        if G or R:
            Frontend.GUI.SetAssistantStatus("Searching ..." if R else "Thinking ...")
            Answer = RealtimeSearchEngine(Frontend.GUI.QueryModifier(Merged_query)) if R else ChatBot(Frontend.GUI.QueryModifier(Merged_query))
            Frontend.GUI.ShowTextToScreen(f"{Assistantname} : {Answer}")
            Frontend.GUI.SetAssistantStatus("Answering ...")
            TextToSpeech(Answer)
            return True

        for q in Decision:
            if not isinstance(q, str):
                continue
            if "general" in q:
                Frontend.GUI.SetAssistantStatus("Thinking ...")
                Answer = ChatBot(Frontend.GUI.QueryModifier(q.replace("general", "").strip()))
                Frontend.GUI.ShowTextToScreen(f"{Assistantname} : {Answer}")
                Frontend.GUI.SetAssistantStatus("Answering ...")
                TextToSpeech(Answer)
                return True
            if "realtime" in q:
                Frontend.GUI.SetAssistantStatus("Searching ...")
                Answer = RealtimeSearchEngine(Frontend.GUI.QueryModifier(q.replace("realtime", "").strip()))
                Frontend.GUI.ShowTextToScreen(f"{Assistantname} : {Answer}")
                Frontend.GUI.SetAssistantStatus("Answering ...")
                TextToSpeech(Answer)
                return True
            if "exit" in q:
                Answer = ChatBot(Frontend.GUI.QueryModifier("Okay, Bye!"))
                Frontend.GUI.ShowTextToScreen(f"{Assistantname} : {Answer}")
                Frontend.GUI.SetAssistantStatus("Answering ...")
                TextToSpeech(Answer)
                os._exit(0)
    except Exception as e:
        print(f"[Main] Response handling error: {e}")
        return False

    return False

def FirstThread():
    processing_states = ["Thinking", "Listening", "Searching", "Answering"]
    while True:
        try:
            mic_status = Frontend.GUI.GetMicroPhoneStatus()
            ai_status = Frontend.GUI.GetAssistantStatus()
            if mic_status == "True":
                if not any(s in ai_status for s in processing_states):
                    MainExecution()
            else:
                if ai_status != "Available..." and not any(s in ai_status for s in processing_states):
                    Frontend.GUI.SetAssistantStatus("Available...")
            time.sleep(1.0)
        except Exception as e:
            print(f"[Main] FirstThread error: {e}")
            time.sleep(1.0)

if __name__ == "__main__":
    t = threading.Thread(target=FirstThread, daemon=True)
    t.start()