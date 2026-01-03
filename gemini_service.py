from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def call_gemini(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    if hasattr(response, "text") and response.text:
        return response.text.strip()

    return response.candidates[0].content.parts[0].text.strip()
