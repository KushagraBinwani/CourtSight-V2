
import json
from pathlib import Path
from tqdm import tqdm

from src.config import (
    PDF_DIR,
    METADATA_DIR,
    PROCESSED_DIR,
)

from src.ingestion.document_builder import build_document
from src.ingestion.metadata_loader import load_metadata



def available_years():

    return sorted(
        int(folder.name)
        for folder in PDF_DIR.iterdir()
        if folder.is_dir()
    )


def main():

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    generated = 0
    skipped = 0
    already_processed = 0

    years = available_years()

    print(f"Found {len(years)} year(s): {years}")

    for year in years:

        print(f"\n===== Processing {year} =====")

        metadata_file = (
            METADATA_DIR
            / str(year)
            / "metadata.parquet"
        )

        metadata = load_metadata(metadata_file)

        for _, row in tqdm(
            metadata.iterrows(),
            total=len(metadata),
            desc=f"{year}",
        ):

            pdf = (
                PDF_DIR
                / str(year)
                / f"{row['path']}_EN.pdf"
            )

            if not pdf.exists():
                skipped += 1
                continue

            output = (
                PROCESSED_DIR
                / f"{row['path']}_EN.json"
            )

            if output.exists():
                already_processed += 1
                continue

            document = build_document(
                row,
                pdf,
            )

            with open(
                output,
                "w",
                encoding="utf-8",
            ) as f:

                json.dump(
                    document.to_dict(),
                    f,
                    indent=4,
                    ensure_ascii=False,
                )

            generated += 1

    print("\n==============================")
    print("Processing Complete")
    print("==============================")
    print(f"Generated         : {generated}")
    print(f"Already Processed : {already_processed}")
    print(f"Skipped           : {skipped}")
    print(f"Total Files Seen  : {generated + already_processed + skipped}")


if __name__ == "__main__":
    main()