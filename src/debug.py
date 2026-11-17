from vectordb import load_db
from hybrid import get_hybrid_retriever
from tests import TESTS, OUT_OF_SCOPE
from rerank import get_rerank_retriever
K = 4

def is_found(expected, docs):
    exp = expected if isinstance(expected, list) else [expected]
    return any(e.lower() in d.page_content.lower() for d in docs for e in exp)

def hit_rate(retriever, name):
    print(f"\n=== {name} ===")
    hits, misses = 0, []
    for question, expected in TESTS:
        docs = retriever.invoke(question)[:K]
        found = is_found(expected, docs)
        print(f"{'OK  ' if found else 'MISS'} | {question}")
        if found:
            hits += 1
        else:
            misses.append((question, docs))
    print(f"{name} hit rate: {hits}/{len(TESTS)} = {hits/len(TESTS):.0%}")
    return misses

def show_misses(misses, name):
    print(f"\n=== {name}: why did these fail? ===")
    for question, docs in misses:
        print(f"\nQ: {question}")
        for d in docs:
            preview = d.page_content[:90].replace("\n", " ")
            print(f"  {d.metadata['source']} S.{d.metadata['page']} | {preview}")

def check_threshold(db):
    print("\n=== Scores: good vs off-topic ===")
    good = [db.similarity_search_with_relevance_scores(q, k=1)[0][1] for q, _ in TESTS]
    bad = [db.similarity_search_with_relevance_scores(q, k=1)[0][1] for q in OUT_OF_SCOPE]
    print(f"Good: min {min(good):.2f}, avg {sum(good)/len(good):.2f} | Off-topic: max {max(bad):.2f}")

if __name__ == "__main__":
    db = load_db()
    vector = db.as_retriever(search_kwargs={"k": K})
    hybrid = get_hybrid_retriever(db, k=K)

    v_misses = hit_rate(vector, "VECTOR")
    h_misses = hit_rate(hybrid, "HYBRID")

    reranked = get_rerank_retriever(get_hybrid_retriever(db, k=5))
    r_misses = hit_rate(reranked, "HYBRID + RERANK")
    
    show_misses(h_misses, "HYBRID")
    check_threshold(db)