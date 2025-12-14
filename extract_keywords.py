"""
Alright. Keyword Extraction — clean, practical, and interview-ready.

🟢 Keyword Extraction (NLP Task)
1️⃣ What is it?

Goal:
Automatically extract the most important words/phrases from a document that summarize its content.

Example:

Text: "Natural Language Processing is used in chatbots and search engines."
Keywords → ["natural language processing", "chatbots", "search engines"]


This is unsupervised (no labels).

2️⃣ Input Filefrom sklearn.feature_extraction.text import TfidfVectorizer

docs = [
    "Natural language processing enables machines to understand text",
    "Keyword extraction is a common NLP task",
    "TF IDF is widely used in information retrieval"
]

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
    max_features=20
)

X = vectorizer.fit_transform(docs)

feature_names = vectorizer.get_feature_names_out()
scores = X.toarray()[0]

keywords = sorted(
    zip(feature_names, scores),
    key=lambda x: x[1],
    reverse=True
)[:5]

print(keywords)


input.txt

Natural Language Processing enables machines to understand human language.
It is widely used in chatbots, search engines, and sentiment analysis systems.

8️⃣ Output Example
["natural language processing",
 "chatbots",
 "search engines",
 "sentiment analysis",
 "keyword extraction"]
"""

