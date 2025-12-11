from transformers import pipeline
import os

# Choose your weapon (uncomment the one you want)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")                  # Classic, very good
# summarizer = pipeline("summarization", model="google/pegasus-xsum")                    # Great for short punchy summaries
# summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")          # Fast & small
# summarizer = pipeline("summarization", model="google/long-t5-tglobal-base")           # Excellent on long texts (up to 16k tokens)

def summarize_file(input_file, output_file=None):
    if output_file is None:
        output_file = input_file.replace(".txt", "_summary.txt")

    with open(input_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    print(f"\nProcessing {input_file} ({len(lines)} paragraph(s))")
    summaries = []

    for i, text in enumerate(lines):
        # Auto-adjust length based on input size
        input_length = len(text.split())
        max_len = min(250, max(30, input_length // 3))
        min_len = min(30, max_len // 2)

        summary = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)[0]["summary_text"]
        print(f"Paragraph {i+1}: {input_length} → {len(summary.split())} words")
        summaries.append(f"[{i+1}] {summary}\n")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(summaries))

    print(f"Summary saved to {output_file}\n")

# Run on all files
files = [
    "summary_short_news.txt",
    "summary_medium_reviews.txt",
    "summary_long_article.txt",
    "summary_very_long_report.txt"
]

for f in files:
    if os.path.exists(f):
        summarize_file(f)
    else:
        print(f"File not found: {f}")