# CourtSight Architecture

## Overview

CourtSight is an AI-powered legal research system designed to make Indian Supreme Court judgments easier to search and analyze.

The backend is organized as a modular pipeline that separates document processing, semantic retrieval, retrieval-augmented generation, and API concerns.

At a high level:

```text
                    CourtSight Backend

                         HTTP Request
                              │
                              ▼
                       ┌─────────────┐
                       │   FastAPI   │
                       │   API Layer │
                       └──────┬──────┘
                              │
                              ▼
                       ┌─────────────┐
                       │   Services  │
                       │ Composition │
                       └──────┬──────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
              ┌───────────┐       ┌────────────┐
              │ Retriever │       │    RAG     │
              └─────┬─────┘       └─────┬──────┘
                    │                   │
                    ▼                   ▼
              ┌───────────┐       ┌────────────┐
              │ Vector    │       │   Prompt   │
              │ Store     │       │  Builder   │
              │ (FAISS)   │       └─────┬──────┘
              └───────────┘             │
                                        ▼
                                  ┌────────────┐
                                  │ Generator  │
                                  │  (Gemini)  │
                                  └────────────┘

The broader knowledge-processing pipeline is:

Raw Judgments
      │
      ▼
  Ingestion
      │
      ▼
   Chunking
      │
      ▼
  Embeddings
      │
      ▼
 Vector Store
      │
      ▼
  Retrieval
      │
      ▼
     RAG
      │
      ▼
 Generated Answer

## Backend structure

The backend is divided into components based on their responsibility.

src/
│
├── ingestion/      # Build the knowledge base
├── chunking/       # Split documents into chunks
├── embeddings/     # Convert chunks into vectors
├── vector_store/   # Store and search vectors
├── retrieval/      # Retrieve relevant chunks
├── rag/            # Construct prompts and generate answers
│
├── models/         # Shared data models
│
└── config.py       # Global configuration

The application layer sits above these components:

app/
├── main.py         # FastAPI application entry point
├── routes.py       # HTTP API routes
├── services.py     # Application service composition
└── schemas.py      # Request/response schemas

# Data Processing Pipeline

CourtSight begins with a collection of legal judgments that must be transformed into representations suitable for semantic retrieval.

## 1. Ingestion

The ingestion layer is responsible for building the knowledge base from the source judgments and associated metadata.

Raw Judgment Data
        │
        ▼
   Ingestion Layer
        │
        ▼
     Documents

The ingestion layer is kept separate from retrieval so that document processing does not become coupled to the API or RAG system.

## 2. Chunking

Long judgments are divided into smaller chunks before embedding.

Document
    │
    ▼
Chunking
    │
    ├── Chunk 1
    ├── Chunk 2
    ├── Chunk 3
    └── ...

Chunking exists as an independent component because the retrieval system operates on chunks rather than entire judgments.

The resulting chunks become the units of semantic retrieval.

## 3. Embeddings

Each chunk is converted into a numerical vector representation.

Text Chunk
    │
    ▼
Sentence Transformer
    │
    ▼
Embedding Vector

The same embedding mechanism is also used to transform user queries into vectors.

This allows queries and document chunks to be compared within the same vector space.

## 4. Vector Store

The generated embeddings are stored and searched using FAISS.

Chunk Embeddings
       │
       ▼
     FAISS
       │
       ▼
Similarity Search

The vector store is responsible for:

building the vector index
storing associated embedded chunks
persisting the index
loading the index
performing similarity search

The vector-store layer is intentionally isolated from the retrieval layer.

## Retrieval Pipeline

The retrieval layer coordinates query embedding and vector search.

User Query
    │
    ▼
Embedding Generator
    │
    ▼
Query Embedding
    │
    ▼
Vector Store
    │
    ▼
Top-k Results

The retriever therefore acts as the bridge between the user's natural-language query and the vector store.

Keeping this logic separate allows retrieval strategies to evolve independently of the underlying vector database.

## Retrieval-Augmented Generation

CourtSight uses retrieval-augmented generation rather than sending a user's question directly to a generative model.

The process is:

User Query
    │
    ▼
Query Embedding
    │
    ▼
Semantic Retrieval
    │
    ▼
Relevant Chunks
    │
    ▼
Prompt Builder
    │
    ▼
Grounded Prompt
    │
    ▼
Gemini
    │
    ▼
Answer

The prompt-building layer takes the retrieved chunks and constructs the context provided to the generative model.

The generator is responsible for interacting with Gemini, while retrieval remains independent of the generation model.

This separation allows the retrieval system and generative model to be changed independently.

## Application Layer

The app/ package exposes CourtSight through an HTTP API.

main.py

main.py is the entry point of the backend application.

Its responsibilities include:

creating the FastAPI application
registering API routers
configuring middleware
configuring application lifecycle behavior
exposing the ASGI application

The application entry point intentionally contains application configuration rather than business logic.

## routes.py

routes.py defines the HTTP interface exposed by CourtSight.

The routes are responsible for:

receiving HTTP requests
validating input
invoking application services
returning structured responses

Routes are intentionally kept thin.

Business logic is delegated to the service layer rather than being implemented directly inside HTTP handlers.

HTTP Request
      │
      ▼
    Route
      │
      ▼
   Service
      │
      ▼
CourtSight Pipeline
      │
      ▼
HTTP Response

## services.py

services.py acts as the composition root of the application.

It assembles the reusable CourtSight components required to process requests.

The service layer coordinates components including:

EmbeddingGenerator
VectorStore
Retriever
PromptBuilder
Generator

Expensive components such as embedding models and vector stores are intended to be initialized once and reused across requests rather than recreated for every request.

This also provides a clean separation between HTTP handling and application logic.

# Separation of Concerns

CourtSight deliberately separates responsibilities across layers.

┌───────────────────────────────────────────┐
│              Application Layer            │
│                                           │
│  FastAPI → Routes → Services              │
└──────────────────────┬────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────┐
│              RAG / Retrieval              │
│                                           │
│  Retriever → Prompt Builder → Generator   │
└──────────────────────┬────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────┐
│           Representation Layer            │
│                                           │
│  Embeddings → Vector Store                │
└──────────────────────┬────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────┐
│            Knowledge Layer                │
│                                           │
│  Ingestion → Documents → Chunks           │
└───────────────────────────────────────────┘

This separation provides several advantages:

individual components can be tested independently
retrieval can evolve without changing the API layer
the generation model can be replaced without rebuilding the ingestion pipeline
expensive shared components can be reused across requests
HTTP concerns remain separate from application and ML logic

# Design Philosophy

CourtSight is organized around a pipeline of increasingly specialized representations:

Legal Judgment
      ↓
Structured Document
      ↓
Text Chunks
      ↓
Embedding Vectors
      ↓
Retrieved Context
      ↓
Generated Answer

Each stage has a specific responsibility and exposes a relatively small interface to the next stage.

This makes the system easier to experiment with as individual components evolve.

For example, different chunking strategies can be evaluated without changing the embedding or generation layers, while different embedding models can be evaluated without changing the API.

# Key Architectural Principle

The central design principle of CourtSight is separation of concerns.

Document processing, semantic representation, vector search, retrieval, generation, and HTTP serving are implemented as distinct layers.

This allows CourtSight to be treated not as a single monolithic "legal chatbot", but as a collection of independently replaceable components forming an end-to-end legal information retrieval system.