from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from config import DATA_DIR
BASE_DIR = Path(__file__).parent.parent   # src/ -> RAG/
DATA_DIR = BASE_DIR / "data"

def load_pdfs():
    docs = []
    for pdf in DATA_DIR.glob("*.pdf"):
        pages = PyPDFLoader(str(pdf)).load()
        for p in pages:
            p.metadata["source"] = pdf.name
            p.metadata["page"] = p.metadata.get("page", 0) + 1
        docs.extend(pages)
        print(f"{pdf.name}: {len(pages)} pages")
    return docs

if __name__ == "__main__":
    docs = load_pdfs()
    print(f"\nTotal: {len(docs)} pages")
    print("\n--- Example page ---")
    print(docs[5].metadata)
    print(docs[5].page_content[:500])