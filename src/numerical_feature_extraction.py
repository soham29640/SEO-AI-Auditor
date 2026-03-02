import json

with open("data/crawl_results_with_clean_text.json", "r", encoding="utf-8") as f:
    data = json.load(f)

avg_count = sum(row.get("word_count", 0) for row in data) / len(data)

avg_backlink = sum(row.get("backlinks_estimated", 0) for row in data) / len(data)

print("avg count : ",avg_count,"\n""avg backlinks :",avg_backlink)