"""
weak_ner_spacy.py

Pipeline:
- Read all .txt in documents/
- Weak-label PERSON, ORG, DATE using regex
- Build spaCy training data
- Train tiny NER model
"""

import re
from pathlib import Path
import random
import json

import spacy
from spacy.tokens import DocBin
from spacy.training.example import Example


DOCS_DIR = Path("documents")


# ---- Weak labelers ----
PERSON_RE = re.compile(r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b")
ORG_RE = re.compile(r"\b([A-Z][A-Za-z0-9]+ (Corp|LLC|Ltd|Inc))\b")
DATE_PATTERNS = [
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),                                 # 2025-03-21
    re.compile(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}, \d{4}\b"),
    re.compile(r"\b\d{1,2}/\d{1,2}/\d{4}\b"),
    re.compile(r"\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b"),
]


def weak_label(text: str):
    ents = []

    # PERSON
    for m in PERSON_RE.finditer(text):
        start, end = m.span(1)
        ents.append((start, end, "PERSON"))

    # ORG
    for m in ORG_RE.finditer(text):
        start, end = m.span(1)
        ents.append((start, end, "ORG"))

    # DATE
    for pat in DATE_PATTERNS:
        for m in pat.finditer(text):
            start, end = m.span(0)
            ents.append((start, end, "DATE"))

    # Deduplicate & resolve overlaps (simple greedy)
    ents = sorted(ents, key=lambda x: (x[0], -(x[1] - x[0])))
    final_ents = []
    last_end = -1
    for start, end, label in ents:
        if start >= last_end:
            final_ents.append((start, end, label))
            last_end = end

    return final_ents


def load_docs_docsdir():
    all_examples = []
    for path in DOCS_DIR.glob("*.txt"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if not text.strip():
            continue
        ents = weak_label(text)
        all_examples.append((text, {"entities": ents}))
    return all_examples


def main():
    data = load_docs_docsdir()
    random.shuffle(data)

    split = int(0.8 * len(data))
    train_data = data[:split]
    dev_data = data[split:]

    nlp = spacy.blank("en")
    ner = nlp.add_pipe("ner")

    for _, ann in train_data:
        for _, _, label in ann["entities"]:
            ner.add_label(label)

    # Build DocBin for dev (optional)
    dev_docbin = DocBin()
    for text, ann in dev_data:
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in ann["entities"]:
            span = doc.char_span(start, end, label=label)
            if span:
                ents.append(span)
        doc.ents = ents
        dev_docbin.add(doc)
    dev_docbin.to_disk("dev_ner.spacy")

    # Train
    optimizer = nlp.begin_training()
    for it in range(10):
        random.shuffle(train_data)
        losses = {}
        for text, ann in train_data:
            doc = nlp.make_doc(text)
            ents = []
            for start, end, label in ann["entities"]:
                span = doc.char_span(start, end, label=label)
                if span:
                    ents.append(span)
            doc.ents = ents
            example = Example.from_dict(doc, {"entities": [(e.start_char, e.end_char, e.label_) for e in ents]})
            nlp.update([example], sgd=optimizer, losses=losses)
        print(f"Iteration {it} - Losses: {losses}")

    nlp.to_disk("weak_ner_model")

    # Quick predictions on dev
    preds = []
    for text, _ in dev_data[:20]:
        doc = nlp(text)
        ents = [(ent.text, ent.label_) for ent in doc.ents]
        preds.append({"text": text[:200], "ents": ents})
    with open("ner_predictions_sample.json", "w", encoding="utf-8") as f:
        json.dump(preds, f, indent=2)


if __name__ == "__main__":
    main()
