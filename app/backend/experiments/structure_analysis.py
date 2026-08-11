import json
from pathlib import Path

HEADINGS = [
    "Issue for Consideration",
    "Headnotes",
    "Facts",
    "Analysis",
    "Reasoning",
    "Conclusion",
    "Order",
    "Result of the case",
    "JUDGMENT",
]

counts = {h: 0 for h in HEADINGS}

documents = 0

for file in Path("data/processed").glob("*.json"):

    documents += 1

    with open(file, encoding="utf-8") as f:

        text = json.load(f)["text"]

    lower = text.lower()

    for heading in HEADINGS:

        if heading.lower() in lower:

            counts[heading] += 1

print(f"\nDocuments Analysed : {documents}\n")

for k, v in counts.items():

    print(f"{k:25} {v}")