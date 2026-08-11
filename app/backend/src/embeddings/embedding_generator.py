from collections.abc import Sequence

from sentence_transformers import SentenceTransformer

from src.models.chunk import Chunk
from src.models.embedding import EmbeddedChunk

from src.config import (
    EMBEDDING_BATCH_SIZE,
    EMBEDDING_MODEL,
)


class EmbeddingGenerator:

    def __init__(
        self,
        model_name: str = EMBEDDING_MODEL,
    ):

        self.model: SentenceTransformer = SentenceTransformer(
            model_name
        )

    def embed_query(
        self,
        query: str,
    ) -> list[float]:

        embedding = self.model.encode(
            query,
            convert_to_numpy=True,
        )

        return embedding.tolist()

    def embed_chunks(
        self,
        chunks: Sequence[Chunk],
        batch_size: int = EMBEDDING_BATCH_SIZE,
    ) -> list[EmbeddedChunk]:

        if not chunks:
            return []

        texts = [
            f"{chunk.title}\n\n{chunk.text}"
            for chunk in chunks
        ]

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            show_progress_bar=True,
        )

        return [
            EmbeddedChunk(
                chunk=chunk,
                embedding=embedding.tolist(),
            )
            for chunk, embedding in zip(
                chunks,
                embeddings,
            )
        ]