from src.models.document import Document

from src.ingestion.pdf_extractor import extract_pdf


def build_document(metadata_row, pdf_path):

    extracted = extract_pdf(pdf_path)

    return Document(

        case_id=metadata_row.get("case_id"),

        title=metadata_row["title"],

        citation=metadata_row["citation"],

        decision_date=str(metadata_row["decision_date"]),

        judges=metadata_row["judge"],

        petitioner=metadata_row["petitioner"],

        respondent=metadata_row["respondent"],

        court=metadata_row["court"],

        path=metadata_row["path"],

        page_count=extracted["pages"],

        word_count=extracted["words"],

        text=extracted["text"]

    )