from langgraph.graph import END, START, StateGraph

from byte_8_ai.nodes.classify import classify_input
from byte_8_ai.nodes.index import index
from byte_8_ai.nodes.parse import parse
from byte_8_ai.nodes.qa import qa
from byte_8_ai.nodes.retrieve import fetch_paper
from byte_8_ai.nodes.summarize import summarize
from byte_8_ai.state import AgentState

def route_after_classify(state: AgentState):
    if state.get("errors"):
        return "invalid"
    return "fetch"

def route_after_fetch(state: AgentState):
    if not state.get("candidates"):
        return "no results"
    return "rank"


def rank(state: AgentState):
    return {"selected_paper": state["candidates"][0]}

def create_qa_graph():
    g=StateGraph(AgentState)
    g.add_node("qa", qa)
    g.add_edge(START, "qa")
    g.add_edge("qa", END)
    return g.compile()

def create_graph():
    g = StateGraph(AgentState)
    g.add_node("Classify_Input", classify_input)
    g.add_node("Fetch_paper_metadata", fetch_paper)
    g.add_node("rank", rank)
    g.add_node("parse", parse)
    g.add_node("index", index)
    g.add_node("summarize", summarize)
    g.add_edge(START, "Classify_Input")
    g.add_conditional_edges(
            "Classify_Input",
            route_after_classify,
            {"fetch": "Fetch_paper_metadata", "invalid": END},
        )
    g.add_conditional_edges(
            "Fetch_paper_metadata", route_after_fetch, {"rank": "rank", "no results": END}
        )
    g.add_edge("Fetch_paper_metadata", END)

    g.add_edge("rank", "parse")
    g.add_edge("parse", "index")
    g.add_edge("index", "summarize")
    g.add_edge("summarize", END)
    
    
    return g.compile()


if __name__ == "__main__":
    graph = create_graph()
    for text in ["2401.12345", "KV cache compression", "9999.99999", "  "]:
        final = graph.invoke({"user_input": text})
        print(f"\n--- input: {text!r}")
        for key, value in final.items():
            print(f"{key:16}, {value!r:.70}")
