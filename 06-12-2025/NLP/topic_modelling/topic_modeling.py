# Save as topic_modeling.py
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
import json

def run_topic_modeling(filename):
    with open(filename, "r", encoding="utf-8") as f:
        documents = [line.strip() for line in f if line.strip()]

    # Optional: remove very common/stop words more aggressively
    vectorizer = CountVectorizer(stop_words="english", min_df=2)

    topic_model = BERTopic(vectorizer_model=vectorizer, language="multilingual")  # works great even on Hinglish!
    topics, probs = topic_model.fit_transform(documents)

    print(f"\n=== {filename} ===")
    print(topic_model.get_topic_info().head(10))

    # Save detailed results
    result = {
        "topics": topic_model.get_topic_info().to_dict("records"),
        "representative_docs": topic_model.get_representative_docs(),
        "top_words": {topic: [word for word, _ in topic_model.get_topic(topic)[:10]] 
                      for topic in topic_model.get_topics() if topic != -1}
    }

    with open(f"topics_result_{filename.replace('.txt','')}.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Results saved for {filename}\n")

# Run on all files
for file in ["topics_easy_classic.txt", "topics_medium_reviews.txt", 
             "topics_hard_news.txt", "topics_veryhard_social.txt"]:
    run_topic_modeling(file)