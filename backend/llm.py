import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Main model first, backup model second
MODELS = [
    m for m in (os.getenv("GEMINI_MODEL"), os.getenv("GEMINI_FALLBACK_MODEL")) if m
]

RETRYABLE = (429, 500, 503, 504)   # "busy" or temporary errors
ATTEMPTS_PER_MODEL = 3


def ask_llm(prompt: str, system: str = "You are a helpful assistant.") -> str:
    last_error = None
    for model in MODELS:
        for attempt in range(ATTEMPTS_PER_MODEL):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system,
                        temperature=0.3,
                    ),
                )
                return response.text
            except APIError as e:
                if e.code not in RETRYABLE:
                    raise   # a real mistake (bad key, bad request): don't hide it
                last_error = e
                time.sleep(2 ** attempt)   # waits 1s, 2s, 4s
    raise last_error