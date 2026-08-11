import time

from src.embeddings.embedding_generator import EmbeddingGenerator
from src.rag.generator import Generator
from src.rag.prompt_builder import PromptBuilder
from src.retrieval.retriever import Retriever
from src.vector_store.vector_store import VectorStore
from src.config import INDEX_DIR


class CourtSightService:

    def __init__(self):

        print("=" * 80)
        print("Starting CourtSight")
        print("=" * 80)

        print("Loading embedding model...")
        self.embedding_generator = EmbeddingGenerator()

        print("Loading FAISS index...")
        self.vector_store = VectorStore()
        self.vector_store.load(
            INDEX_DIR / "faiss.index",
            INDEX_DIR / "embedded_chunks.pkl",
        )

        print("Creating retriever...")
        self.retriever = Retriever(
            embedding_generator=self.embedding_generator,
            vector_store=self.vector_store,
        )

        print("Loading prompt builder...")
        self.prompt_builder = PromptBuilder()

        print("Loading Gemini...")
        self.generator = Generator()

        print("\nCourtSight is ready.\n")

    def answer(
        self,
        query: str,
    ):
        start = time.perf_counter()

        search_results = self.retriever.retrieve(query)

        prompt = self.prompt_builder.build(
            query=query,
            results=search_results,
        )

        answer = self.generator.generate(prompt)

        latency = round(time.perf_counter() - start, 2)

        avg_score = (
            round(
                sum(result.score for result in search_results) / len(search_results),
                4,
            )
            if search_results
            else 0
        )

        return {
            "answer": answer,
            "results": search_results,
            "stats": {
                "retrieved": len(search_results),
                "latency": latency,
                "avg_score": avg_score,
            },
        }


courtsight = CourtSightService()