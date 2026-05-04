import asyncio
import os
import subprocess
from random import randint
from time import sleep

import requests
from dotenv import dotenv_values

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_vars = dotenv_values(os.path.join(current_dir, ".env"))
HuggingFaceAPIKey = env_vars.get("HuggingFaceAPIKey")

if not HuggingFaceAPIKey:
    raise ValueError("HuggingFaceAPIKey not found in .env")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HuggingFaceAPIKey}"}


def open_image_windows(path: str):
    """Open image with default viewer on Windows."""
    try:
        os.startfile(path)
    except Exception as e:
        print(f"[ImageGen] Could not open image: {e}")


async def query(payload: dict):
    try:
        response = await asyncio.to_thread(
            requests.post, API_URL, headers=headers, json=payload, timeout=60
        )
        if response.status_code == 200:
            return response.content
        elif response.status_code == 503:
            print("[ImageGen] Model loading, retrying in 10s...")
            await asyncio.sleep(10)
            return None
        elif response.status_code == 429:
            print("[ImageGen] Rate limited, retrying in 5s...")
            await asyncio.sleep(5)
            return None
        else:
            print(f"[ImageGen] API error {response.status_code}: {response.text[:200]}")
            return None
    except Exception as e:
        print(f"[ImageGen] Request error: {e}")
        return None


async def generate_images(prompt: str):
    folder = os.path.join(current_dir, "Data")
    os.makedirs(folder, exist_ok=True)

    safe_prompt = prompt.replace(" ", "_")[:50]
    tasks = [
        asyncio.create_task(query({
            "inputs": f"{prompt}, 4K, ultra high detail, high resolution, sharp",
            "seed": randint(0, 1_000_000)
        }))
        for _ in range(4)
    ]

    results = await asyncio.gather(*tasks)
    saved = 0
    for i, data in enumerate(results):
        if data:
            path = os.path.join(folder, f"{safe_prompt}_{i+1}.jpg")
            try:
                with open(path, "wb") as f:
                    f.write(data)
                print(f"[ImageGen] Saved: {path}")
                open_image_windows(path)
                saved += 1
            except Exception as e:
                print(f"[ImageGen] Save error: {e}")

    if saved == 0:
        print("[ImageGen] No images were generated successfully.")


def GenerateImage(prompt: str):
    if not prompt or not isinstance(prompt, str):
        print("[ImageGen] Invalid prompt.")
        return
    try:
        asyncio.run(generate_images(prompt))
    except Exception as e:
        print(f"[ImageGen] Error: {e}")


if __name__ == "__main__":
    data_file = os.path.join(current_dir, "Frontend", "Files", "ImageGeneration.data")
    os.makedirs(os.path.dirname(data_file), exist_ok=True)

    if not os.path.exists(data_file):
        with open(data_file, "w") as f:
            f.write(",False")

    while True:
        try:
            with open(data_file, "r") as f:
                raw = f.read().strip()
            if "," not in raw:
                raw = ",False"
            prompt, status = raw.split(",", 1)

            if status.strip().lower() == "true" and prompt.strip():
                print(f"[ImageGen] Generating: {prompt.strip()}")
                GenerateImage(prompt.strip())
                with open(data_file, "w") as f:
                    f.write(",False")
                break

            sleep(1)
        except Exception as e:
            print(f"[ImageGen] Loop error: {e}")
            sleep(1)
