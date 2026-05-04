import cohere
from dotenv import dotenv_values
import os

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_vars = dotenv_values(os.path.join(current_dir, ".env"))
CO_API_KEY = env_vars.get("CO_API_KEY")

if not CO_API_KEY:
    raise ValueError("CO_API_KEY not found in .env")

co = cohere.Client(api_key=CO_API_KEY)

funcs = [
    "exit", "general", "realtime", "open", "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "reminder", "email check", "email send", "email summarize"
]

preamble = """
You are a Decision-Making Model. Classify user queries into one of these categories only — do NOT answer them.

-> 'general (query)' — for conversational questions, math, history, time/date, definitions, incomplete queries, or anything a chatbot can answer without live data.
-> 'realtime (query)' — for questions requiring live/current data: news, prices, weather, recent events, named public figures' current status.
-> 'open (app/website)' — to open apps or sites. Multiple: 'open chrome, open spotify'
-> 'close (app)' — to close apps. Multiple: 'close notepad, close chrome'
-> 'play (song)' — to play songs on YouTube.
-> 'generate image (prompt)' — to generate an image.
-> 'system (command)' — for mute, unmute, volume up, volume down.
-> 'content (topic)' — to write letters, essays, code, emails, etc.
-> 'google search (topic)' — to search Google.
-> 'youtube search (topic)' — to search YouTube.
-> 'email check' — check inbox.
-> 'email summarize' — summarize emails.
-> 'email send (recipient, subject, message)' — send an email.
-> 'exit' — user says goodbye or wants to quit.

For multiple tasks: 'open chrome, play shape of you, general what is python'
Default to 'general (query)' if unsure.
"""

ChatHistory = [
    {"role": "User", "message": "open chrome and tell me about mahatma gandhi"},
    {"role": "Chatbot", "message": "open chrome, general tell me about mahatma gandhi"},
    {"role": "User", "message": "what is today's date and remind me I have a meeting at 9pm"},
    {"role": "Chatbot", "message": "general what is today's date, reminder 9:00pm meeting"},
    {"role": "User", "message": "check my emails"},
    {"role": "Chatbot", "message": "email check"},
    {"role": "User", "message": "generate image of a sunset over mountains"},
    {"role": "Chatbot", "message": "generate image sunset over mountains"},
    {"role": "User", "message": "play shape of you"},
    {"role": "Chatbot", "message": "play shape of you"},
    {"role": "User", "message": "bye"},
    {"role": "Chatbot", "message": "exit"},
]


def FirstLayerDMM(prompt: str = "test") -> list:
    try:
        stream = co.chat_stream(
            model="command-a-03-2025",
            message=prompt,
            temperature=0.5,
            chat_history=ChatHistory,
            prompt_truncation="OFF",
            connectors=[],
            preamble=preamble,
        )

        response = ""
        for event in stream:
            if event.event_type == "text-generation":
                response += event.text

        response = response.replace("\n", "").strip()
        parts = [p.strip() for p in response.split(",")]

        valid = []
        for part in parts:
            for func in funcs:
                if part.startswith(func):
                    valid.append(part)
                    break

        if "(query)" in valid:
            return FirstLayerDMM(prompt)

        return valid if valid else [f"general {prompt}"]

    except Exception as e:
        print(f"[Model] Error: {e}")
        return [f"general {prompt}"]


if __name__ == "__main__":
    while True:
        user = input(">>> ")
        print(FirstLayerDMM(user))

