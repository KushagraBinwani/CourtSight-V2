import json
from pathlib import Path

pages = []
words = []
chars = []

for file in Path("data/processed").glob("*.json"):

    with open(file, encoding="utf-8") as f:

        doc = json.load(f)

    pages.append(doc["page_count"])
    words.append(doc["word_count"])
    chars.append(len(doc["text"]))

print("=" * 50)

print("Documents :", len(words))

print()

print("Average Pages :", round(sum(pages)/len(pages),2))
print("Average Words :", round(sum(words)/len(words),2))
print("Average Characters :", round(sum(chars)/len(chars),2))

print()

print("Longest Judgment :", max(words))
print("Shortest Judgment :", min(words))

print()

print("Largest Pages :", max(pages))
print("Smallest Pages :", min(pages))