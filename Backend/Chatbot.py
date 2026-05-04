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

if GroqAPIKey:
    pass
else:
    raise ValueError("GroqAPIKey not found in .env file.")

client = Groq(api_key=GroqAPIKey)

System = f"""You are {Assistantname}, a helpful and accurate AI assistant for {Username}.
- Answer concisely and clearly. Do not pad responses.
- Reply only in English.
- Do not mention your training data or knowledge cutoff.
- Do not include notes or disclaimers unless asked.
"""

SystemChatBot = [{"role": "system", "content": System}]

chat_log_path = os.path.join(current_dir, "Data", "ChatLog.json")
os.makedirs(os.path.dirname(chat_log_path), exist_ok=True)

try:
    with open(chat_log_path, "r", encoding="utf-8") as f:
        messages = load(f)
except (FileNotFoundError, ValueError):
    messages = []
    with open(chat_log_path, "w", encoding="utf-8") as f:
        dump(messages, f, indent=4)


def RealtimeInformation() -> str:
    now = datetime.datetime.now()
    return (
        f"Current datetime: {now.strftime('%A, %d %B %Y')} "
        f"at {now.strftime('%H:%M:%S')}"
    )


def AnswerModifier(answer: str) -> str:
    if not isinstance(answer, str):
        return str(answer)
    lines = [l for l in answer.split("\n") if l.strip()]
    return "\n".join(lines)


def ChatBot(Query: str) -> str:
    if not Query or not isinstance(Query, str):
        return "Invalid input."
    try:
        with open(chat_log_path, "r", encoding="utf-8") as f:
            messages = load(f)

        messages.append({"role": "user", "content": Query})

        time_ctx = {"role": "system", "content": RealtimeInformation()}

        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=SystemChatBot + [time_ctx] + messages,
            max_tokens=2000,
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

    except Exception as e:
        print(f"[Chatbot] Error: {e}")
        return "I encountered an error. Please check your Groq API key and try again."


if __name__ == "__main__":
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ("exit", "quit"):
                break
            print(f"Assistant: {ChatBot(user_input)}")
        except KeyboardInterrupt:
            break