import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from graph import app as rag_graph
from logger import log

api = FastAPI(
    title="German RAG Assistant",
    description="Answers questions about University of Passau study and exam regulations.",
    version="1.0",
)

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500,
                          examples=["Wie oft darf man eine Prüfung wiederholen?"])

class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    blocked: bool
    latency_s: float

@api.get("/health")
def health():
    return {"status": "ok"}

@api.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    start = time.time()
    try:
        result = rag_graph.invoke({"question": req.question})
    except Exception as e:
        log.error("api | error | %s", e)
        raise HTTPException(status_code=500, detail="Internal error while answering.")
    latency = round(time.time() - start, 2)
    log.info("api | answered in %.2fs", latency)
    return AskResponse(
        answer=result["answer"],
        sources=result.get("sources", []),
        blocked=result.get("blocked", False),
        latency_s=latency,
    )