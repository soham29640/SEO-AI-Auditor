from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import json
from model.report_generator import report_generator_for_tfidf


def seo_keyword_gap_analysis(query: str):

    tfidf = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        stop_words="english",
        sublinear_tf=True,
        lowercase=True,
        min_df=2,
        max_df=0.85,
        token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z]+\b"
    )

    data_path = "data/crawl_results.json"

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    corpus = df["clean_text"].tolist()

    tfidf_matrix = tfidf.fit_transform(corpus)
    feature_names = tfidf.get_feature_names_out()

    # -------- Extract important SERP keywords --------
    def get_top_keywords(doc_index, top_n=50):
        row = tfidf_matrix[doc_index].toarray()[0]
        top_indices = row.argsort()[-top_n:][::-1]
        return [feature_names[i] for i in top_indices]

    top_keywords = get_top_keywords(0)

    query_lower = query.lower()

    present = []
    missing = []

    for keyword in top_keywords:
        if keyword in query_lower:
            present.append(keyword)
        else:
            missing.append(keyword)

    total_keywords = len(top_keywords)
    coverage = len(present) / total_keywords * 100

    # -------- Severity --------
    if coverage >= 75:
        severity = "Low"
    elif coverage >= 50:
        severity = "Moderate"
    else:
        severity = "High"

    report = {
        "total_keywords_analyzed": total_keywords,
        "keywords_present_count": len(present),
        "keywords_missing_count": len(missing),
        "coverage_score_percent": round(coverage, 2),
        "gap_severity": severity,
        "present_keywords": present,
        "missing_keywords_top20": missing[:20],
    }

    return report_generator_for_tfidf(report)