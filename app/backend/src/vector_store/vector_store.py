import numpy as np
import faiss
import joblib

from src.models.search import SearchResult


class VectorStore:

    def __init__(self):
        self.index = None
        self.embedded_chunks = []

    def build_index(self, embedded_chunks):

        self.embedded_chunks = embedded_chunks

        vectors = [
            embedded.embedding
            for embedded in embedded_chunks
        ]

        vectors = np.array(vectors, dtype=np.float32)

        faiss.normalize_L2(vectors)

        dimension = vectors.shape[1]

        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(vectors)

    def save(self, index_path, metadata_path):

        faiss.write_index(
            self.index,
            str(index_path),
        )

        joblib.dump(
            self.embedded_chunks,
            str(metadata_path),
        )

    def load(self, index_path, metadata_path):

        self.index = faiss.read_index(
            str(index_path)
        )

        self.embedded_chunks = joblib.load(
            str(metadata_path)
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
                    embedded_chunk=self.embedded_chunks[idx],
                )
            )

        return results