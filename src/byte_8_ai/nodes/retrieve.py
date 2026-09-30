import arxiv

from byte_8_ai.services.arxiv_cl import search_by_id, search_by_topic
from byte_8_ai.state import AgentState


def fetch_paper(state: AgentState):
    if state["mode"] == "id":
        target = state["arxiv_id"]
        search = search_by_id
    else:
        target = state["search_query"]
        search = search_by_topic

    try:
        results = search(target)
    except arxiv.ArxivError as e:
        return {"candidates": [], "errors": [f"request failed for {target}: {e} "]}
    if not results:
        return {"candidates": [], "errors": [f"No papers found on arxiv for {target}"]}
    return {"candidates": results}
