from typing import TypedDict, List
from langchain_core.documents import Document
from langgraph.graph import StateGraph, START, END
from answer import (db, retriever, chain, llm, count_tokens, rerank,
                    SCORE_THRESHOLD, MAX_CONTEXT_TOKENS, NO_INFO, TOKEN_OVER)

MAX_RETRIES = 2

# ---------- State ----------
class RAGState(TypedDict):
    question: str        # original question (used for the answer)
    search_query: str    # query used for search (can be rewritten)
    on_topic: bool
    docs: List[Document]
    candidates: List[Document]
    retries: int
    answer: str
    sources: List[str]

# ---------- Nodes ----------
def check_topic(state: RAGState):
    best = db.similarity_search_with_relevance_scores(state["question"], k=1)
    on_topic = bool(best) and best[0][1] >= SCORE_THRESHOLD
    return {"on_topic": on_topic, "search_query": state["question"], "retries": 0}

def no_info(state: RAGState):
    return {"answer": NO_INFO, "sources": []}

def retrieve(state: RAGState):
    q = state["search_query"]
    docs = rerank(q, retriever.invoke(q), top_n=4)
    selected, total = [], 0
    for d in docs:
        n = count_tokens(d.page_content)
        if total + n > MAX_CONTEXT_TOKENS:
            break
        selected.append(d)
        total += n
    print(f"   [retrieve] query: {q} -> {len(selected)} chunks")
    update = {"docs": selected}
    if state.get("retries", 0) == 0:      # only save candidates from the first search
        update["candidates"] = selected
    return update

def grade_docs(state: RAGState):
    relevant = []
    for d in state["docs"]:
        prompt = (
            f"Frage: {state['question']}\n\n"
            f"Dokument:\n{d.page_content}\n\n"
            "Enthält das Dokument Informationen, die zur Beantwortung der Frage helfen? "
            "Antworte nur mit 'ja' oder 'nein'."
        )
        verdict = llm.invoke(prompt).content.strip().lower()
        if verdict.startswith("ja"):
            relevant.append(d)
    print(f"   [grade] {len(relevant)}/{len(state['docs'])} chunks relevant")
    return {"docs": relevant}

def rewrite_question(state: RAGState):
    prompt = (
        "Die folgende Suchanfrage hat keine passenden Dokumente gefunden.\n"
        f"Ursprüngliche Frage: {state['question']}\n"
        f"Letzte Suchanfrage: {state['search_query']}\n\n"
        "Formuliere eine NEUE, kürzere Suchanfrage mit anderen Fachbegriffen "
        "aus deutschen Studien- und Prüfungsordnungen. Gib nur die Suchanfrage aus."
    )
    new_query = llm.invoke(prompt).content.strip()
    print(f"   [rewrite] {new_query}")
    return {"search_query": new_query, "retries": state["retries"] + 1}
def fallback(state: RAGState):
    print("   [fallback] no chunk passed grading -> using top reranked chunks")
    return {"docs": state["candidates"]}

def generate(state: RAGState):
    docs = state["docs"]
    if not docs:
        return {"answer": TOKEN_OVER, "sources": []}
    context = "\n\n".join(
        f"[{i+1}] {d.metadata['source']} S.{d.metadata['page']}:\n{d.page_content}"
        for i, d in enumerate(docs))
    answer = chain.invoke({"context": context, "question": state["question"], "no_info": NO_INFO})
    sources = [f"[{i+1}] {d.metadata['source']} S.{d.metadata['page']}" for i, d in enumerate(docs)]
    return {"answer": answer, "sources": sources}

# ---------- Routing ----------
def route_topic(state: RAGState):
    return "retrieve" if state["on_topic"] else "no_info"

def route_after_grade(state: RAGState):
    if state["docs"]:
        return "generate"
    if state["retries"] < MAX_RETRIES:
        return "rewrite_question"
    return "fallback"

# ---------- Build ----------
graph = StateGraph(RAGState)
graph.add_node("check_topic", check_topic)
graph.add_node("no_info", no_info)
graph.add_node("retrieve", retrieve)
graph.add_node("grade_docs", grade_docs)
graph.add_node("rewrite_question", rewrite_question)
graph.add_node("fallback", fallback)                
graph.add_node("generate", generate)

graph.add_edge(START, "check_topic")
graph.add_conditional_edges("check_topic", route_topic,
                            {"retrieve": "retrieve", "no_info": "no_info"})
graph.add_edge("retrieve", "grade_docs")
graph.add_conditional_edges("grade_docs", route_after_grade,
                            {"generate": "generate",
                             "rewrite_question": "rewrite_question",
                             "no_info": "no_info","fallback": "fallback"})
graph.add_edge("fallback", "generate") 
graph.add_edge("rewrite_question", "retrieve")
graph.add_edge("generate", END)
graph.add_edge("no_info", END)

app = graph.compile()

def ask(question):
    result = app.invoke({"question": question})
    return result["answer"], result["sources"]

if __name__ == "__main__":
    print(app.get_graph().draw_mermaid())
    for q in ["Wie oft darf man eine Prüfung wiederholen?",
              "Was passiert, wenn man eine Frist aus Gründen nicht einhalten kann, die man nicht zu vertreten hat?",
              "Was ist die Hauptstadt von Frankreich?"]:
        print(f"\n=== {q}")
        answer, sources = ask(q)
        print(f"A: {answer}")
        for s in sources:
            print("  ", s)