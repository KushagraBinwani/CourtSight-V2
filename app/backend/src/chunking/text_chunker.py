from typing import List

from src.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    SENTENCE_TOLERANCE,
)

from src.ingestion.text_cleaner import TextCleaner
from src.models.chunk import Chunk


class TextChunker:
    """
    Fixed-size sliding window chunker.

    Splits cleaned document text into overlapping chunks
    using word count rather than paragraph boundaries.
    """

    def __init__(
        self,
        chunk_size: int = CHUNK_SIZE,
        overlap: int = CHUNK_OVERLAP,
    ):
        if overlap >= chunk_size:
            raise ValueError("Overlap must be smaller than chunk size.")

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_document(self, document) -> List[Chunk]:
        """
        Accepts a Document object.

        Returns
        -------
        List[Chunk]
        """
        text = TextCleaner.clean(document.text)

        if not text:
            return []

        words = text.split()

        chunks = []

        start = 0
        chunk_number = 0

        while start < len(words):

            target_end = min(
                start + self.chunk_size,
                len(words),
            )

            end = self._find_sentence_boundary(
                words,
                target_end,
            )

            chunk_words = words[start:end]

            chunk_text = " ".join(chunk_words)

            chunk = Chunk(
                chunk_id=f"{document.case_id}_chunk_{chunk_number}",
                case_id=document.case_id,
                chunk_number=chunk_number,
                start_word=start,
                end_word=end,
                word_count=len(chunk_words),
                text=chunk_text,
                title=document.title,
            )

            chunks.append(chunk)

            if end == len(words):
                break

            start = end - self.overlap
            chunk_number += 1

        return chunks

    def _find_sentence_boundary(
        self,
        words: List[str],
        target: int,
        tolerance: int = SENTENCE_TOLERANCE,
    ) -> int:
        """
        Extend chunk until the next sentence end.

        Prevents cutting in the middle of sentences
        whenever possible.
        """

        search_end = min(
            target + tolerance,
            len(words),
        )

        for i in range(target, search_end):

            if words[i - 1].endswith((".", "!", "?")):
                return i

        return target