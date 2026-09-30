import re

NEW_ID = re.compile(r"\b(\d{4}\.\d{4,5})(v\d+)?\b")
OLD_ID = re.compile(r"\b([a-z\-]+(?:\.[A-Z]{2})?/\d{7})\b")


def extract_arxiv_id(text: str) -> str | None:
    match=NEW_ID.search(text)
    if match:
        return match.group(1)
    match=OLD_ID.search(text)
    if match:
        return match.group(1)

    return None



# ── self-check: every line should print True ──
cases = [
    ("2401.12345", "2401.12345"),
    ("2401.12345v2", "2401.12345"),
    ("https://arxiv.org/abs/2401.12345", "2401.12345"),
    ("hep-th/9901001", "hep-th/9901001"),
    ("2024 advances in RAG", None),
    ("12401.123456", None),
]
for text, expected in cases:
    got = extract_arxiv_id(text)
    print(got == expected, repr(text), "->", repr(got))