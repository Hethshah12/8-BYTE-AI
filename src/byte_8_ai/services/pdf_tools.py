from pathlib import Path

import pymupdf
import pymupdf4llm
import requests


def download_pdf(url: str, dest: Path, timeout: int = 60):
    if dest.exists():
        return dest
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()

    if not resp.content.startswith(b"%PDF"):
        raise ValueError(f"URL did not return a PDF: {url}")

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(resp.content)

    return dest


def pdf_to_markdown(path: Path, max_pages: int = 50):
    with pymupdf.open(path) as doc:
        n_pages = min(len(doc), max_pages)
        markdown = pymupdf4llm.to_markdown(
            doc, pages=list(range(n_pages)), use_ocr=False
        )
    return markdown, n_pages
