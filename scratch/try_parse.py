from datetime import datetime

from byte_8_ai.nodes.parse import parse
from byte_8_ai.state import PaperMetadata

paper = PaperMetadata(
    arxiv_id="1706.03762",
    title="Attention Is All You Need",
    authors=["Vaswani et al."],
    published=datetime(2017, 6, 12),
    abstract="The dominant sequence transduction models are based on ...",
    pdf_url="https://arxiv.org/pdf/1706.03762",
)

result = parse({"selected_paper": paper})
print(result)