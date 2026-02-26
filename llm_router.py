import requests
import google.generativeai as genai

# -------------------------
# GEMINI SETUP
# -------------------------
genai.configure(api_key="GEMINI_API_KEY")

def call_gemini(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text


# -------------------------
# OLLAMA (LLAMA 8B)
# -------------------------
def call_ollama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3:8b",
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()
    return response.json()["response"]


# -------------------------
# ROUTER (USER DECIDES)
# -------------------------
from gemini_service import call_gemini
from ollama_service import call_ollama

def call_llm(prompt: str, agent: str):
    agent = agent.lower()

    if agent == "llama":
        return call_ollama(prompt)

    elif agent == "gemini":
        return call_gemini(prompt)

    else:
        raise ValueError("Invalid agent. Use 'llama' or 'gemini'")