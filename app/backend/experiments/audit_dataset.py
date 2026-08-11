import json
import re
from pathlib import Path

YEARS = [
    1955,
    1965,
    1975,
    1985,
    1995,
    2005,
    2015,
    2025,
]

# ---------------------------------------------
# Count downloaded PDFs
# ---------------------------------------------

pdf_counts = {}

for year in YEARS:
    pdf_folder = Path(f"data/pdf/{year}")
    pdf_counts[year] = len(list(pdf_folder.glob("*.pdf")))

# ---------------------------------------------
# Count generated JSONs
# ---------------------------------------------

json_counts = {year: 0 for year in YEARS}

unknown = []

for file in Path("data/processed").glob("*.json"):

    with open(file, encoding="utf-8") as f:
        doc = json.load(f)

    path = doc.get("path", "")

    # Finds the first occurrence of a 4-digit year (e.g. 1955, 2005)
    match = re.search(r"(19|20)\d{2}", path)

    if match:
        year = int(match.group())

        if year in json_counts:
            json_counts[year] += 1

    else:
        unknown.append(file.name)

# ---------------------------------------------
# Print Report
# ---------------------------------------------

print("\n" + "=" * 60)
print("DATASET AUDIT REPORT")
print("=" * 60)

for year in YEARS:
    print(
        f"{year} | PDFs: {pdf_counts[year]:3} | JSONs: {json_counts[year]:3}"
    )

print("\n" + "=" * 60)

print(f"Total PDFs : {sum(pdf_counts.values())}")
print(f"Total JSONs: {sum(json_counts.values())}")

if unknown:
    print(f"\nCouldn't determine year for {len(unknown)} files:")
    for file in unknown:
        print(f" - {file}")
else:
    print("\nAll JSON files successfully classified by year.")