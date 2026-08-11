from dataclasses import dataclass

from src.models.chunk import Chunk


@dataclass
class EmbeddedChunk:

    """
    Represents a chunk together with its embedding vector.
    """

    chunk: Chunk

    embedding: list[float]