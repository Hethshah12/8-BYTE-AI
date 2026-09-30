import pytest

from byte_8_ai.nodes.classify import classify_input, extract_arxiv_id


@pytest.mark.parametrize(
    "text, expected",
    [
        ("2401.12345", "2401.12345"),  # plain new-style ID
        ("1412.6980", "1412.6980"),  # 4-digit suffix (2007-2014)
        ("2401.12345v2", "2401.12345"),  # version dropped
        ("arXiv:2401.12345", "2401.12345"),  # prefix
        ("https://arxiv.org/abs/2401.12345", "2401.12345"),  # abs URL
        ("arxiv.org/pdf/2401.12345.pdf", "2401.12345"),  # pdf URL
        ("hep-th/9901001", "hep-th/9901001"),  # old style
        ("math.GT/0309136", "math.GT/0309136"),  # old style with subject class
        ("2024 advances in RAG", None),  # starts with digits, but a topic
        ("KV cache compression", None),  # plain topic
        ("12401.123456", None),  # digits too long on both sides
    ],
)
def test_extract_arxiv_id(text, expected):
    assert extract_arxiv_id(text) == expected


def test_classify_id_input():
    assert classify_input({"user_input": " arXiv:1706.03762 "}) == {
        "mode": "id",
        "arxiv_id": "1706.03762",
    }


def test_classify_topic_input():
    assert classify_input({"user_input": "2024 advances in RAG"}) == {
        "mode": "topic",
        "search_query": "2024 advances in RAG",
    }


def test_classify_empty_input():
    result = classify_input({"user_input": "   "})
    assert "errors" in result
    assert "mode" not in result
