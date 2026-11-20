import os
import sys
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector
from load import load_pdfs
from chunk import split_docs
from config import DATABASE_URL, COLLECTION, EMBED_MODEL, EMBED_DIM

load_dotenv()

CONNECTION = os.getenv("DATABASE_URL")
COLLECTION = "german_rag"
embeddings = OllamaEmbeddings(model="qwen3-embedding:0.6b")

def get_db(fresh=False):
    return PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION,
        connection=CONNECTION,
        use_jsonb=True,
        embedding_length=1024,
        pre_delete_collection=fresh,
    )

def build_db(chunks, batch_size=100):
    db = get_db(fresh=True)
    for i in range(0, len(chunks), batch_size):
        db.add_documents(chunks[i:i + batch_size])
        print(f"Added {min(i + batch_size, len(chunks))}/{len(chunks)}")
    return db

def load_db():
    return get_db()

def search(db, question, k=4):
    results = db.similarity_search_with_relevance_scores(question, k=k)
    print(f"\nQ: {question}")
    for doc, score in results:
        preview = doc.page_content[:100].replace("\n", " ")
        print(f"  {score:.3f} | {doc.metadata['source']} S.{doc.metadata['page']} | {preview}...")

if __name__ == "__main__":
    if "--build" in sys.argv:
        db = build_db(split_docs(load_pdfs()))
    else:
        db = load_db()
    search(db, "Wie oft darf man eine Prüfung wiederholen?")
    search(db, "Was ist die Hauptstadt von Frankreich?")