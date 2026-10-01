from byte_8_ai.services.vector_store import get_collection

col = get_collection("arxiv_1706.03762")
q = "what is the computational complexity of the self-attention model?"
r = col.query(query_texts=[q], n_results=6)
for doc, meta, dist in zip(r["documents"][0], r["metadatas"][0], r["distances"][0]):
    print(f"\n{dist:.3f}  {meta['section']}\n{doc[:300]}")