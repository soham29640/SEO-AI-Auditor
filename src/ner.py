import spacy
import pandas as pd
import json
from model.report_generator import report_generator_for_ner


def entity_seo_analysis(query: str):

    nlp = spacy.load("en_core_web_sm")

    data_path = "data/crawl_results.json"

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # ---------------- Entity Extraction ----------------
    def extract_entities(text):
        doc = nlp(text)

        entities = [
            ent.text.lower().strip()
            for ent in doc.ents
            if ent.label_ in ["ORG", "PRODUCT", "PERSON", "GPE"]
        ]

        return list(set(entities))

    # ---------------- Competitor Entities ----------------
    df["entities"] = df["clean_text"].apply(extract_entities)

    competitor_entities = set()

    for ent_list in df["entities"]:
        competitor_entities.update(ent_list)

    # ---------------- Query Entities ----------------
    query_entities = set(extract_entities(query))

    missing_entities = competitor_entities - query_entities
    present_entities = competitor_entities.intersection(query_entities)

    if len(competitor_entities) > 0:
        coverage_score = (len(present_entities) / len(competitor_entities)) * 100
    else:
        coverage_score = 0

    # ---------------- Severity ----------------
    if coverage_score >= 70:
        severity = "Strong"

    elif coverage_score >= 40:
        severity = "Moderate"

    else:
        severity = "Weak"

    # ---------------- Final Report ----------------
    report = {
        "total_competitor_entities": len(competitor_entities),
        "entities_covered": len(present_entities),
        "entities_missing": len(missing_entities),
        "entity_coverage_score_percent": round(coverage_score, 2),
        "severity_level": severity,
        "covered_entities_sample": list(present_entities)[:15],
        "missing_entities_sample": list(missing_entities)[:15]
    }

    return report_generator_for_ner(report)