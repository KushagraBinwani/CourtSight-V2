# CourtSight

> An AI-powered legal research system for semantic search and retrieval over Indian Supreme Court judgments.

## Overview

CourtSight is a legal research platform designed to make large collections of Indian Supreme Court judgments easier to search and explore.

The project focuses on the retrieval side of legal NLP: transforming a large corpus of unstructured judgments into searchable semantic representations and using those representations to retrieve relevant legal context for a user query.

CourtSight combines:

- Document ingestion and preprocessing
- Metadata extraction
- Fixed-window text chunking
- SentenceTransformer embeddings
- FAISS vector search
- Retrieval-augmented generation
- Gemini-based answer generation
- Retrieval observability
- Legal source presentation

The goal is not simply to generate answers with an LLM, but to investigate how effectively relevant legal information can be retrieved from a large and heterogeneous corpus.

---

## Architecture

```text
                    ┌──────────────────┐
                    │ Supreme Court    │
                    │ Judgments        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Ingestion        │
                    │ & Preprocessing  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Document         │
                    │ Chunking         │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Sentence         │
                    │ Transformer      │
                    │ Embeddings       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ FAISS Vector     │
                    │ Index            │
                    └────────┬─────────┘
                             │
                  User Query │
                             ▼
                    ┌──────────────────┐
                    │ Semantic         │
                    │ Retrieval        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Prompt Builder   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Gemini           │
                    │ Generation       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Grounded Answer  │
                    │ + Sources        │
                    └──────────────────┘
```

---

## Retrieval Pipeline

### 1. Ingestion

Court judgments are processed into standardized `Document` objects.

The ingestion pipeline handles:

- PDF text extraction
- Metadata loading
- Text cleaning
- Document construction

Because the corpus contains judgments with inconsistent formatting, preprocessing was designed around the characteristics of the actual dataset rather than assuming uniform document structure.

### 2. Chunking

Large judgments are divided into fixed-size chunks before embedding.

Multiple chunking strategies were investigated, including paragraph-based approaches. Legacy judgments often lacked sufficiently consistent structural boundaries, producing highly variable chunk sizes.

The current pipeline uses a fixed-window strategy selected through experimentation.

### 3. Embeddings

Each chunk is transformed into a dense semantic vector using a SentenceTransformer model.

The same embedding model is used to encode both:

- Document chunks
- User queries

This allows queries and legal text to be compared in the same vector space.

### 4. Vector Search

CourtSight uses FAISS for efficient nearest-neighbor search over the chunk embeddings.

For a query:

```text
Query
  ↓
Embedding
  ↓
FAISS
  ↓
Top-k semantic matches
```

The current retrieval pipeline returns the highest-ranked matching chunks for downstream generation.

---

## Retrieval-Augmented Generation

CourtSight separates retrieval from generation.

The LLM does not independently search the corpus.

Instead:

```text
User Query
     ↓
Semantic Retrieval
     ↓
Relevant Legal Context
     ↓
Prompt Construction
     ↓
Gemini
     ↓
Answer
```

The generation prompt constrains the model to use the retrieved context when answering the query.

This separation allows retrieval quality to be evaluated independently from the language model.

---

## Why Retrieval Is the Core Problem

Semantic similarity does not necessarily imply retrieval usefulness.

Two chunks can be semantically related to a query while only one contains the information actually required to answer it.

For example, a judgment may contain extensive discussion of a legal provision that is related to a query without that discussion being necessary to answer the specific question.

This distinction motivates future work on:

- Retrieval evaluation
- Larger initial candidate sets
- Reranking
- Hybrid retrieval
- Metadata-aware filtering

---

## Experiments

CourtSight includes experiments investigating the characteristics of the legal corpus and different preprocessing strategies.

These include:

- Corpus analysis
- Document structure analysis
- Paragraph-based chunking
- Duplicate detection
- Outlier detection
- Dataset auditing

These experiments informed the design of the production pipeline.

---

## Observability

The backend exposes basic retrieval statistics alongside generated answers, including:

- Number of retrieved chunks
- Retrieval similarity information
- Average retrieval score
- End-to-end latency

This provides a foundation for future quantitative retrieval evaluation.

---

## Project Structure

```text
CourtSight/
│
├── app/
│   ├── backend/
│   │   ├── app/
│   │   ├── experiments/
│   │   ├── scripts/
│   │   └── src/
│   │       ├── chunking/
│   │       ├── embeddings/
│   │       ├── ingestion/
│   │       ├── models/
│   │       ├── rag/
│   │       ├── retrieval/
│   │       └── vector_store/
│   │
│   └── frontend/
│       ├── app/
│       ├── components/
│       ├── lib/
│       └── types/
│
├── docs/
│   └── architecture.md
│
├── notes/
│   └── domain-models.md
│
├── archive/
│
└── storage/
```

---

## Tech Stack

### Backend

- Python
- FastAPI
- SentenceTransformers
- FAISS
- Gemini

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

### Data & NLP

- PDF text extraction
- Metadata extraction
- Text preprocessing
- Semantic embeddings
- Vector similarity search
- Retrieval-augmented generation

---

## Current Limitations

CourtSight is an active research and engineering project.

Current limitations include:

- Semantic retrieval is currently the primary retrieval strategy
- Retrieval quality is not yet evaluated using a formal benchmark
- Legacy judgments contain significant structural inconsistency
- Citation relationships are an ongoing extension of the system
- Hybrid retrieval and reranking remain areas for experimentation

---

## Future Work

Planned directions include:

- Formal retrieval evaluation
- Reranking
- Hybrid lexical + semantic retrieval
- Metadata-aware filtering
- Citation graph construction
- Citation-aware retrieval
- Clickable source citations
- Improved handling of legacy judgments
- Comparison of alternative embedding models

---

## Documentation

More detailed technical documentation is available in:

- [`docs/architecture.md`](docs/architecture.md)
- [`notes/domain-models.md`](notes/domain-models.md)

---

## Status

CourtSight is an ongoing project focused on understanding and engineering semantic retrieval systems for legal information.

The system is intentionally being developed incrementally, with experiments and design decisions documented alongside the production pipeline.
