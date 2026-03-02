from ddgs import DDGS

keyword = input("Enter keyword: ")

with DDGS() as ddgs:
    results = list(ddgs.text(keyword, max_results=30))  

bad_sites = ["tiktok", "pinterest", "youtube", "gettyimages"]

urls = []
for r in results:
    url = r["href"]
    if any(b in url for b in bad_sites):
        continue
    urls.append(url)
    if len(urls) == 10:   
        break

print("URLs to crawl:", urls)