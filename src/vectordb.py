import time
from pathlib import Path
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from load import load_pdfs
from chunk import split_docs
from langchain_ollama import OllamaEmbeddings

load_dotenv()

BASE_DIR = Path(__file__).parent.parent
DB_DIR = str(BASE_DIR / "chroma_db")

# embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
embeddings = OllamaEmbeddings(model="qwen3-embedding:0.6b")

def build_db(chunks, batch_size=50):
    db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings,collection_metadata={"hnsw:space": "cosine"},)
    for i in range(0, len(chunks), batch_size):
        db.add_documents(chunks[i:i + batch_size])
        print(f"Added {min(i + batch_size, len(chunks))}/{len(chunks)}")
        # time.sleep(1)   # avoid Gemini rate limit
    return db

def load_db():
    return Chroma(persist_directory=DB_DIR, embedding_function=embeddings,collection_metadata={"hnsw:space": "cosine"},)

def search(db, question, k=4):
    results = db.similarity_search_with_relevance_scores(question, k=k)
    print(f"\nQ: {question}")
    for doc, score in results:
        preview = doc.page_content[:100].replace("\n", " ")
        print(f"  {score:.3f} | {doc.metadata['source']} S.{doc.metadata['page']} | {preview}...")

if __name__ == "__main__":
    if Path(DB_DIR).exists():
        print("Loading existing DB...")
        db = load_db()
    else:
        print("Building new DB...")
        db = build_db(split_docs(load_pdfs()))

    search(db, "Wie oft darf man eine Prüfung wiederholen?")
    search(db, "Wie viele ECTS hat der LL.B. Legal Tech?")
    search(db, "Was ist die Hauptstadt von Frankreich?")