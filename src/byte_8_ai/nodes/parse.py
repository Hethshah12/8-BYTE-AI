"""
Flow of doing this is:
1)working out file space
2)Download PDF
3) turn that PDF into markdown
4)save the markdown text
"""

from pathlib import Path

import pymupdf
import requests

from byte_8_ai.services.pdf_tools import download_pdf, pdf_to_markdown
from byte_8_ai.state import AgentState, PaperMetadata

pf = Path(__file__).resolve().parents[3]
pdf_f = pf / "data" / "pdfs"
text_f = pf / "data" / "parsed"
MIN_CHAR_PER_PAGE = 200


def _fallback(paper: PaperMetadata, parsed_path: Path, reason: str):
    """Writing the abstract , so that the later nodes always read the same file, even if parsing fails"""
    parsed_path.parents.mkdir(parents=True, exist_ok=True)
    parsed_path.write_text(f"Abstract: \n\n{paper.abstract} \n\n", encoding="utf-8")
    return {
        "parsed_path": str(parsed_path),
        "parsed_quality": "abstract_only",
        "errors": [f"parse fallback ({paper.arxiv_id}): {reason}"],
    }


def parse(state: AgentState):
    paper = state["selected_paper"]
    safe_id = paper.arxiv_id.replace("/", "_")
    pdf_path = pdf_f / f"{safe_id}.pdf"
    parsed_path = text_f / f"{safe_id}.md"

    if paper.pdf_url is None:  # calling the fallback function in case of a url failure
        return _fallback(paper, parsed_path, "no pdf url")

    try:
        download_pdf(paper.pdf_url, pdf_path)
        markdown, n_pages = pdf_to_markdown(pdf_path)
    except (requests.RequestException, ValueError, pymupdf.FileDataError) as e:
        pdf_path.unlink(missing_ok=True)
        return _fallback(paper, parsed_path, f"download/parse failed: {e}")

    if n_pages == 0 or len(markdown.strip()) / n_pages < MIN_CHAR_PER_PAGE:
        return _fallback(paper, parsed_path, "very few charechters ")

    parsed_path.parent.mkdir(parents=True, exist_ok=True)
    parsed_path.write_text(markdown, encoding="utf-8")

    return {
        "pdf_path": str(pdf_path),
        "parsed_path": str(parsed_path),
        "parsed_quality": "full",
    }
