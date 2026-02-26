import requests

def call_ollama(prompt: str):
    print("Calling Ollama (phi3)...")

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    print("Ollama responded")

    response.raise_for_status()
    return response.json()["response"]