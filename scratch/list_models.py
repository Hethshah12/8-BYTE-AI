from google import genai
from groq import Groq

import byte_8_ai.config  # noqa: F401  (loads .env)

gemini_client = genai.Client()  # kept in a variable, so it stays open while we loop
print("Gemini models (flash only):")
for m in gemini_client.models.list():
    if "flash" in m.name:
        print("  ", m.name)

groq_client = Groq()
print("\nGroq models:")
for m in groq_client.models.list().data:
    print("  ", m.id)