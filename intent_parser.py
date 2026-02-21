import json
import re
from gemini_service import call_gemini

def clean_json(text: str) -> str:
    text = re.sub(r"```json|```", "", text)
    return text.strip()

def extract_intent(user_command: str) -> dict:
    prompt = f"""
You are an intent extraction engine.

RULES:
- Return ONLY valid JSON
- No explanation
- No markdown
- No extra text

JSON FORMAT:
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
    except Exception:
        return {
            "intent": "PARSE_ERROR",
            "raw_response": response
        }
