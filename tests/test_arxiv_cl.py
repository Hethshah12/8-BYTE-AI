# from datetime import datetime, timezone

# import arxiv

# from byte_8_ai.services.arxiv_cl import _to_metadata


# def _fake_result(**overrides) -> arxiv.Result:
#     fields = dict(
#         entry_id="http://arxiv.org/abs/2401.12345v2",
#         title="  A Paper  ",
#         authors=[arxiv.Result.Author("Jane Doe"), arxiv.Result.Author("John Roe")],
#         published=datetime(2024, 1, 15, tzinfo=timezone.utc),
#         summary="The abstract.\n",
#         categories=["cs.CL", "cs.LG"],
#         links=[arxiv.Result.Link("http://arxiv.org/pdf/2401.12345v2", title="pdf")],
#     )
#     fields.update(overrides)
#     return arxiv.Result(**fields)


# def test_maps_all_fields():
#     meta = _to_metadata(_fake_result())
#     assert meta.arxiv_id == "2401.12345"  # version stripped
#     assert meta.title == "A Paper"  # whitespace stripped
#     assert meta.authors == ["Jane Doe", "John Roe"]
#     assert meta.abstract == "The abstract."
#     assert meta.pdf_url == "http://arxiv.org/pdf/2401.12345v2"
#     assert meta.categories == ["cs.CL", "cs.LG"]


# def test_missing_pdf_link_gives_none():
#     meta = _to_metadata(_fake_result(links=[]))
#     assert meta.pdf_url is None