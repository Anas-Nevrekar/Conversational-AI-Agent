import json
from gemini_service import ask_gemini

def extract_intent(command):
    prompt = f"""
You are an intent extraction engine.

User command: "{command}"

Extract intent strictly in JSON:
{{
  "device": "<device name>",
  "action": "<on/off/increase/decrease>"
}}
"""

    response = ask_gemini(prompt)

    try:
        json_start = response.find("{")
        json_end = response.rfind("}") + 1
        intent_json = response[json_start:json_end]
        return json.loads(intent_json)
    except:
        return {
            "device": "unknown",
            "action": "unknown"
        }
