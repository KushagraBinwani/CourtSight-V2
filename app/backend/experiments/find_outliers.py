import json
from pathlib import Path

largest = None
smallest = None

for file in Path("data/processed").glob("*.json"):

    with open(file, encoding="utf-8") as f:
        doc = json.load(f)

    if largest is None or doc["word_count"] > largest["word_count"]:
        largest = doc

    if smallest is None or doc["word_count"] < smallest["word_count"]:
        smallest = doc

print("=" * 60)
print("Largest Judgment")
print("=" * 60)

print("Path:", largest["path"])
print("Words:", largest["word_count"])
print("Pages:", largest["page_count"])
print("Title:", largest["title"])

print()

print("=" * 60)
print("Smallest Judgment")
print("=" * 60)

print("Path:", smallest["path"])
print("Words:", smallest["word_count"])
print("Pages:", smallest["page_count"])
print("Title:", smallest["title"])