"""
General Flow
1)read/go through the paper (parse saved)
2)building the prompt: rules + paper metadata + paper text +user question
3)gemini does briefing
4)if answer is invalid -> we go again
"""

from pathlib import Path

from byte_8_ai.config import get_llm
from byte_8_ai.state import AgentState, Briefing

SYSTEM_PROMPT = """
You write executive briefings of research papers for busy engineers.
Rules:
1)Use only the paper text provided. There is no neccesity to add facts from outside it.
2)Be concrete and to the point: include minute details such as numbers, datasets and model names where the paper gives them.
3)Limitations are mandatory, prefer limitations that the author states themselves.
If the paper states none , list the most important ones you can see in its method or experiments, and start each of those with "inferred:"
4)Follow up questions should be ones this paper's text could plausibly answer
"""
MAX_CHARS = 300_000
ATTEMPTS = 2


def summarize(state: AgentState):
    paper = state["selected_paper"]
    text = Path(state["parsed_path"]).read_text(encoding="utf-8")
    note = ""
    if state.get("parsed_quality") == "abstract_only":
        note = (
            "\nNOTE: Only the abstract is available, not the entire paper ."
            "All the claims that are to be made should be from the abstract only."
        )

    user_prompt = (
        f"Title: {paper.title}\n"
        f"Authors: {', '.join(paper.authors)}\n"
        f"Published: {paper.published.date()}\n"
        f"{note}\n\n"
        f"PAPER TEXT:\n{text}"
    )
    messages = [("system", SYSTEM_PROMPT), ("human", user_prompt)]
    llm = get_llm("summarize").with_structured_output(Briefing)
    last_error = None
    for _ in range(ATTEMPTS):
        try:
            briefing = llm.invoke(messages)
            return {"briefing": briefing}
        except Exception as e:
            last_error = e

    return {"errors": [f"Summarize failed after {ATTEMPTS} attempts: {last_error}"]}
