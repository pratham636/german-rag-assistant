from sentence_transformers import CrossEncoder
from langchain_core.runnables import RunnableLambda
import torch
from config import RERANK_MODEL, RERANK_TOP_N
from config import RERANK_MODEL, RERANK_TOP_N, RERANK_DEVICE
reranker = CrossEncoder(RERANK_MODEL, device=RERANK_DEVICE)

device = "cuda" if torch.cuda.is_available() else "cpu"

# reranker = CrossEncoder(RERANK_MODEL, device=device)   # multilingual, good for German

def rerank(question, docs, top_n=RERANK_TOP_N):
    if not docs:
        return []
    scores = reranker.predict([(question, d.page_content) for d in docs],show_progress_bar=False)
    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    return [d for d, _ in ranked[:top_n]]

def get_rerank_retriever(base_retriever, top_n=4):
    """Hybrid -> rerank, usable like a normal retriever (.invoke)."""
    return RunnableLambda(lambda q: rerank(q, base_retriever.invoke(q), top_n))

def rerank_with_scores(question, docs, top_n=4):
    if not docs:
        return []
    scores = reranker.predict([(question, d.page_content) for d in docs],
                              show_progress_bar=False)
    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    return ranked[:top_n]

if __name__ == "__main__":
    from vectordb import load_db
    from hybrid import get_hybrid_retriever
    r = get_rerank_retriever(get_hybrid_retriever(load_db(), k=5))
    for d in r.invoke("Was muss man nach der Masterarbeit im Doppelmaster machen?"):
        print(d.metadata["source"], "S.", d.metadata["page"], "|", d.page_content[:80])