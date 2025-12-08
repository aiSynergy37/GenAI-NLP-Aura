# summarize_article.py
"""
Summarize a long article using T5-small.

Input: article.txt (plain text)
Output:
    summary.txt
    chunk_summaries.json

Requirements:
    pip install transformers
"""

import json
from pathlib import Path

from transformers import T5TokenizerFast, T5ForConditionalGeneration


MODEL_NAME = "t5-small"
INPUT_FILE = "article.txt"
SUMMARY_FILE = "summary.txt"
CHUNK_SUMMARIES_FILE = "chunk_summaries.json"


def read_article(path: str) -> str:
    return Path(path).read_text(encoding="utf-8", errors="ignore")


def split_into_chunks(text: str, max_words: int = 200):
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i : i + max_words])
        if chunk.strip():
            chunks.append(chunk)
    return chunks


def summarize_text(text: str, tokenizer, model, max_input_len=512, max_output_len=128):
    inputs = tokenizer(
        "summarize: " + text,
        return_tensors="pt",
        truncation=True,
        max_length=max_input_len,
    )
    output_ids = model.generate(
        inputs.input_ids,
        max_length=max_output_len,
        num_beams=4,
        early_stopping=True,
    )
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)


def main():
    article = read_article(INPUT_FILE)

    tokenizer = T5TokenizerFast.from_pretrained(MODEL_NAME)
    model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

    chunks = split_into_chunks(article, max_words=200)

    chunk_summaries = []
    for idx, chunk in enumerate(chunks):
        print(f"Summarizing chunk {idx+1}/{len(chunks)}...")
        s = summarize_text(chunk, tokenizer, model)
        chunk_summaries.append({"chunk_index": idx, "summary": s})

    # Optionally generate a final summary from all chunk summaries
    combined = " ".join(cs["summary"] for cs in chunk_summaries)
    final_summary = summarize_text(combined, tokenizer, model)

    Path(SUMMARY_FILE).write_text(final_summary, encoding="utf-8")
    Path(CHUNK_SUMMARIES_FILE).write_text(
        json.dumps(chunk_summaries, indent=2), encoding="utf-8"
    )

    print("Done. Summary written to", SUMMARY_FILE)


if __name__ == "__main__":
    main()
