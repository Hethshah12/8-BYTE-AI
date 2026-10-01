from langgraph.graph import END, START, StateGraph
from byte_8_ai.nodes.index import index
from byte_8_ai.nodes.classify import classify_input
from byte_8_ai.nodes.parse import parse
from byte_8_ai.nodes.retrieve import fetch_paper
from byte_8_ai.state import AgentState

# dummy_paper = PaperMetadata(
#     arxiv_id="2401.12345",
#     title="Detection and Mitigation of Data poisoning in LLMS",
#     authors=["Heth Shah", "H Achyuth"],
#     published="2026-05-01T00:00:00Z",
#     abstract="This paper presents a novel approach to detect and mitigate data poisoning attacks in large language models (LLMs). We propose a multi-stage detection framework that leverages both statistical analysis and machine learning techniques to identify poisoned data points. Our mitigation strategy involves retraining the model with a curated dataset, effectively reducing the impact of poisoned data on model performance. Experimental results demonstrate the effectiveness of our approach in maintaining model accuracy while minimizing the influence of malicious inputs.",
#     pdf_url="https://arxiv.org/pdf/2401.12345.pdf",
#     categories=["cs.LG", "cs.CR"],
# )


def route_after_classify(state: AgentState):
    if state.get("errors"):
        return "invalid"
    return "fetch"


def route_after_fetch(state: AgentState):
    if not state.get("candidates"):
        return "no results"
    return "rank"


def summarize(state: AgentState):
    return {}


def rank(state: AgentState):
    return {"selected_paper": state["candidates"][0]}


# def parse(state: AgentState):
#     return {"parsed_path": "data/parsed/stub.md", "parsed_quality": "full"}


# def index(state: AgentState):
#     return {"collection_name": "stub_collection"}


# def fetch_paper(state: AgentState):
#     return {"candidates": [dummy_paper]}


# def classify_input(state: AgentState):
#     text = state["user_input"].strip()
#     if not text:
#         return {"errors": ["User input is empty. Please provide a valid input."]}
#     if text[0].isdigit():
#         return {"mode": "id", "arxiv_id": text}
#     return {"mode": "topic", "search_query": text}


def create_graph():
    g = StateGraph(AgentState)
    g.add_node("Classify_Input", classify_input)
    g.add_node("rank", rank)
    g.add_node("parse", parse)
    g.add_node("index", index)
    g.add_node("summarize", summarize)
    g.add_edge(START, "Classify_Input")
    g.add_edge("rank", "parse")
    g.add_edge("parse", "index")
    g.add_edge("index", "summarize")
    g.add_edge("summarize", END)
    g.add_node("Fetch_paper_metadata", fetch_paper)
    g.add_conditional_edges(
        "Classify_Input",
        route_after_classify,
        {"fetch": "Fetch_paper_metadata", "invalid": END},
    )
    g.add_conditional_edges(
        "Fetch_paper_metadata", route_after_fetch, {"rank": "rank", "no results": END}
    )
    g.add_edge("Fetch_paper_metadata", END)

    return g.compile()


if __name__ == "__main__":
    graph = create_graph()
    for text in ["2401.12345", "KV cache compression", "9999.99999", "  "]:
        final = graph.invoke({"user_input": text})
        print(f"\n--- input: {text!r}")
        for key, value in final.items():
            print(f"{key:16}, {value!r:.70}")
