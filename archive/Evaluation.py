import fitz
import pandas as pd
from pathlib import Path

YEARS = [1955, 1965, 1975, 1985, 1995, 2005, 2015, 2025]

results = []

REQUIRED_FIELDS = [
    "title",
    "citation",
    "judge",
    "decision_date",
    "path"
]

for year in YEARS:

    metadata_path = Path(f"data/metadata/{year}/metadata.parquet")
    pdf_folder = Path(f"data/pdf/{year}")

    df = pd.read_parquet(metadata_path)

    row = df.iloc[0]

    pdf_name = f"{row['path']}_EN.pdf"
    pdf_path = pdf_folder / pdf_name

    metadata_complete = True

    for field in REQUIRED_FIELDS:
        if pd.isna(row[field]) or str(row[field]).strip() == "":
            metadata_complete = False

    pdf_exists = pdf_path.exists()

    pages = 0
    words = 0
    chars = 0
    empty_pages = 0
    avg_words = 0
    complete = False
    error = ""

    if pdf_exists:

        try:

            doc = fitz.open(pdf_path)

            pages = len(doc)

            full_text = ""

            for page in doc:

                text = page.get_text()

                if len(text.strip()) == 0:
                    empty_pages += 1

                full_text += text

            words = len(full_text.split())
            chars = len(full_text)

            avg_words = round(words/pages,1)

            ending = full_text[-2000:].lower()

            keywords = [
                "result of the case",
                "appeal allowed",
                "appeal dismissed",
                "petition dismissed",
                "disposed of",
                "costs"
            ]

            complete = any(k in ending for k in keywords)

        except Exception as e:
            error = str(e)

    verdict = (
        metadata_complete
        and pdf_exists
        and pages > 0
        and empty_pages == 0
        and words > 1000
        and complete
    )

    results.append({

        "Year": year,

        "Metadata Complete": metadata_complete,

        "PDF Exists": pdf_exists,

        "Pages": pages,

        "Words": words,

        "Characters": chars,

        "Avg Words/Page": avg_words,

        "Empty Pages": empty_pages,

        "Extraction Complete": complete,

        "Verdict": "PASS" if verdict else "FAIL",

        "Error": error

    })

report = pd.DataFrame(results)

print(report)

report.to_csv("pipeline_validation_report.csv", index=False)

print("\nSaved pipeline_validation_report.csv")