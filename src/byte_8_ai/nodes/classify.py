import re

from byte_8_ai.state import AgentState

OLD_ID = re.compile(r"\b(\d{4}\.\d{4,5})(v\d+)?\b")
NEW_ID = re.compile(r"\b([a-z\-]+(?:\.[A-Z]{2})?/\d{7})\b")


def extract_arxiv_id(text: str):
    match = NEW_ID.search(text)
    if match:
        return match.group(1)

    match = OLD_ID.search(text)
    if match:
        return match.group(1)

    return None


def classify_input(state: AgentState):
    text = state["user_input"].strip()
    if not text:
        return {"errors": ["User input is empty. need a valid input"]}

    arxiv_id = extract_arxiv_id(text)
    if arxiv_id:
        return {"mode": "id", "arxiv_id": arxiv_id}
    return {"mode": "topic", "search_query": text}
