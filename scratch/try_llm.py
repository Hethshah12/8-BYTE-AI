from byte_8_ai.config import get_llm

print("Gemini:", get_llm("summarize").invoke("Reply with only the word OK").text)
print("Groq:  ", get_llm("qa").invoke("Reply with only the word OK").text)