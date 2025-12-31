import json
import re
from gemini_service import call_gemini

def clean_json(text: str) -> str:
    # Remove ```json and ``` fences
    text = re.sub(r"```json|```", "", text)
    return text.strip()

def extract_intent(user_command: str) -> dict:
    prompt = f"""
You are an intent extraction engine for industrial IoT commands.

Return ONLY valid JSON.
Do NOT wrap in markdown.
Do NOT explain.

JSON schema:
{{
  "intent": "",
  "device": "",
  "action": "",
  "sensor": "",
  "condition": {{
    "sensor": "",
    "operator": "",
    "value": ""
  }}
}}

User command:
"{user_command}"
"""

    response = call_gemini(prompt)
    cleaned = clean_json(response)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {
            "intent": "UNKNOWN",
            "raw_response": response
        }
