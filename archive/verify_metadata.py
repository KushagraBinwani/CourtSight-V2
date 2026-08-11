from pathlib import Path
import pandas as pd

START_YEAR = 1950
END_YEAR = 2025

metadata_root = Path("data/metadata")

total_files = 0
total_judgments = 0

print("=" * 60)
print("VERIFYING METADATA")
print("=" * 60)

for year in range(START_YEAR, END_YEAR + 1):

    metadata_file = metadata_root / str(year) / "metadata.parquet"

    if not metadata_file.exists():
        print(f"{year}: MISSING")
        continue

    df = pd.read_parquet(metadata_file)

    num_judgments = len(df)

    total_files += 1
    total_judgments += num_judgments

    print(f"{year}: {num_judgments:,} judgments")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print(f"Metadata files found : {total_files}")
print(f"Years expected       : {END_YEAR - START_YEAR + 1}")
print(f"Total judgments      : {total_judgments:,}")