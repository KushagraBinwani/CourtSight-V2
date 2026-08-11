import re
from typing import List, Tuple

from .chunk_models import Chunk


class ParagraphChunker:
    """
    Splits a legal judgment into overlapping paragraph-based chunks.
    """

    def __init__(
        self,
        target_words: int = 450,
        overlap: int = 2,
    ):
        self.target_words = target_words
        self.overlap = overlap

    def chunk_document(self, document):
        """
        Split a judgment into chunks.
        """

        text = document["text"]
        case_id = document["case_id"]
        title = document["title"]

        text = self._extract_judgment(text)

        paragraphs = self._extract_paragraphs(text)

        chunks = self._build_chunks(paragraphs, case_id, title)

        return chunks

    def _extract_judgment(self, text: str) -> str:
        """
        Remove everything before the actual judgment begins.
        """

        markers = [
            "The Judgment of the Court was delivered by",
            "JUDGMENT",
            "ORDER"
        ]

        for marker in markers:

            idx = text.find(marker)

            if idx != -1:
                return text[idx:]

        # If we don't find any marker,
        # just return the original text.
        return text

    def _extract_paragraphs(self, text: str) -> List[Tuple[int, str]]:
        """
        Extract numbered paragraphs from a judgment.

        Returns
        -------
        List of tuples:
            (paragraph_number, paragraph_text)
        """

        text = text.replace("\r\n", "\n")

        pattern = re.compile(
            r"(\d+)\.\s*(.*?)(?=\n\d+\.\s|\Z)",
            re.DOTALL,
        )

        paragraphs = []

        for match in pattern.finditer(text):

            number = int(match.group(1))

            paragraph = match.group(2).strip()

            paragraphs.append((number, paragraph))

        return paragraphs

    def _build_chunks(
        self,
        paragraphs: List[Tuple[int, str]],
        case_id: str,
        title: str,
    ) -> List[Chunk]:

        chunks = []

        start = 0
        chunk_number = 1

        while start < len(paragraphs):

            end = start

            current_words = 0
            current_text = []

            while end < len(paragraphs):

                paragraph_number, paragraph_text = paragraphs[end]

                paragraph_words = len(paragraph_text.split())

                new_total = current_words + paragraph_words

                if new_total >= self.target_words:

                    current_diff = abs(self.target_words - current_words)
                    new_diff = abs(self.target_words - new_total)

                    if new_diff <= current_diff or current_words == 0:
                        current_text.append(f"{paragraph_number}. {paragraph_text}")
                        current_words = new_total
                        end += 1

                    break

                current_text.append(f"{paragraph_number}. {paragraph_text}")
                current_words += paragraph_words
                end += 1

            chunk = Chunk(
                chunk_id=f"{case_id}_{chunk_number}",
                case_id=case_id,
                chunk_number=chunk_number,
                start_paragraph=paragraphs[start][0],
                end_paragraph=paragraphs[end - 1][0],
                word_count=current_words,
                text="\n\n".join(current_text),
                title=title
            )

            chunks.append(chunk)

            chunk_number += 1

            if end == len(paragraphs):
                break

            start = max(end - self.overlap, start + 1)

        return chunks