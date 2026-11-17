# Results – German RAG Assistant (Phase 1)

## Setup

| Part | Choice |
| --- | --- |
| Documents | 10 German PDFs from University of Passau (study and exam regulations, module catalogue, exam announcement, building directory, English study guide) |
| Loader | PyPDFLoader, metadata: file name + page |
| Chunking | RecursiveCharacterTextSplitter, 800 chars, 150 overlap |
| Embeddings | `qwen3-embedding:0.6b` (Ollama, local) |
| Vector DB | Chroma, cosine distance |
| Keyword search | BM25 with German tokenizer |
| Reranker | `BAAI/bge-reranker-v2-m3` (cross-encoder, local) |
| LLM | `qwen3.5:4b` (Ollama, local) |
| Observability | LangSmith |

## Retrieval evaluation

Test set: 25 questions (German + English) with expected text in the correct chunk.
Metric: hit rate = correct chunk among the top 4 results.

| Version | Hit rate |
| --- | --- |
| Vector search only (baseline) | 76% (19/25) |
| + removed table-of-contents chunks | 80% (20/25) |
| + hybrid search (BM25 + vector) | 88% (22/25) |
| **+ cross-encoder reranking** | **92% (23/25)** |

What fixed what:
- **Hybrid search** fixed exact-name questions, e.g. "Centrum für Europarecht" and "zurücktreten" (found the exam announcement through the exact word).
- **Reranking** fixed "right PDF, wrong chunk" cases, e.g. the Masterarbeit defence in the double master's regulations.

Off-topic detection: relevant questions score ≥ 0.43, off-topic questions ≤ 0.26 → threshold set to 0.35.

## Remaining misses

1. **"Was regelt § 4 …?"** – The § number and its title were mainly in the table of contents. In the body text, § number and title are often on separate lines or in different chunks. Possible fix: extract § numbers as metadata during chunking.
2. **"Was passiert, wenn man eine Frist … nicht zu vertreten hat?"** – Vague question; many similar deadline rules exist across several regulations, so retrieval returns related but not the exact rule.

## Findings

- **Table-of-contents chunks** ("§ 27 Ziel … ……") ranked highest for some questions because they contain many keywords but no content. Filtering chunks with many dot leaders improved the hit rate from 76% to 80%.
- **Hyphenated line breaks** in the PDFs ("angemes- sene", "Staats -prüfung") break words. This hurts keyword search and exact-match tests. Expected test texts were chosen without broken words.
- **Correct retrieval, wrong answer:** for "Wo ist das Centrum für Europarecht?" the right chunk was retrieved, but the 4B model answered "Ludwigstraße 8" instead of "Leopoldstraße 4". The building directory is a list, and the small model mixed up which bullet belongs to which building. → Hit rate alone is not enough; answer quality must be evaluated too.
- **Too much context confuses a small model:** with ~15 chunks (~2,900 tokens), answers mixed rules from different programmes. Reranking down to 4 chunks gave shorter, more focused context.
- **Embedding rate limits:** the Gemini free tier (100 requests/min) was too slow for ~1,000 chunks. Switching to a local embedding model removed the limit and keeps documents on the machine.
- **Chroma distance:** the default L2 distance produced negative relevance scores with Qwen embeddings; switching the collection to cosine fixed it.

## Next steps

- LangGraph agent (document grading, query rewriting)
- Answer evaluation with RAGAS (faithfulness, answer relevancy)
- § numbers as metadata for legal documents
- FastAPI + Docker
