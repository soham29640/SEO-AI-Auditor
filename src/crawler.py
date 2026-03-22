import json
import re
from urllib.parse import urlparse

from crawl4ai import AsyncWebCrawler
from ddgs import DDGS
from bs4 import BeautifulSoup


# ---------------- Utilities ----------------

def get_domain(url):
    return urlparse(url).netloc.replace("www.", "")


def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def word_count(text):
    return len(text.split())


# ---------------- Backlink Count ----------------

async def estimate_backlinks(url: str):
    query = f'"{url}"'
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=30))
        return len(results)
    except:
        return 0


# ---------------- Extract Structured Content ----------------

def extract_main_content(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["nav", "header", "footer", "aside", "script", "style", "noscript"]):
        tag.decompose()

    headings = []
    paragraphs = []

    for tag in soup.find_all(["h1", "h2", "h3"]):
        text = clean_text(tag.get_text())
        if len(text) > 5:
            headings.append(text)

    for tag in soup.find_all("p"):
        text = clean_text(tag.get_text())
        if len(text) > 60:
            paragraphs.append(text)

    content = " ".join(paragraphs)

    return headings, content


# ---------------- Search Top 10 URLs ----------------

def get_top_urls(keyword: str, limit: int = 10):
    urls = []
    with DDGS() as ddgs:
        results = ddgs.text(keyword, max_results=limit)
        for r in results:
            urls.append(r["href"])
    return urls


# ---------------- MAIN FUNCTION ----------------
async def crawl(keyword: str = None, url: str = None):

    response_data = {}

    # =========================
    # CASE 1: If URL provided
    # =========================
    if url:
        async with AsyncWebCrawler() as crawler:
            page = await crawler.arun(url)

        if page:
            headings, content = extract_main_content(page.html)
            wc = word_count(content)
            backlinks = await estimate_backlinks(url)
            clean_content = clean_text(" ".join(headings) + " " + content)

            response_data["url_analysis"] = {
                "url": url,
                "word_count": wc,
                "backlinks_estimated": backlinks,
                "clean_text": clean_content
            }
        else:
            response_data["url_analysis"] = {
                "error": "Failed to crawl URL"
            }

    # =========================
    # CASE 2: If Keyword provided
    # =========================
    if keyword:
        extracted_data = []
        urls = get_top_urls(keyword, 25)

        async with AsyncWebCrawler() as crawler:
            pages = await crawler.arun_many(urls)

            for page in pages:
                if not page:
                    continue

                headings, content = extract_main_content(page.html)
                wc = word_count(content)

                if wc < 200:
                    continue

                backlinks = await estimate_backlinks(page.url)

                extracted_data.append({
                    "url": page.url,
                    "domain": get_domain(page.url),
                    "title": page.metadata.get("title") if page.metadata else None,
                    "meta_description": page.metadata.get("description") if page.metadata else None,
                    "headings": headings[:20],
                    "word_count": wc,
                    "content": content[:5000],
                    "backlinks_estimated": backlinks,
                    "clean_text": clean_text(" ".join(headings) + " " + content)
                })

        extracted_data.sort(
            key=lambda x: x["word_count"] + x["backlinks_estimated"] * 20,
            reverse=True
        )

        # Save JSON file
        with open("data/crawl_results.json", "w", encoding="utf-8") as f:
            json.dump(extracted_data, f, indent=2, ensure_ascii=False)

        response_data["keyword_analysis"] = {
            "message": "Keyword crawl completed and data saved to crawl_results.json"
        }

    # =========================
    # If nothing provided
    # =========================
    if not response_data:
        return {"error": "Provide keyword or url"}

    return response_data