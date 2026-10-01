"""
Flow
1) Take question from user state["messages"]
2)find the 4 closest chunks in the paper ( choosing k to be 4)
3)even tho the closest chunk will be far away, we can choose to put "Not in the paper" reliability is the key to such models and hence we can avoid them 
4)else we can ask llm to choose to answer only using the text in the chunks

"""
import groq
from langchain_core.messages import AIMessage

from byte_8_ai.config import get_llm
from byte_8_ai.services.vector_store import get_collection
from byte_8_ai.state import AgentState

TOP_K=4
MAX_DISTANCE=0.75
NOT_IN_PAPER="Couldn't be found in the paper"

SYSTEM_PROMPT=f"""
You answer questions about the research paper

RULES:
1)Use only the excerpts below, do not use any of the outside knowledge
2)After each claim, cite the sections in brackets eg: [3.2 Attention].
3)If the excerpts do not contain the answer, reply exactly : "{NOT_IN_PAPER}"
4)keep the answers short and precisely to the point: 2-5 sentences.
"""

def qa(state: AgentState):
    question=state["messages"][-1].content 
    collection=get_collection(state["collection_name"])

    results=collection.query(query_texts=[question], n_results=TOP_K)
    chunks=results["documents"][0]
    distances=results["distances"][0]
    sections=[m["section"] for m in results["metadatas"][0]]
    sources=", ".join(f"{s} ({d:.2f})" for s, d in zip(sections,distances))


    #if nothing is in the paper
    if not chunks or distances[0]>MAX_DISTANCE:
        return {"messages": [AIMessage(NOT_IN_PAPER)]}

    excerpts="\n\n---\n\n".join(chunks)
    messages=[("system",SYSTEM_PROMPT), ("human", f"EXCERPTS:\n{excerpts}\n\nQUESTION:{question}")]

    #llm's decision whether to answer the question or not based on the excerpts
    try:
        answer=get_llm("qa").invoke(messages).text
    except groq.APIError as e:
        return{
            "messages":[AIMessage("Sorry, The qa model is not available")], "errors":[f"QA failed {e}"]
        } 
    return {"messages": [AIMessage(f"{answer} \n\nSources: {sources}")]}