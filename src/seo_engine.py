from src.crawler import crawl
from src.numerical_feature_extraction import content_strength_report
from src.similarity import semantic_seo_report
from src.topic_modeling import seo_intent_analysis
from src.tfidf import seo_keyword_gap_analysis
from src.ner import entity_seo_analysis

async def submit(keyword: str, url: str):
    result = await crawl(keyword, url)
    return result["url_analysis"]["url"],content_strength_report(result["url_analysis"]["word_count"],result["url_analysis"]["backlinks_estimated"]),semantic_seo_report(result["url_analysis"]["clean_text"]),seo_intent_analysis(result["url_analysis"]["clean_text"]),seo_keyword_gap_analysis(result["url_analysis"]["clean_text"]),entity_seo_analysis(result["url_analysis"]["clean_text"])
