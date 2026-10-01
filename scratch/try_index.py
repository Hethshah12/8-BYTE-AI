from datetime import datetime
from pathlib import Path

from byte_8_ai.nodes.index import index
from byte_8_ai.services.vector_store import get_collection
from byte_8_ai.state import PaperMetadata

paper = PaperMetadata(
    arxiv_id="1706.03762", title="Attention Is All You Need", authors=[],
    published=datetime(2017, 6, 12), abstract="...",
)
parsed = Path("data/parsed/1706.03762.md")

result = index({"selected_paper": paper, "parsed_path": str(parsed)})
print(result)
collection = get_collection(result["collection_name"])
print("chunks stored:", collection.count())

for question in [
    "How does multi-head attention work?",
    "What hardware was used for training?",
    "What is the recipe for chocolate cake?",
]:
    result = collection.query(query_texts=[question], n_results=3)
    print(f"\nQ: {question}")
    for meta, dist in zip(result["metadatas"][0], result["distances"][0]):
        print(f"   {dist:.3f}  {meta['section']}")