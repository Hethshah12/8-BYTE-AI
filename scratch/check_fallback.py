import os

from byte_8_ai.config import get_llm

print("GEMINI_MODEL          =", os.getenv("GEMINI_MODEL"))
print("GEMINI_FALLBACK_MODEL =", os.getenv("GEMINI_FALLBACK_MODEL"))
print("summarize LLM type    =", type(get_llm("summarize")).__name__)