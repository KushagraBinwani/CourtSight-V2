from dataclasses import dataclass

from src.models.chunk import Chunk


@dataclass
class SearchResult:
    """
    Represents one retrieved chunk together with its similarity score.
    """
    score: float
    chunk: Chunk