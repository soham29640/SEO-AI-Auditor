from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
import json
from model.report_generator import report_generator_for_similarity

def semantic_seo_report(
        query: str,
):

    # ---------------- LOAD SERP DATA ----------------
    serp_file="data/crawl_results.json"
    with open(serp_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    corpus = df["clean_text"].tolist()

    # ---------------- LOAD MODEL ----------------
    model_name="all-MiniLM-L6-v2"
    model = SentenceTransformer(model_name)

    # ---------------- CREATE EMBEDDINGS ----------------
    corpus_embeddings = model.encode(corpus, normalize_embeddings=True)
    query_embedding = model.encode(query, normalize_embeddings=True)

    # ---------------- AVERAGE SERP EMBEDDING ----------------
    avg_corpus_embedding = np.mean(corpus_embeddings, axis=0)

    # ---------------- COSINE SIMILARITY ----------------
    score = np.dot(query_embedding, avg_corpus_embedding)
    similarity_percent = float(score * 100)

    # ---------------- GRADE SYSTEM ----------------
    if similarity_percent >= 85:
        grade = "A"
        level = "Excellent Semantic Alignment"

    elif similarity_percent >= 75:
        grade = "B"
        level = "Strong Alignment"

    elif similarity_percent >= 60:
        grade = "C"
        level = "Moderate Alignment"
    
    else:
        grade = "D"
        level = "Weak Alignment"
       
    # ---------------- INDIVIDUAL COMPETITOR SIMILARITY ----------------
    individual_scores = []

    for i, emb in enumerate(corpus_embeddings):
        s = float(np.dot(query_embedding, emb) * 100)
        individual_scores.append((df.iloc[i]["url"], s))

    individual_scores.sort(key=lambda x: x[1], reverse=True)

    top_competitors = [
        {"url": url, "similarity_percent": round(s, 2)}
        for url, s in individual_scores[:3]
    ]

    # ---------------- POSITION RANK ----------------
    all_scores = [s for _, s in individual_scores]
    better_than = sum(1 for s in all_scores if similarity_percent > s)
    percentile = (better_than / len(all_scores)) * 100

    # ---------------- FINAL REPORT ----------------
    report = {
        "semantic_similarity_percent": round(similarity_percent, 2),
        "grade": grade,
        "alignment_level": level,
        "better_than_percent_of_competitors": round(percentile, 2),
        "top_similar_competitors": top_competitors,
    }

    return report_generator_for_similarity(report)