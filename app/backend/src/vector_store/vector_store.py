import numpy as np
import faiss
import joblib

from src.models.chunk import Chunk
from src.models.search import SearchResult


class VectorStore:

    def __init__(self):
        self.index = None
        self.chunks: list[Chunk] = []

    def build_index(self, embedded_chunks):

        vectors = [
            embedded.embedding
            for embedded in embedded_chunks
        ]

        vectors = np.array(
            vectors,
            dtype=np.float32,
        )

        faiss.normalize_L2(vectors)

        dimension = vectors.shape[1]

        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(vectors)

        self.chunks = [
            embedded.chunk
            for embedded in embedded_chunks
        ]

    def save(self, index_path, chunks_path):

        faiss.write_index(
            self.index,
            str(index_path),
        )

        joblib.dump(
            self.chunks,
            str(chunks_path),
        )

    def load(self, index_path, chunks_path):

        self.index = faiss.read_index(
            str(index_path)
        )

        self.chunks = joblib.load(
            str(chunks_path)
        )

    def search(self, query_embedding, k=5):

        query_vector = np.array(
            [query_embedding],
            dtype=np.float32,
        )

        faiss.normalize_L2(query_vector)

        scores, indices = self.index.search(
            query_vector,
            k,
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):

            results.append(
                SearchResult(
                    score=float(score),
                    chunk=self.chunks[idx],
                )
            )

        return results