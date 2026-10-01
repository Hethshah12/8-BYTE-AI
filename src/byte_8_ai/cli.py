"""Usage:
    uv run python -m byte_8_ai.cli <id>
    uv run python -m byte_8_ai.cli <topic>


"""
import json
import sys
from pathlib import Path

from langchain_core.messages import HumanMessage

from byte_8_ai.graph import create_graph, create_qa_graph

BRIEFING_FOLDER=Path(__file__).resolve().parents[2]/"data"/"briefings"

def save_briefing(state):
    paper=state["selected_paper"]
    output={
        "paper":paper.model_dump(mode="json"),
        "source_quality":state.get("parsed_quality"),
        "briefing":state["briefing"].model_dump(),
    
    }
    BRIEFING_FOLDER.mkdir(parents=True, exist_ok=True)
    path=BRIEFING_FOLDER/(paper.arxiv_id.replace("/", "_")+".json")
    path.write_text(json.dumps(output, indent=2, ensure_ascii=True), encoding="utf-8")
    return path

def print_briefing(state):
    paper, b=state["selected_paper"],state["briefing"]
    print(f"\n -----{paper.title}-----")
    print(f"{', '.join(paper.authors)} | arxiv {paper.arxiv_id}| {paper.published.date()}")
    print(f"https://arxiv.org/abs/{paper.arxiv_id}\n")
    print("WHY IT MATTERS\n" + b.why_it_matters + "\n")
    print("PROBLEM\n" + b.problem + "\n")
    for title, items in [
        ("METHOD", b.method),
        ("KEY FINDINGS", b.key_findings),
        ("LIMITATIONS", b.limitations),
        ("SUGGESTED QUESTIONS", b.follow_up_questions),
    ]:
        print(title)
        for item in items:
            print(f"  - {item}")
        print()

def main():
    if len(sys.argv)<2:
        print(__doc__)
        return

    state=create_graph().invoke({"user_input":" ".join(sys.argv[1:])})

    for error in state.get("errors", []):
        print(f"[!]{error}")

    if "briefing" in state:
        print_briefing(state)
        print(f"Briefing saved to {save_briefing(state)}")

    if "collection_name" not in state:
        return 

    qa_graph=create_qa_graph()
    while True:
        question=input("\n Ask any questions related to the paper (To quit just hit Enter)").strip()
        if not question:
            break
        messages=state.get("messages", [])+[HumanMessage(question)]
        state=qa_graph.invoke({**state, "messages":messages})
        print(state["messages"][-1].content)

if __name__=="__main__":
    main()
