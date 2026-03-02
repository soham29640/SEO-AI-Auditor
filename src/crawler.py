import json
import asyncio
import re
from urllib.parse import urlparse

from crawl4ai import AsyncWebCrawler
from ddgs import DDGS
from duck_duck_go import urls
from bs4 import BeautifulSoup


# ---------------- Domain ----------------
def get_domain(url):
    return urlparse(url).netloc.replace("www.", "")


# ---------------- Clean Text ----------------
def clean_text(text):
    if not text:
        return ""

    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ---------------- Detect Block Pages ----------------
def is_block_page(title, headings, content):
    signals = [
        "blocked",
        "access denied",
        "verify you are human",
        "captcha",
        "cloudflare",
        "bot protection",
        "enable javascript"
    ]

    text = (
        (title or "") +
        " " +
        " ".join(headings or []) +
        " " +
        content[:500]
    ).lower()

    return any(s in text for s in signals)


# ---------------- Extract Main Content ----------------
def extract_main_content(html):
    soup = BeautifulSoup(html, "html.parser")

    # remove junk areas
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

    return headings, paragraphs, content


# ---------------- Word Count ----------------
def word_count(text):
    return len(text.split())


# ---------------- Backlinks (Async) ----------------
async def estimate_backlinks(url):
    query = f'"{url}"'
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=30))
        return len(results)
    except:
        return 0


# ---------------- Main Crawl ----------------
async def crawl():

    extracted_data = []

    # remove duplicate urls
    unique_urls = list(set(urls))

    async with AsyncWebCrawler() as crawler:
        pages = await crawler.arun_many(unique_urls)

        for page in pages:
            if not page:
                continue

            headings = []
            paragraphs = []
            content = ""

            # try Crawl4AI extraction
            if page.extracted_content:
                paragraphs = page.extracted_content.get("paragraphs", [])
                headings = page.extracted_content.get("headings", [])

            # fallback to BeautifulSoup
            if not paragraphs or len(paragraphs) < 3:
                h, p, c = extract_main_content(page.html)
                headings = h
                paragraphs = p
                content = c
            else:
                cleaned_paragraphs = [
                    clean_text(p) for p in paragraphs if len(p) > 60
                ]
                content = " ".join(cleaned_paragraphs)

            title = page.metadata.get("title") if page.metadata else None

            # skip blocked pages
            if is_block_page(title, headings, content):
                print("Blocked page skipped:", page.url)
                continue

            wc = word_count(content)

            # skip thin content
            if wc < 200:
                continue

            backlinks = await estimate_backlinks(page.url)

            data = {
                "url": page.url,
                "domain": get_domain(page.url),
                "title": title,
                "meta_description": page.metadata.get("description") if page.metadata else None,
                "headings": headings[:20],
                "word_count": wc,
                "content": content[:5000],
                "backlinks_estimated": backlinks
            }

            extracted_data.append(data)

    # sort by quality
    extracted_data.sort(
        key=lambda x: x["word_count"] + x["backlinks_estimated"] * 20,
        reverse=True
    )

    with open("data/crawl_results.json", "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=2, ensure_ascii=False)

    print("\nSaved results to crawl_results.json")


asyncio.run(crawl())