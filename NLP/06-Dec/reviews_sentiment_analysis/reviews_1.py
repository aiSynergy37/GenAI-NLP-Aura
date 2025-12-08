'''
reading files
✔️ text cleaning
✔️ preprocessing
✔️ transformations
✔️ embeddings
✔️ feature engineering
✔️ building 2 small NLP models
✔️ evaluation


Text Preprocessing (Implement Your Own Pipeline)

Steps you must implement:

✔️ Lowercasing
✔️ Remove punctuation
✔️ Remove numbers
✔️ Normalize multiple spaces
✔️ Remove stopwords
✔️ Apply stemming or lemmatization (choose one)
✔️ Tokenize
3️⃣ Create Two Representations
A) Bag-of-Words (CountVectorizer)

Unigrams only

Limit vocabulary to top 5000 words

B) TF-IDF Representation

Unigrams + bigrams

Limit vocabulary to top 8000 features

4️⃣ Build Two Models
➤ Model 1: Logistic Regression (baseline)

'''
import re
import json
import nltk
import string
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

stopwords_set = set(stopwords.words("english"))
stemmer = PorterStemmer()

clean_rows = []

df = pd.read_csv("output.csv", header=None, names=["user", "rating", "review"])
print(df.head())

'''
with open("reviews.txt") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 3:
            continue

        user, rating, review = parts
        clean_rows.append({
            "user": user,
            "rating": int(rating),
            "review": review
        })


# --- Write cleaned JSONL ---
with open("clean_reviews.jsonl", "w") as out:
    for row in clean_rows:
        out.write(json.dumps(row) + "\n")


# ------ TEXT CLEANING FUNCTIONS ------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"\d+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()

    tokens = text.split()
    tokens = [t for t in tokens if t not in stopwords_set]
    tokens = [stemmer.stem(t) for t in tokens]
    return " ".join(tokens)


texts = [clean_text(r["review"]) for r in clean_rows]
labels = [1 if r["rating"] >= 4 else 0 for r in clean_rows]


# ------ VECTORIZERS ------
bow_vec = CountVectorizer(max_features=5000)
tfidf_vec = TfidfVectorizer(max_features=8000, ngram_range=(1, 2))

X_bow = bow_vec.fit_transform(texts)
X_tfidf = tfidf_vec.fit_transform(texts)

# ------ SPLIT DATA ------
X_train, X_test, y_train, y_test = train_test_split(X_tfidf, labels, test_size=0.2, random_state=42)

# ------ MODELS ------
logreg = LogisticRegression(max_iter=500)
logreg.fit(X_train, y_train)

nb = MultinomialNB()
nb.fit(X_train, y_train)

# ------ EVALUATION ------
pred_logreg = logreg.predict(X_test)
pred_nb = nb.predict(X_test)

rep_logreg = classification_report(y_test, pred_logreg)
rep_nb = classification_report(y_test, pred_nb)

with open("evaluation_report.txt", "w") as out:
    out.write("LOGISTIC REGRESSION\n")
    out.write(rep_logreg + "\n")
    out.write("NAIVE BAYES\n")
    out.write(rep_nb + "\n")
'''