"""
Perfect. Let’s do CORPUS-LEVEL text statistics — this is EDA at a professional level (what seniors actually do before modeling).

🟢 Corpus-Level Text Statistics

Corpus-level ≠ single document
Here we analyze patterns across the entire dataset.

1️⃣ Typical Input (Corpus)
corpus/
 ├── doc1.txt
 ├── doc2.txt
 ├── doc3.txt
 ├── doc4.txt


or a CSV with many rows.

2️⃣ What Corpus-Level Stats Answer

Is my dataset biased?

Are documents too short / too long?

Is vocabulary rich or repetitive?

Will TF-IDF or Transformers work better?

Is there spam / boilerplate?

3️⃣ Core Corpus-Level Statistics (Must-Know)
🔹 Size & Length Distribution
Stat	Why
#documents	Dataset scale
Avg / median length	Model choice
Min / max length	Outliers
Length histogram	Padding strategy
🔹 Vocabulary Growth
Stat	Why
Total vocab size	Coverage
Vocab growth curve	Data saturation
Avg vocab per doc	Diversity
🔹 Lexical Diversity (Corpus)
Stat	Meaning
Global TTR	Overall diversity
Avg doc TTR	Per-doc richness
Hapax ratio	Noise
🔹 Frequency Distribution
Stat	Why
Zipf slope	Natural language sanity
Top-k words	Dataset theme
Long-tail size	Rare tokens
🔹 Redundancy & Duplication
Stat	Why
Duplicate documents	Data leakage
Near-duplicate ratio	Copy/paste
Boilerplate text	SEO / spam
🔹 Quality & Noise Indicators
Stat	Detects
Avg stopword ratio	Signal vs noise
URL / email density	Spam
Digit ratio	IDs, prices
Uppercase ratio	Shouting
🔹 Label-Aware Stats (if supervised)
Stat	Why
Class imbalance	Metric choice
Avg length per class	Bias
Vocab overlap across classes	Separability
"""
from pathlib import Path
import re
from collections import Counter
import numpy as np

docs = []
for f in Path("corpus").glob("*.txt"):
    docs.append(f.read_text(encoding="utf-8"))

# Tokenize
tokenized = [re.findall(r"\b\w+\b", d.lower()) for d in docs]

doc_lengths = [len(t) for t in tokenized]
vocab = set(w for doc in tokenized for w in doc)

# Vocabulary growth
vocab_growth = []
seen = set()
for doc in tokenized:
    seen.update(doc)
    vocab_growth.append(len(seen))

# Frequencies
global_freq = Counter(w for doc in tokenized for w in doc)

stats = {
    "num_docs": len(docs),
    "avg_doc_length": np.mean(doc_lengths),
    "median_doc_length": np.median(doc_lengths),
    "min_doc_length": min(doc_lengths),
    "max_doc_length": max(doc_lengths),
    "global_vocab_size": len(vocab),
    "hapax_ratio": sum(1 for w, c in global_freq.items() if c == 1) / len(global_freq),
    "top_words": global_freq.most_common(10)
}

for k, v in stats.items():
    print(k, "→", v)

"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vec = TfidfVectorizer(stop_words="english").fit_transform(docs)
sim = cosine_similarity(vec)

duplicate_pairs = [(i, j) for i in range(len(docs))
                   for j in range(i+1, len(docs)) if sim[i, j] > 0.9]

print("Near-duplicate pairs:", duplicate_pairs)
"""
