from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
import json

# ---------------- USER INPUT (Company Content) ----------------
query =  "The 11 best SEO tools The 11 best SEO tools What is an SEO tool? What makes the best SEO tool? The best SEO tools at a glance Best AI assistant tool for SEO seoClarity (Web) Best SEO tool for AI integration Surfer (Web) Best SEO tool for beginners Mangools (Web) Best SEO tool for rank tracking Semrush (Web) Send Slack channel messages for completed SEMrush site audits Schedule daily site audit campaign re-crawls in SEMrush with Schedule by Zapier Generate overview reports in SEMrush when site audits are completed in SEMrush Best tool for SEO audits SEOptimer (Web) Best SEO tool for competitor research Ahrefs (Web) We independently review every app we recommend in our best apps lists. When you click some of the links on this page, we may earn a commission. Learn more. For some jobs, you can get by purely on your own cunning, physical abilities, or ambition alone. SEO marketer is not one of those jobs. Marketers like me can't do what they do without the right tools—tools that help us track performance metrics, diagnose problems, suggest improvements, report on progress, and automate the little things we don't have time to do a hundred times a day. I sifted through a ton of SEO software options (including ones I use regularly) to find what I think are the best SEO tools around. Here's what I found. I define an SEO tool as any software you can use to improve some aspect of a search engine optimization campaign. These tools can serve many different functions, including search query analytics, reporting automation, AI-driven content optimization recommendations, and website performance analysis. This gets tricky when you consider how many types of software marketers use for specific aspects of SEO. To try to keep some semblance of a level playing field, I excluded products that are narrowly focused on just one or two niche SEO use cases, like Moz's handy title tag tool. Instead, I focused on products that could fit into one of four distinct SEO product categories. SEO audit tools: These tools are designed primarily to perform analysis of one or more metrics related to search engine optimization efforts. Keyword research tools: The primary purpose of these tools is reporting on the search metrics of keywords or helping identify keywords to target. These don't necessarily measure ranking performance for specific webpages or domains. Rank trackers: Nearly all SEO rank trackers can perform general keyword research, but their main function is monitoring how well specific webpages or domains rank for individual keywords. They also tend to include suites of other tools for SEO-related tasks, though not as many as all-in-one tools. All-in-one tools: Similar to rank trackers, all-in-one SEO tools have many features, but their range of tools is more comprehensive. They can make tools from the other categories redundant and tend to include advanced features like automation and AI. I was able to dig into a number of tools myself, but I wasn't able to personally test each of them. When I couldn't, I looked to firsthand accounts from real users, software demos, aggregated reviews, and Reddit forums to fill in the blanks. Our best apps roundups are written by humans who've spent much of their careers using, testing, and writing about software. Unless explicitly stated, we spend dozens of hours researching and testing apps, using each app as it's intended to be used and evaluating it against the criteria we set for the category. We're never paid for placement in our articles from any app or for links to any site—we value the trust readers put in us to offer authentic evaluations of the categories and apps we review. For more details on our process, read the full rundown of how we select apps to feature on the Zapier blog. Since SEO tools can fall into distinct categories, nailing down what makes them great is a little complicated. To score them as objectively as possible, I reviewed dozens of products and whittled down a list of quality criteria that could apply to any category. SEO-centric functionality: Each tool has to have functionality that relates to some element of search engine optimization. They should fit into one of the categories above by specializing in a function like keyword analysis, on-page performance troubleshooting, website performance reporting, content ideation, or competitor analysis. Value: How well does the price represent the quality of the product? Tools with specific use cases should be effective enough to justify subscriptions for users with more comprehensive tools, just as comprehensive tools should have extensive feature suites, and paid tools in general should be more useful than free options. User experience: How easy is the tool to integrate, learn, and use? The learning curve should be low enough for users to reliably access any feature they need in complex tools without resorting to more familiar, less functional tools. Integrations: Since digital marketers tend to use many different software products, integration is key for SEO tools. Users should be able to integrate these tools readily into common platforms for related tasks like meetings, scheduling, reporting, and customer relationship management. In a sea of niche SEO products, seoClarity is about as close to an all-in-one tool as it gets. With a wide range of both general SEO and content optimization features and an AI assistant, it can likely replace several other tools for many users. On the SEO analysis end, seoClarity does a lot of what these other tools do. It offers rank monitoring, search trend insights, actionable diagnostic insights, pe"

# ---------------- LOAD SERP DATA ----------------
path = "data/crawl_results_with_clean_text.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)
corpus = df["clean_text"].tolist()

# ---------------- LOAD MODEL ----------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------- CREATE EMBEDDINGS ----------------
print("\nGenerating embeddings...")

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

# ---------------- PRINT REPORT ----------------
print("\n================ SEMANTIC SEO REPORT ================\n")

print(f"Semantic Similarity Score: {similarity_percent:.2f}%")
print(f"Grade: {grade}")
print(f"Alignment Level: {level}")

# ---------------- INTERPRETATION ----------------
print("\n📊 Interpretation:")

if grade == "A":
    print("- Your content strongly matches SERP semantic space.")
    print("- Focus on differentiation and authority signals.")
    print("- Improve UX, trust signals, and backlinks.")

elif grade == "B":
    print("- Your content aligns well with competitors.")
    print("- Expand deeper feature explanations.")
    print("- Add structured comparisons and FAQs.")

elif grade == "C":
    print("- Your content partially matches ranking pages.")
    print("- Expand subtopics covered by top competitors.")
    print("- Add richer tool comparisons and examples.")
    print("- Improve topical completeness.")

else:
    print("- Your content is semantically far from SERP leaders.")
    print("- Re-structure content around dominant SERP themes.")
    print("- Add missing sections and improve depth.")
    print("- Study top-ranking competitors more closely.")

# ---------------- INDIVIDUAL COMPETITOR SIMILARITY ----------------
print("\n📈 Top 3 Closest Competitors:")

individual_scores = []

for i, emb in enumerate(corpus_embeddings):
    s = float(np.dot(query_embedding, emb) * 100)
    individual_scores.append((df.iloc[i]["url"], s))

individual_scores.sort(key=lambda x: x[1], reverse=True)

for url, s in individual_scores[:3]:
    print(f"{url} → {s:.2f}% similarity")

# ---------------- POSITION RANK ----------------
all_scores = [s for _, s in individual_scores]
better_than = sum(1 for s in all_scores if similarity_percent > s)

percentile = (better_than / len(all_scores)) * 100

print(f"\n🏁 You are more semantically aligned than {percentile:.2f}% of competitors.")

print("\n======================================================\n")