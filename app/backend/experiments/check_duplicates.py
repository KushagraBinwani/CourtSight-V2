from collections import Counter

from src.ingestion.metadata_loader import load_metadata

YEARS = [1965, 1975]

for year in YEARS:
    metadata = load_metadata(f"data/metadata/{year}/metadata.parquet")

    counts = Counter(metadata["path"])

    duplicates = {k: v for k, v in counts.items() if v > 1}

    print(f"\n{year}")

    if duplicates:
        print("Duplicate paths found:")
        for path, count in duplicates.items():
            print(path, count)
    else:
        print("No duplicate paths.")