import json

from src.config import (
    INDEX_DIR,
    PROCESSED_DIR,
)


from src.models.document import Document
from src.chunking.text_chunker import TextChunker
from src.embeddings.embedding_generator import EmbeddingGenerator
from src.vector_store.vector_store import VectorStore

def load_documents():

    documents = []

    json_files = sorted(PROCESSED_DIR.glob("*.json"))

    print(f"Found {len(json_files)} processed documents.\n")

    for json_file in json_files:

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        documents.append(
            Document(
                case_id=data["case_id"],
                title=data["title"],
                citation=data["citation"],
                decision_date=data["decision_date"],
                judges=data["judges"],
                petitioner=data["petitioner"],
                respondent=data["respondent"],
                court=data["court"],
                path=data["path"],
                page_count=data["page_count"],
                word_count=data["word_count"],
                text=data["text"],
            )
        )

    return documents


def main():

    INDEX_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("=" * 80)
    print("Loading Documents")
    print("=" * 80)

    documents = load_documents()

    print(f"Loaded {len(documents)} documents.\n")

    print("=" * 80)
    print("Chunking Documents")
    print("=" * 80)

    chunker = TextChunker()

    all_chunks = []

    for i, document in enumerate(documents, start=1):

        all_chunks.extend(
            chunker.chunk_document(document)
        )

        if i % 100 == 0 or i == len(documents):
            print(f"Chunked {i}/{len(documents)} documents...")

    print(f"\nCreated {len(all_chunks)} chunks.\n")

    print("=" * 80)
    print("Generating Embeddings")
    print("=" * 80)

    embedder = EmbeddingGenerator()

    embedded_chunks = embedder.embed_chunks(all_chunks)

    print(f"\nEmbedded {len(embedded_chunks)} chunks.\n")

    print("=" * 80)
    print("Building FAISS Index")
    print("=" * 80)

    vector_store = VectorStore()

    vector_store.build_index(embedded_chunks)

    print("\nSaving index...")

    vector_store.save(
        INDEX_DIR / "faiss.index",
        INDEX_DIR / "chunks.pkl",
    )

    print("\n" + "=" * 80)
    print("DONE")
    print("=" * 80)
    print(f"Documents   : {len(documents)}")
    print(f"Chunks      : {len(all_chunks)}")
    print(f"Embeddings  : {len(embedded_chunks)}")
    print(f"FAISS Index : {INDEX_DIR / 'faiss.index'}")
    print(f"Chunk Store : {INDEX_DIR / 'embedded_chunks.pkl'}")


if __name__ == "__main__":
    main()