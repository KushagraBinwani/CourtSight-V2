import re


class TextCleaner:
    """
    Cleans extracted judgment text before chunking.
    """

    @staticmethod
    def clean(text: str) -> str:
        if not text:
            return ""

        # Normalize line endings
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Remove multiple blank lines
        text = re.sub(r"\n{2,}", "\n\n", text)

        # Remove repeated spaces/tabs
        text = re.sub(r"[ \t]+", " ", text)

        # Remove isolated page numbers
        text = re.sub(r"\n\s*\d+\s*\n", "\n", text)

        # Remove common OCR artifacts
        text = re.sub(r"[·•]+", "", text)

        # Remove spaces before punctuation
        text = re.sub(r"\s+([.,;:!?])", r"\1", text)

        # Collapse whitespace
        text = re.sub(r"\s+", " ", text)

        return text.strip()