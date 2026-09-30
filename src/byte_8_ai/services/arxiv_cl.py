import re

import arxiv

from byte_8_ai.state import PaperMetadata

_client = arxiv.Client(page_size=50, delay_seconds=50, num_retries=3)
_VERSION_SUFFIX = re.compile(r"v\d+$")


def _to_metadata(result: arxiv.Result):
    arxiv_id = _VERSION_SUFFIX.sub("", result.get_short_id())
    return PaperMetadata(
        arxiv_id=arxiv_id,
        title=result.title.strip(),
        authors=[author.name for author in result.authors],
        published=result.published,
        abstract=result.summary.strip(),
        pdf_url=result.pdf_url,
        categories=result.categories,
    )


def search_by_id(arxiv_id: str):
    search = arxiv.Search(id_list=[arxiv_id])
    return [_to_metadata(r) for r in _client.results(search)]


def search_by_topic(query: str, max_results: int = 10):
    search = arxiv.Search(query=query, max_results=max_results)
    return [_to_metadata(r) for r in _client.results(search)]
