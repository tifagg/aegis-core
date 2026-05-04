from googlesearch import search
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values
import os

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_vars = dotenv_values(os.path.join(current_dir, ".env"))

Username = env_vars.get("Username", "Tifa")
Assistantname = env_vars.get("Assistantname", "M8")
GroqAPIKey = env_vars.get("GroqAPIKey")

if not GroqAPIKey:
    raise ValueError("GroqAPIKey not found in .env")

client = Groq(api_key=GroqAPIKey)

System = f"""You are {Assistantname}, a highly accurate AI assistant for {Username}.
You have access to real-time internet search results provided below.
Answer professionally using the provided data. Use proper grammar and punctuation.
Do not mention that you were given search results."""

chat_log_path = os.path.join(current_dir, "Data", "ChatLog.json")
os.makedirs(os.path.dirname(chat_log_path), exist_ok=True)

try:
    with open(chat_log_path, "r", encoding="utf-8") as f:
        messages = load(f)
except (FileNotFoundError, ValueError):
    messages = []
    with open(chat_log_path, "w", encoding="utf-8") as f:
        dump([], f)

SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello! How can I help you?"},
]


def GoogleSearch(query: str) -> str:
    try:
        results = list(search(query, advanced=True, num_results=5))
        text = f"Search results for '{query}':\n\n"
        for r in results:
            text += f"Title: {r.title}\nSummary: {r.description}\n\n"
        return text
    except Exception as e:
        return f"Search failed: {e}"


def AnswerModifier(answer: str) -> str:
    lines = [l for l in answer.split("\n") if l.strip()]
    return "\n".join(lines)


def Information() -> str:
    now = datetime.datetime.now()
    return (
        f"Current date/time context:\n"
        f"Day: {now.strftime('%A')}, Date: {now.strftime('%d %B %Y')}, "
        f"Time: {now.strftime('%H:%M:%S')}"
    )


def RealtimeSearchEngine(prompt: str) -> str:
    global messages

    try:
        with open(chat_log_path, "r", encoding="utf-8") as f:
            messages = load(f)
    except Exception:
        messages = []

    messages.append({"role": "user", "content": prompt})

    context = SystemChatBot + [
        {"role": "system", "content": GoogleSearch(prompt)},
        {"role": "system", "content": Information()},
    ]

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=context + messages,
        max_tokens=2048,
        temperature=0.7,
        stream=True,
    )

    answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            answer += chunk.choices[0].delta.content
    answer = answer.replace("</s>", "").strip()

    messages.append({"role": "assistant", "content": answer})
    with open(chat_log_path, "w", encoding="utf-8") as f:
        dump(messages, f, indent=4)

    return AnswerModifier(answer)


while True:
    q = input("Query: ")
    if q.lower() in ["exit", "quit"]:
        print("Exiting loop...")
        break
    print(RealtimeSearchEngine(q))

