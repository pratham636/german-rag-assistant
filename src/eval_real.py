from hybrid import get_hybrid_retriever
from rerank import get_rerank_retriever
from vectordb import load_db
from graph import ask
from tests import REAL_TESTS, REAL_NO_ANSWER
from config import TOP_K

K = 4
db = load_db()
reranked = get_rerank_retriever(get_hybrid_retriever(db, k=TOP_K))

print("=== Retrieval: answerable real questions ===")
hits = 0
for q, expected in REAL_TESTS:
    docs = reranked.invoke(q)[:K]
    found = any(e.lower() in d.page_content.lower() for d in docs for e in expected)
    hits += found
    print(f"{'OK  ' if found else 'MISS'} | {q}")
print(f"Hit rate: {hits}/{len(REAL_TESTS)}")

print("\n=== Honesty: questions with no answer in the documents ===")
honest = 0
for q in REAL_NO_ANSWER:
    answer, _ = ask(q)
    said_no = "keine informationen" in answer.lower()
    honest += said_no
    print(f"{'OK      ' if said_no else 'INVENTED'} | {q}\n         -> {answer[:120]}")
print(f"Correctly said 'no info': {honest}/{len(REAL_NO_ANSWER)}")