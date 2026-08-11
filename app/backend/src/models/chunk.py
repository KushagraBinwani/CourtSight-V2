from dataclasses import dataclass


@dataclass
class Chunk:
    """
    Represents one retrievable chunk from a legal judgment.
    """

    chunk_id: str
    case_id: str
    chunk_number: int

    # Word offsets in the cleaned document
    start_word: int
    end_word: int

    word_count: int

    text: str
    title: str