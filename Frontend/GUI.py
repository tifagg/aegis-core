import os
import tkinter as tk

# Global state variables
assistant_status = "Available..."
microphone_status = "False"

# Paths
def get_temp_path(filename: str) -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    files_dir = os.path.join(base_dir, "Files")
    os.makedirs(files_dir, exist_ok=True)
    return os.path.join(files_dir, filename)

# Status setters/getters
def SetAssistantStatus(status: str):
    global assistant_status
    assistant_status = status
    print(f"[GUI] Assistant status set to: {status}")

def GetAssistantStatus() -> str:
    return assistant_status

def SetMicroPhoneStatus(status: str):
    global microphone_status
    microphone_status = status
    print(f"[GUI] Microphone status set to: {status}")

def GetMicroPhoneStatus() -> str:
    return microphone_status

# Text display
def ShowTextToScreen(text: str):
    print(f"[GUI] Screen text: {text}")

# Answer modifier
def AnswerModifier(text: str) -> str:
    # Simple placeholder: you can expand with formatting
    return text.strip()

# Query modifier
def QueryModifier(text: str) -> str:
    # Simple placeholder: you can expand with preprocessing
    return text.strip()

# GUI main loop
def GraphicalUserInterface():
    root = tk.Tk()
    root.title("M8 Assistant")

    status_label = tk.Label(root, text=f"Status: {assistant_status}", font=("Arial", 12))
    status_label.pack(pady=10)

    mic_label = tk.Label(root, text=f"Microphone: {microphone_status}", font=("Arial", 12))
    mic_label.pack(pady=10)

    text_area = tk.Text(root, height=10, width=50)
    text_area.pack(pady=10)

    def update_labels():
        status_label.config(text=f"Status: {assistant_status}")
        mic_label.config(text=f"Microphone: {microphone_status}")
        root.after(1000, update_labels)

    update_labels()
    root.mainloop()
