"""
Given any large .txt file (e.g. a novel or log dump), compute and print:

Total lines, words, characters
Top 10 most frequent words (case-insensitive, ignore punctuation)
Average word length
Number of lines containing digits
Longest word and its length
Vocabulary size (unique words)

Bonus One-liner Challenges (They LOVE these)

Read a file and print only lines that contain a valid IPv4 address
Reverse each line of a file and write to reversed.txt
Find all lines where a word appears more than 3 times
Replace all dates in format DD/MM/YYYY → YYYY-MM-DD across multiple files
"""

import re
from collections import Counter

def analyze(path):
    freq = Counter()
    vocab = set()
    longest = ""

    lines = 0
    words = 0
    chars = 0
    digit_lines = 0

    word_re = re.compile(r"[A-Za-z0-9']+")

    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            lines += 1
            chars += len(line)

            has_digit = any(c.isdigit() for c in line)
            digit_lines += has_digit

            ws = word_re.findall(line.lower())
            #print(ws)
            words += len(ws)

            freq.update(ws)
            vocab.update(ws)

            if ws:
                w = max(ws, key=len)
                #print(w)
                if len(w) > len(longest):
                    longest = w

    avg_len = sum(len(w) * c for w, c in freq.items()) / words if words else 0

    return {
        "lines": lines,
        "words": words,
        "characters": chars,
        "top10": freq.most_common(10),
        "avg_word_len": round(avg_len, 2),
        "digit_lines": digit_lines,
        "longest_word": (longest, len(longest)),
        "vocab_size": len(vocab),
    }


# Example
analyze("novels.txt")
