from byte_8_ai.services.arxiv_cl import search_by_id, search_by_topic

for p in search_by_id("1706.03762"):
    print(p.arxiv_id, "|", p.title, "|", p.pdf_url)

print("dummy id: ", search_by_id("9999.99999"))

for p in search_by_topic("KV cache Compression", max_results=5):
    print(p.arxiv_id, "|", p.title)