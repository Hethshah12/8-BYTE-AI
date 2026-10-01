import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

PROJECT_FOLDER = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_FOLDER / ".env")


def _required(name: str):
    """Going through the env vars and checking if they exist and are valid, if not raise error"""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} not set in .env file")
    return value


def get_llm(role: str):
    """so what i've thought is
    for summarization and stuff we can use google genai, but for reasoning QA we can use groq, the idea behind this was google genai has a longer and better context window, but groq is better for reasoning and hence we can use both of them for different tasks
    """
    if role == "summarize":
        _required("GOOGLE_API_KEY")
        primary = ChatGoogleGenerativeAI(
            model=_required("GEMINI_MODEL"), temperature=0, max_retries=2
        )  # setting temperature to 0 for a deterministic output, as we do not want a different summary and apart from that we do not want to waste tokens on retries, also setting max_Retries to 2

        backup_model = os.getenv("GEMINI_FALLBACK_MODEL")
        if backup_model:
            backup = ChatGoogleGenerativeAI(
                model=backup_model, temperature=0, max_retries=2
            )
            return primary.with_fallbacks([backup])
        return primary

    if role == "qa":
        _required("GROQ_API_KEY")
        return ChatGroq(model=_required("GROQ_MODEL"), temperature=0, max_retries=2)
    raise ValueError(f"Unknown role: {role}, Expecting one of ['summarize', 'qa']")
