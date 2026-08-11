from dataclasses import dataclass

from src.models.embedding import EmbeddedChunk


@dataclass
class SearchResult:
    """
    Represents one retrieved chunk together with its similarity score.
    """
    score: float
    embedded_chunk: EmbeddedChunk