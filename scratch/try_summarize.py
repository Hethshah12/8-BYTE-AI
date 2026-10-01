from datetime import datetime

from byte_8_ai.nodes.summarize import summarize
from byte_8_ai.state import PaperMetadata

paper = PaperMetadata(
    arxiv_id="1706.03762",
    title="Attention Is All You Need",
    authors=["Ashish Vaswani", "Noam Shazeer"],
    published=datetime(2017, 6, 12),
    abstract="...",
)

result = summarize({
    "selected_paper": paper,
    "parsed_path": "data/parsed/1706.03762.md",
    "parsed_quality": "full",
})

if "briefing" in result:
    print(result["briefing"].model_dump_json(indent=2))
else:
    print(result)