import pandas as pd
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import spacy
from model.report_generator import report_generator_for_topic_modeling


def seo_intent_analysis(query: str):

    nlp = spacy.load("en_core_web_sm")

    data_path = "data/crawl_results.json"

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # ---------------- Preprocess ----------------
    def preprocess(text):
        doc = nlp(text)
        tokens = [
            token.lemma_
            for token in doc
            if not token.is_stop and token.is_alpha
        ]
        return " ".join(tokens)

    df["processed_text"] = df["clean_text"].apply(preprocess)

    # ---------------- Vectorization ----------------
    vectorizer = CountVectorizer(
        stop_words="english",
        min_df=2,
        max_df=0.8
    )

    X = vectorizer.fit_transform(df["processed_text"])

    # ---------------- LDA ----------------
    n_topics = 3

    lda = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=42
    )

    lda.fit(X)

    feature_names = vectorizer.get_feature_names_out()

    topics = {}

    for topic_idx, topic in enumerate(lda.components_):
        top_indices = topic.argsort()[-5:][::-1]
        top_words = [feature_names[i] for i in top_indices]
        topics[topic_idx] = top_words

    # ---------------- Assign topics ----------------
    doc_topics = lda.transform(X)
    df["dominant_topic"] = doc_topics.argmax(axis=1)

    # Label topics automatically
    topic_labels = {
        i: ", ".join(words[:2])
        for i, words in topics.items()
    }

    df["topic_label"] = df["dominant_topic"].map(topic_labels)

    # ---------------- Query Topic ----------------
    query_processed = preprocess(query)

    query_vector = vectorizer.transform([query_processed])

    query_topic_dist = lda.transform(query_vector)

    query_dominant_topic = query_topic_dist.argmax(axis=1)[0]

    query_topic_label = topic_labels.get(query_dominant_topic, "Unknown")

    # ---------------- SERP Topic Distribution ----------------
    serp_distribution = df["topic_label"].value_counts().to_dict()

    dominant_serp_topic = max(serp_distribution, key=serp_distribution.get)

    # ---------------- Save topic results ----------------
    df.to_json(
        "data/topic_modeled_results.json",
        orient="records",
        indent=2
    )

    # ---------------- Build report ----------------
    report = {
        "company_topic": query_topic_label,
        "dominant_serp_topic": dominant_serp_topic,
        "serp_topic_distribution": serp_distribution,
        "topic_keywords": topics,
    }

    return report_generator_for_topic_modeling(report)