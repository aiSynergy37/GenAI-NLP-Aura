"""
spam_pipeline.py

NLP pipeline:
- Read emails_raw.txt
- Clean & preprocess
- TF-IDF features
- Train Logistic Regression, Linear SVM, Naive Bayes
- Evaluate & save artifacts
"""

import re
import json
import string
import joblib
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, confusion_matrix


DATA_PATH = Path("emails_raw.txt")


def load_raw_emails(path: Path):
    texts = []
    labels = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = re.match(r"\[(SPAM|HAM)\]\s*(.*)", line)
            if not m:
                continue
            label_str, text = m.groups()
            label = 1 if label_str == "SPAM" else 0
            labels.append(label)
            texts.append(text)
    return texts, labels


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"<[^>]+>", " ", text)  # HTML tags
    text = re.sub(r"http\S+|www\.\S+", " ", text)  # URLs
    text = re.sub(r"\d+", " ", text)  # numbers
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text


def main():
    texts_raw, labels = load_raw_emails(DATA_PATH)
    labels = np.array(labels)

    texts_clean = [clean_text(t) for t in texts_raw]

    # Save cleaned dataset
    with open("emails_clean.jsonl", "w", encoding="utf-8") as out:
        for t, lbl in zip(texts_clean, labels):
            out.write(json.dumps({"text": t, "label": int(lbl)}) + "\n")

    # TF-IDF features (1–3 grams)
    vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1, 3))
    X = vectorizer.fit_transform(texts_clean)

    X_train, X_test, y_train, y_test = train_test_split(
        X, labels, test_size=0.2, random_state=42
    )

    models = {
        "logreg": LogisticRegression(max_iter=1000),
        "svm": LinearSVC(),
        "nb": MultinomialNB(),
    }

    reports = {}
    cms = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        reports[name] = classification_report(y_test, y_pred, digits=4)
        cms[name] = confusion_matrix(y_test, y_pred).tolist()

        joblib.dump(model, f"{name}_spam_model.pkl")

    joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

    with open("metrics_report.txt", "w", encoding="utf-8") as out:
        for name in models:
            out.write(f"=== {name.upper()} ===\n")
            out.write(reports[name] + "\n")
            out.write("Confusion matrix (rows=true, cols=pred):\n")
            out.write(str(cms[name]) + "\n\n")


if __name__ == "__main__":
    main()
