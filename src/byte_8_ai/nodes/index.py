"""
FLOW
1) read the markdown that is parsed and saved
2) removal of useless sections like references and stuff
3) split the text into sections and headings
4) for long sections we cut them into overlapping chunks to have a precontext of the previous chunk and reference to the next chunk
5) store all of these chunks in db, with the section name for quick searching and retrieval

"""

import re
from pathlib import Path

from byte_8_ai.services.vector_store import get_collection
from byte_8_ai.state import AgentState

CHUNK_WORDS = 150
OVERLAP_WORDS = 40

REFERENCES = re.compile(
    r"(\*\*references\*\*|^#+\s*\**references\**\s*$).*?(?=^#|\Z)",
    re.IGNORECASE | re.MULTILINE | re.DOTALL,
)


def remove_references(markdown: str):
    return REFERENCES.sub("\n\n", markdown)


def clean_heading(line: str):
    return line.strip("#*_ \t")


def split_into_sections(markdown: str):
    """return a list of all the sections"""
    sections = []
    title = "Front Matter"
    lines = []

    for line in markdown.splitlines():
        if line.startswith("#"):
            sections.append((title, "\n".join(lines)))
            title = clean_heading(line)
            lines = []
        else:
            lines.append(line)
    sections.append((title, "\n".join(lines)))

    return [(t, text) for t, text in sections if text.strip()]


def chunk_words(text: str, size: int = CHUNK_WORDS, overlap: int = OVERLAP_WORDS):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        chunks.append(" ".join(words[start : start + size]))
        if start + size >= len(words):
            break
        start += size - overlap
    return chunks


def index(state: AgentState):
    paper = state["selected_paper"]
    markdown = Path(state["parsed_path"]).read_text(encoding="utf-8")
    collection_name = "arxiv_" + paper.arxiv_id.replace("/", "_")
    collection = get_collection(collection_name)

    if collection.count() > 0:
        return {"collection_name": collection_name}
    ids, documents, metadata = [], [], []
    for section_title, section_text in split_into_sections(remove_references(markdown)):
        for chunk in chunk_words(section_text):
            n = len(ids)
            ids.append(f"{collection_name}-{n}")
            documents.append(f"Section: {section_title}\n\n\n{chunk}")
            metadata.append({"section": section_title, "chunk_index": n})

    if not documents:
        return {"errors": [f"no documents to index for {paper.arxiv_id}"]}

    collection.add(ids=ids, documents=documents, metadatas=metadata)
    return {"collection_name": collection_name}
