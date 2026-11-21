from ragas import evaluate, EvaluationDataset
from ragas.metrics import Faithfulness, ResponseRelevancy, LLMContextPrecisionWithoutReference
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from answer import retriever, chain, llm, rerank, NO_INFO
from graph import app as agent
from langchain_ollama import ChatOllama
from vectordb import embeddings
from tests import TESTS
from ragas import RunConfig
from langchain_groq import ChatGroq

QUESTIONS = [q for q, _ in TESTS]
print("Questions:", len(QUESTIONS)) 

def run_simple(q):
    docs = rerank(q, retriever.invoke(q))
    context = "\n\n".join(d.page_content for d in docs)
    answer = chain.invoke({"context": context, "question": q, "no_info": NO_INFO})
    return answer, [d.page_content for d in docs]

def run_agent(q):
    r = agent.invoke({"question": q})
    return r["answer"], [d.page_content for d in r.get("docs", [])]

def build_dataset(run_fn):
    rows = []
    for q in QUESTIONS:
        answer, contexts = run_fn(q)
        rows.append({"user_input": q, "response": answer, "retrieved_contexts": contexts})
    return EvaluationDataset.from_list(rows)
# groq_llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)

JUDGE_NAME = "8b"
judge = LangchainLLMWrapper(ChatOllama(model="qwen3:8b", temperature=0, reasoning=False))
# judge = LangchainLLMWrapper(groq_llm)               # strong judge from Groq
judge_emb = LangchainEmbeddingsWrapper(embeddings)  # embeddings stay local (Ollama)
metrics = [Faithfulness(), ResponseRelevancy(strictness=1), LLMContextPrecisionWithoutReference()]
run_config = RunConfig(timeout=600, max_workers=2)
# for name, fn in [("SIMPLE", run_simple), ("AGENT", run_agent)]:
for name, fn in [("AGENT", run_agent)]:
    print(f"\n=== {name} ===")
    result = evaluate(build_dataset(fn), metrics=metrics, llm=judge,
                      embeddings=judge_emb, run_config=run_config)
    print(result)
    result.to_pandas().to_csv(f"ragas_{name.lower()}_{JUDGE_NAME}.csv", index=False)
