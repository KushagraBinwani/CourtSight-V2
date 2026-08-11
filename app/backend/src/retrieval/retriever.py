from src.embeddings.embedding_generator import EmbeddingGenerator
from src.vector_store.vector_store import VectorStore


class Retriever:

    def __init__(
        self,
        embedding_generator: EmbeddingGenerator,
        vector_store: VectorStore,
    ):

        self.embedding_generator = embedding_generator
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        k: int = 5,
    ):

        query_embedding = self.embedding_generator.embed_query(query)

        results = self.vector_store.search(
            query_embedding=query_embedding,
            k=k,
        )

        return results