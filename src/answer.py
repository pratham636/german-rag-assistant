from dotenv import load_dotenv
from langsmith import traceable
load_dotenv()
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from vectordb import load_db
from hybrid import get_hybrid_retriever
from transformers import AutoTokenizer          
from rerank import rerank
from config import (TOP_K, SCORE_THRESHOLD, MAX_CONTEXT_TOKENS, NO_INFO,
                    TOKEN_OVER, LLM_MODEL, TOKENIZER_MODEL)
from config import OLLAMA_BASE_URL

db = load_db()
retriever = get_hybrid_retriever(db, k=TOP_K)
llm = ChatOllama(model=LLM_MODEL, temperature=0, reasoning=False,
                 base_url=OLLAMA_BASE_URL)
# llm = ChatOllama(model=LLM_MODEL, temperature=0, reasoning=False)
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_MODEL)   

PROMPT = ChatPromptTemplate.from_template(
    """Beantworte die Frage NUR mit dem Kontext. Wenn die Antwort fehlt, sag: "{no_info}"
Antworte kurz auf Deutsch und nenne die Quelle, z.B. [1].

Kontext:
{context}

Frage: {question}
Antwort:"""
)
chain = PROMPT | llm | StrOutputParser()

def count_tokens(text):
    return len(tokenizer.encode(text, add_special_tokens=False))  

@traceable(name="German RAG")
def ask(question):
    best = db.similarity_search_with_relevance_scores(question, k=1)
    if not best or best[0][1] < SCORE_THRESHOLD:
        return NO_INFO, []

    selected, total, truncated = [], 0, False
    docs = rerank(question, retriever.invoke(question), top_n=4)
    for d in docs:
        n = count_tokens(d.page_content)
        if total + n > MAX_CONTEXT_TOKENS:
            truncated = True
            break
        selected.append(d)
        total += n
    if not selected:
        return TOKEN_OVER, []

    context = "\n\n".join(
        f"[{i+1}] {d.metadata['source']} S.{d.metadata['page']}:\n{d.page_content}"
        for i, d in enumerate(selected))
    answer = chain.invoke({"context": context, "question": question, "no_info": NO_INFO})
    if truncated:
        answer += f"\n\n Kontext gekürzt: {len(selected)} von {len(docs)} Chunks genutzt ({total}/{MAX_CONTEXT_TOKENS} Tokens)."
    sources = [f"[{i+1}] {d.metadata['source']} S.{d.metadata['page']}" for i, d in enumerate(selected)]
    print(f"   (used {len(selected)} chunks, {total} tokens)")
    return answer, sources

if __name__ == "__main__":
    for q in ["Wie oft darf man eine Prüfung wiederholen?",
              "Wo ist das Centrum für Europarecht?",
              "Was ist die Hauptstadt von Frankreich?"]:
        answer, sources = ask(q)
        print(f"\nQ: {q}\nA: {answer}")
        for s in sources:
            print("  ", s)

        print("\n \n")