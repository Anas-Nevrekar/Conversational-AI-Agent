import json
import re
from llm_router import call_llm

def extract_complete_json(text: str):
    """
    Finds the first '{' and the last '}' to isolate the JSON object,
    ignoring any markdown or hallucinated text outside those bounds.
    """
    # Remove markdown code blocks first
    clean_text = re.sub(r'```(?:json)?', '', text)
    clean_text = clean_text.replace('```', '').strip()

    start = clean_text.find("{")
    end = clean_text.rfind("}") # Find the LAST occurrence
    
    if start == -1 or end == -1 or end < start:
        return None

    return clean_text[start:end+1]

def sanitize_json_string(json_text: str):
    # 1. Handle Llama's specific trailing comma/hallucination before the last brace
    # This replaces things like 'null, end with }' with 'null }'
    json_text = re.sub(r',\s*end\s*.*?\s*}', '}', json_text)
    
    # 2. Replace null with empty string (as per your requirement)
    # We use regex to ensure we only replace the value, not keys containing 'null'
    json_text = re.sub(r':\s*null', ': ""', json_text)

    return json_text

def extract_intent(user_command: str, agent: str) -> dict:
    # Adding "JSON Output:" to the end of the prompt helps Llama start correctly
    prompt = f"""
You are an intent extraction engine.

STRICT RULES:
- Return ONLY one valid JSON object.
- No markdown.
- No explanation.
- No extra text.

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

JSON Output:"""

    response = call_llm(prompt, agent)

    # Clean the response string
    json_text = extract_complete_json(response)

    if not json_text:
        return {
            "intent": "PARSE_ERROR",
            "raw_response": response
        }

    json_text = sanitize_json_string(json_text)

    try:
        return json.loads(json_text)
    except Exception:
        # Fallback: if json.loads fails, return the error and the text we tried to parse
        return {
            "intent": "PARSE_ERROR",
            "raw_response": response,
            "cleaned_attempt": json_text
        }