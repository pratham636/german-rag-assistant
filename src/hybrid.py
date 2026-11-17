import re
from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from vectordb import load_db

K = 4

def german_tokenize(text):
    # lowercase + split into words, keep §, numbers and umlauts
    return re.findall(r"§|\w+", text.lower())

def get_all_chunks(db):
    data = db.get()
    return [Document(page_content=t, metadata=m)
            for t, m in zip(data["documents"], data["metadatas"])]

def get_hybrid_retriever(db, k=K, weights=(0.5, 0.5)):
    chunks = get_all_chunks(db)
    bm25 = BM25Retriever.from_documents(chunks, preprocess_func=german_tokenize)
    bm25.k = k
    vector = db.as_retriever(search_kwargs={"k": k})
    return EnsembleRetriever(retrievers=[bm25, vector], weights=list(weights))

if __name__ == "__main__":
    db = load_db()
    retriever = get_hybrid_retriever(db)
    q = "Wie oft darf man eine Prüfung wiederholen?"
    for d in retriever.invoke(q):
        print(f"{d.metadata['source']} S.{d.metadata['page']} | {d.page_content[:90]}")