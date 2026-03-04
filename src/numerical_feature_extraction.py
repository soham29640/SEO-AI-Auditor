import json
from model.report_generator import report_generator_for_numerical_feature_extraction

def content_strength_report(
        your_word_count=0,
        your_backlinks=0
    ):
 
    # ---------------- LOAD SERP DATA ----------------
    serp_file="data/crawl_results.json"
    with open(serp_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ---------------- SERP AVERAGES ----------------
    avg_count = sum(row.get("word_count", 0) for row in data) / len(data)
    avg_backlink = sum(row.get("backlinks_estimated", 0) for row in data) / len(data)

    # ---------------- CALCULATIONS ----------------
    word_diff_percent = (your_word_count / avg_count) * 100
    backlink_diff_percent = (your_backlinks / avg_backlink) * 100

    report = {
        "serp_avg_word_count": round(avg_count, 0),
        "your_word_count": your_word_count,
        "content_depth_score_percent": round(word_diff_percent, 2),

        "serp_avg_backlinks": round(avg_backlink, 0),
        "your_backlinks": your_backlinks,
        "authority_score_percent": round(backlink_diff_percent, 2)
    }

    return report_generator_for_numerical_feature_extraction(word_diff_percent,backlink_diff_percent)