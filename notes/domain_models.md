# CourtSight Domain Models

## Overview

CourtSight uses a small set of domain models to represent information as it moves through the retrieval pipeline.

The models form a progression from the original legal judgment to its searchable semantic representation and finally to a ranked retrieval result.

```text
Document
    │
    ▼
Chunk
    │
    ▼
EmbeddedChunk
    │
    ▼
SearchResult

Each model has a specific responsibility and keeps the different stages of the pipeline decoupled.

# Document
## Purpose

Document represents a single Supreme Court judgment.

It provides the canonical representation of a legal judgment that the rest of the CourtSight pipeline can operate on.

## Responsibilities
Store judgment metadata
Store extracted judgment text
Provide serialization through to_dict()
Why Does It Exist?

The source corpus contains legal judgments alongside metadata in different formats.

Document provides a standardized representation that the rest of CourtSight can consume regardless of how the judgment was originally stored.

## Used By
Ingestion
Chunking
Embedding
Design Pattern

Document is a domain model.

It represents data rather than implementing processing logic.

## Future Improvements
Make the dataclass immutable with frozen=True
Separate document metadata into a dedicated Metadata model
Add validation
Introduce type-safe enums for fields such as court

# Chunk
## Purpose

Chunk represents a single retrievable segment of a legal judgment.

It is the fundamental unit used by embedding, vector storage, semantic retrieval, and LLM context generation.

## Responsibilities
Store chunk text
Maintain its position within the original document
Preserve its relationship to the parent judgment
Provide metadata required during retrieval
Fields
Field	Purpose
chunk_id	Globally unique identifier for the chunk
case_id	Identifies the parent legal judgment
chunk_number	Order of the chunk within the document
start_word	Starting word index in the original document
end_word	Ending word index in the original document
word_count	Number of words contained in the chunk
text	Chunk content that will be embedded
title	Case title for display and citation

## Why Does It Exist?

Large legal judgments cannot be efficiently treated as single retrieval units.

The Chunk model provides a standardized representation of smaller searchable sections while maintaining a connection to the original judgment.

## Position in the Pipeline
Document
    │
    ▼
Chunk
    │
    ▼
Embedding
    │
    ▼
Vector Store
    │
    ▼
Semantic Retrieval
    │
    ▼
LLM Context

## Relationship With Document
Document
    │
    ├── Chunk 1
    ├── Chunk 2
    ├── Chunk 3
    └── ...

A Document may produce many Chunk objects.

Each Chunk belongs to one parent judgment.

## Design Decisions
Separate Domain Model

Chunk is independent of the chunking algorithm.

This allows different chunking strategies—fixed-size, paragraph-based, semantic, or others—to produce the same standardized object.

Positional Metadata

The model stores:

start_word
end_word

rather than storing only the chunk text.

This preserves information about where the chunk originated in the judgment and creates opportunities for future functionality such as:

reconstructing surrounding context
highlighting passages
merging adjacent retrieved chunks
tracing retrieval back to the original judgment
Minimal Metadata

The chunk does not duplicate the complete Document object.

Instead, it stores the metadata needed during retrieval while retaining enough information to identify the parent judgment.

## Future Improvements
Make the dataclass immutable
Add citation metadata
Store token count in addition to word count
Store optional section or heading information
Store source page numbers for PDF traceability

# EmbeddedChunk
## Purpose

EmbeddedChunk represents a Chunk together with its semantic embedding vector.

It is the output of the embedding stage and the input to vector indexing and semantic retrieval.

## Responsibilities
Store the original Chunk
Store its embedding vector
Preserve the relationship between semantic representation and source text
Fields
Field	Purpose
chunk	Original Chunk object
embedding	Numerical vector representing the chunk
Why Does It Exist?

An embedding model transforms text into a high-dimensional numerical representation.

EmbeddedChunk keeps that representation paired with the source Chunk, allowing downstream components to access both the vector and the original legal text.

## Position in the Pipeline
Document
      │
      ▼
Chunk
      │
      ▼
EmbeddingGenerator
      │
      ▼
EmbeddedChunk
      │
      ▼
Vector Store
      │
      ▼
Retriever

## Design Decisions

### Composition

Rather than copying metadata such as case_id, title, or text, EmbeddedChunk stores the complete Chunk.

This avoids unnecessary duplication and keeps the complete chunk representation available during retrieval.

### Separation of Concerns

EmbeddedChunk is a data model only.

It does not generate embeddings or interact with embedding services.

Those responsibilities belong to the embedding subsystem.

## Architectural Role

EmbeddedChunk bridges text processing and vector search.

Chunk
      │
      ▼
EmbeddedChunk
      │
      ▼
FAISS Index

## Future Improvements

Make the dataclass immutable
Store embedding dimensionality
Support multiple embedding vectors for different models
Record the embedding model used to create the vector

# SearchResult
## Purpose

SearchResult represents a retrieved EmbeddedChunk together with its similarity score.

It is the output of the vector search stage and the input to downstream retrieval and RAG components.

## Responsibilities
Store the retrieved EmbeddedChunk
Preserve the similarity score returned by vector search
Represent a ranked retrieval result
Fields
Field	Purpose
score	Similarity score between the query and retrieved chunk
embedded_chunk	Retrieved EmbeddedChunk

## Why Does It Exist?

Vector search produces two important pieces of information:

Which chunk was retrieved
How similar that chunk was to the query

SearchResult combines these into one object that downstream components can consume.

## Position in the Pipeline
User Query
      │
      ▼
EmbeddingGenerator
      │
      ▼
Query Embedding
      │
      ▼
VectorStore
      │
      ▼
SearchResult
      │
      ▼
Retriever
      │
      ▼
LLM

## Design Decisions
### Composition

Rather than storing only a chunk identifier, SearchResult contains the complete EmbeddedChunk.

This provides immediate access to:

chunk text
chunk metadata
source information
embedding

without requiring an additional lookup.

### Similarity Score

The retrieval score is preserved alongside the retrieved chunk.

This allows future retrieval stages to perform:

ranking
threshold filtering
reranking
confidence reporting
Separation of Concerns

SearchResult is a data model only.

It does not perform retrieval or ranking.

Those responsibilities belong to the retrieval subsystem.

## Future Improvements
Make the dataclass immutable
Store retrieval rank
Store retrieval method, such as vector, hybrid, or reranked
Store optional reranking explanations or metadata

# Domain Model Flow

The four models form a progression through the CourtSight retrieval pipeline:

┌──────────────┐
│   Document   │
│              │
│ Full legal   │
│ judgment     │
└──────┬───────┘
       │
       │ chunking
       ▼
┌──────────────┐
│    Chunk     │
│              │
│ Retrievable  │
│ text segment │
└──────┬───────┘
       │
       │ embedding
       ▼
┌──────────────┐
│ EmbeddedChunk│
│              │
│ Text + vector│
└──────┬───────┘
       │
       │ vector search
       ▼
┌──────────────┐
│ SearchResult │
│              │
│ Chunk + score│
└──────────────┘

This separation allows each stage of CourtSight to operate on a clearly defined representation rather than sharing implementation-specific objects.

# Key Takeaway

The domain models provide the data contracts connecting the major stages of CourtSight.

A legal judgment begins as a Document, becomes a collection of retrievable Chunk objects, receives semantic representations as EmbeddedChunk objects, and ultimately becomes a ranked SearchResult when retrieved for a user query.

This structure keeps the retrieval pipeline modular and makes individual components easier to replace, test, and extend.