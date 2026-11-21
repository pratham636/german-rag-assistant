# Results – German RAG Assistant

All numbers below were measured on the final code unless stated otherwise.

## Setup

| Part | Choice |
| --- | --- |
| Documents | 10 German PDFs from the University of Passau (study and exam regulations, module catalogue, exam announcement, building directory, English study guide), ~320 pages |
| Chunking | RecursiveCharacterTextSplitter, 800 chars, 150 overlap, table-of-contents chunks removed |
| Embeddings | `qwen3-embedding:0.6b` (Ollama, local) |
| Vector DB | PostgreSQL + pgvector (Supabase, Frankfurt), HNSW index, cosine |
| Keyword search | BM25 with a German tokenizer |
| Reranker | `BAAI/bge-reranker-v2-m3` (cross-encoder, local) |
| LLM | `qwen3.5:4b` (Ollama, local) |
| Agent | LangGraph: security check → topic check → retrieve → grade → rewrite (max 2) → fallback → generate |

## 1. Retrieval

Metric: hit rate = the chunk containing the expected answer is among the top 4 results.

| Test set | Vector | Hybrid (BM25 + vector) | + Rerank |
| --- | --- | --- | --- |
| 25 questions, derived from retrieved chunks | 80% | 88% | 92% |
| 40 synthetic questions, AI-generated from the full PDFs | 58% | 68% | **73%** |
| All 65 | 66% | 75% | 80% |
| 8 real student questions (answerable) | – | – | **5/8** |

- The first test set is optimistic (questions written from chunks the retriever already found). The 40 synthetic questions give a more realistic number.
- The pipeline improvements hold on every test set: **+15 points** from vector-only to hybrid + rerank on the synthetic set.
- Earlier step: removing table-of-contents chunks raised the first test set from 76% to 80%.
- Migrating the vector store from Chroma to PostgreSQL + pgvector gave identical hit rates.

**Main failure modes**
1. **Programme confusion:** questions about the small Master Rechtsinformatik regulation (8 pages) retrieve the large LL.B. module catalogue (138 pages) instead (4/4 missed).
2. **FAQ splitting:** in the module catalogue, an FAQ question and its answer often end up in different chunks.
3. **Thin coverage:** some topics (printing, housing, rooms) appear only as one bullet point in the building directory.
4. **Legal structure:** § numbers and their titles end up in different chunks ("Was regelt § 4?").

## 2. Answer quality (RAGAS)

Judge: `qwen3:8b` (local), 65 questions, answer relevancy with strictness=1.

| Version | Faithfulness | Answer relevancy | Context precision |
| --- | --- | --- | --- |
| Simple pipeline | 0.80 | 0.53 | 0.88 |
| Agent | 0.76 | **0.60** | **0.92** |

Earlier run with the smaller `qwen3.5:4b` judge (25 questions, strictness=3):

| Version | Faithfulness | Answer relevancy | Context precision |
| --- | --- | --- | --- |
| Simple pipeline | 0.82 | 0.59 | 0.91 |
| Agent | 0.80 | 0.67 | 0.82 |

- **Consistent over all runs:** the agent improves answer relevancy (+0.07–0.08), at slightly lower faithfulness (−0.02–0.04).
- **Context precision depends on the judge:** the 4B judge rated the agent lower, the 8B judge higher. Small judge models are unreliable for this metric.
- **Reproducible:** the simple pipeline scored identically in two separate 8B runs.
- Scores are indicative only: the judges are small local models.

## 3. Real user questions

15 questions written by a student, without looking at the documents.

| Test | Result |
| --- | --- |
| Answerable questions, retrieval | 5/8 |
| Questions with no answer in the documents, honest "no info" | **7/7** (before fix: 5/7) |

- **7 of 15 real questions are not covered by the documents** (work, visa, Mensa, rent, opening hours, dress code). Students ask about daily life; the corpus covers study rules.
- Both invented answers (before the fix) came from the **fallback path**: after the grader rejected all chunks, the fallback still passed irrelevant chunks to the LLM.

### Fallback confidence threshold

The fallback now only uses chunks with a reranker score ≥ 0.3.

| Question | Max reranker score | Result |
| --- | --- | --- |
| Fachschaft (answerable) | 0.90 | answered |
| Graduiertenzentrum (answerable) | 0.49 | answered |
| Doppelmaster, after the thesis (answer scattered) | 0.02 | "no info" (lost) |
| Full-time work (no answer) | 0.22 | "no info" |
| Opening days (no answer) | 0.01 | "no info" |
| Dress code (no answer) | 0.00 | "no info" |

- Decision: **honesty over coverage.** For exam regulations, a wrong answer is worse than "I don't know".
- Effect on RAGAS: negligible (agent 0.77/0.60/0.93 → 0.76/0.60/0.92).

## 4. Agent vs simple pipeline (manual check, 5 hard questions)

| Question | Simple | Agent |
| --- | --- | --- |
| Deadline missed for reasons beyond one's control | wrong rule | correct (Nachfrist) |
| Withdrawing from exams | wrong date (registration deadline) | correct (11 January 2027) |
| How often can an exam be repeated | mixed rules | same |
| Centrum für Europarecht | wrong building | same |
| Double master, after the thesis | partly correct | "no info" (after threshold) |

Cost: ~1–2 s extra per question, ~20–25 s when rewrites are needed.

**Agent debugging findings**
- **Repeated rewrite:** with temperature 0, rewriting only the original question produced the same query twice → the prompt now includes the failed query.
- **Query drift:** rewrites drop key names ("Graduiertenzentrum" → "Zentrum für wissenschaftliche Weiterbildung").
- **Inconsistent grader:** the 4B grader is sometimes too lenient (4/4), sometimes too strict (0/4 on correct chunks), causing unnecessary rewrites.
- Takeaway: in production, route only low-confidence questions through the agent loop.

## 5. Security

- 24 automated tests (pytest): **22 passed, 2 expected failures**.
- Blocked: prompt injection in German and English, uppercase variants, character tricks ("Ign0riere"), rephrasings, indirect questions about instructions, empty and too-long input.
- Masked: e-mail addresses, phone numbers, IBANs.
- Output check blocks answers that leak the prompt.
- Red-teaming found 3 bypasses → fixed with text normalization and 2 new patterns.
- Known limitation (documented as expected-failure tests): rule-based filters can't catch every rephrasing. Next step: an LLM-based injection classifier.

## 6. Engineering findings

- **Table-of-contents chunks** ranked highest for some questions (many keywords, no content).
- **Hyphenated line breaks** in the PDFs ("angemes- sene") break words for keyword search and exact-match tests.
- **Correct retrieval, wrong answer:** the 4B model mixed up list items in the building directory (CEP → wrong street).
- **Too much context confuses a small model:** with ~15 chunks, answers mixed rules from different programmes; reranking to 4 chunks fixed this.
- **Reranking needs enough candidates:** with fewer hybrid candidates (k=4 instead of 5), the rerank hit rate dropped from 92% to 88%.
- **GPU sharing:** on an 8 GB laptop GPU, PyTorch (reranker) and Ollama crashed when both used CUDA → LLM on GPU, reranker on CPU.
- **Rate limits:** the Gemini free tier was too slow for embedding (~1,000 chunks); the Groq free tier was too small for a full RAGAS run → local models.
- **Idle database connections:** Supabase closed connections after long idle periods → `pool_pre_ping` and `pool_recycle`.
- **Chroma distance:** the default L2 distance gave negative relevance scores with Qwen embeddings → cosine.

## Next steps

- Metadata filter by study programme (fixes programme confusion)
- Contextual retrieval (prefix chunks with document and § context)
- FAQ-aware chunking for the module catalogue
- Route only low-confidence questions through the agent
- LLM-based prompt-injection classifier
- Larger set of real user questions