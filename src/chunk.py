from langchain_text_splitters import RecursiveCharacterTextSplitter
from load import load_pdfs
from config import CHUNK_SIZE, CHUNK_OVERLAP
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

def split_docs(docs, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    for i, c in enumerate(chunks):
        c.metadata["chunk_id"] = i
    chunks = [c for c in chunks if c.page_content.count("....") < 3]
    return chunks

if __name__ == "__main__":
    docs = load_pdfs()
    chunks = split_docs(docs)

    sizes = [len(c.page_content) for c in chunks]
    print(f"\n{len(docs)} pages -> {len(chunks)} chunks")
    print(f"Avg size: {sum(sizes)//len(sizes)} | min: {min(sizes)} | max: {max(sizes)}")

    for c in chunks[100:103]:
        print("\n---", c.metadata["source"], "S.", c.metadata["page"],c.metadata["chunk_id"], "---")
        print(c.page_content)