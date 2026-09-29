import operator
from datetime import datetime
from typing import Annotated, Literal, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from pydantic import BaseModel, Field

# os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
# print("Successfully set GOOGLE_API_KEY:", os.environ["GOOGLE_API_KEY"])
# os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY")

# Things that will be stored from the paper metadata
#Could have used a TypedDict but pydantic Basemodel, does both validation as well as serialization/deserialization to/from JSON.
class PaperMetadata(BaseModel):
    arxiv_id:str
    title:str
    authors:list[str]
    published:datetime
    abstract:str
    pdf_url:str
    categories:list[str]=Field(default_factory=list)


#Adding a response Briefing to the state, this wil use the data from paper arxiv directly in summarization instead of using the data understood from the LLM to re-type that can cause hallucination. This will be used in the summarization prompt to provide a more accurate summary of the paper.
class Briefing(BaseModel):
    why_it_matters: str= Field(description="A paragraph explaining why this paper is important and relevant to the user.")

    problem: str= Field(description="The problem that the paper is trying to solve")
    method: list[str]=Field(description="Describing the method/approach in bullet points")
    key_findings: list[str]=Field(min_length=1, description="The key findings of the paper in bullet points")

    limitations: list[str]=Field(description="The limitations of the paper in bullet points")
    follow_up_questions: list[str]=Field(description="Questions asked by the reader")

class AgentState(TypedDict, total=False):
    user_input: str
    mode :Literal["id", "topic"]
    arxiv_id:str
    search_query:str
    candidates:list[PaperMetadata]
    selected_paper:PaperMetadata
    pdf_path:str
    parsed_path:str
    parsed_quality: Literal["full", "abstract", "failed"]
    collection_name: str
    briefing: Briefing
    messages: Annotated[list[AnyMessage], add_messages]
    errors:Annotated[list[str], operator.add]

