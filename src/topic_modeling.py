import pandas as pd
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import spacy

# ------------------- Load spaCy -------------------
nlp = spacy.load("en_core_web_sm")

# ------------------- Load Data -------------------
path = "data/crawl_results_with_clean_text.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# ------------------- Preprocessing -------------------
def preprocess(text):
    doc = nlp(text)
    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and token.is_alpha
    ]
    return " ".join(tokens)

df["processed_text"] = df["clean_text"].apply(preprocess)

# ------------------- Vectorization -------------------
vectorizer = CountVectorizer(
    stop_words="english",
    min_df=2,
    max_df=0.8
)

X = vectorizer.fit_transform(df["processed_text"])

# ------------------- LDA Model -------------------
lda = LatentDirichletAllocation(
    n_components=3,
    random_state=42
)

lda.fit(X)

feature_names = vectorizer.get_feature_names_out()

# ------------------- Print Topics -------------------
print("\n================ TOPIC KEYWORDS ================\n")

for topic_idx, topic in enumerate(lda.components_):
    top_indices = topic.argsort()[-5:][::-1]
    top_words = [feature_names[i] for i in top_indices]
    print(f"Topic {topic_idx}: {', '.join(top_words)}")

# ------------------- Assign Dominant Topic -------------------
doc_topics = lda.transform(X)
df["dominant_topic"] = doc_topics.argmax(axis=1)

# ------------------- Human-Readable Labels -------------------
topic_labels = {
    0: "Free SEO Tools",
    1: "Pricing / Plans",
    2: "Branded SEO Platforms"
}

df["topic_label"] = df["dominant_topic"].map(topic_labels)

# ------------------- Save Results -------------------
df.to_json(
    "data/topic_modeled_results.json",
    orient="records",
    indent=2
)

# ==============================================================
#                    COMPANY WEBSITE ANALYSIS
# ==============================================================

query =  "The 11 best SEO tools The 11 best SEO tools What is an SEO tool? What makes the best SEO tool? The best SEO tools at a glance Best AI assistant tool for SEO seoClarity (Web) Best SEO tool for AI integration Surfer (Web) Best SEO tool for beginners Mangools (Web) Best SEO tool for rank tracking Semrush (Web) Send Slack channel messages for completed SEMrush site audits Schedule daily site audit campaign re-crawls in SEMrush with Schedule by Zapier Generate overview reports in SEMrush when site audits are completed in SEMrush Best tool for SEO audits SEOptimer (Web) Best SEO tool for competitor research Ahrefs (Web) We independently review every app we recommend in our best apps lists. When you click some of the links on this page, we may earn a commission. Learn more. For some jobs, you can get by purely on your own cunning, physical abilities, or ambition alone. SEO marketer is not one of those jobs. Marketers like me can't do what they do without the right tools—tools that help us track performance metrics, diagnose problems, suggest improvements, report on progress, and automate the little things we don't have time to do a hundred times a day. I sifted through a ton of SEO software options (including ones I use regularly) to find what I think are the best SEO tools around. Here's what I found. I define an SEO tool as any software you can use to improve some aspect of a search engine optimization campaign. These tools can serve many different functions, including search query analytics, reporting automation, AI-driven content optimization recommendations, and website performance analysis. This gets tricky when you consider how many types of software marketers use for specific aspects of SEO. To try to keep some semblance of a level playing field, I excluded products that are narrowly focused on just one or two niche SEO use cases, like Moz's handy title tag tool. Instead, I focused on products that could fit into one of four distinct SEO product categories. SEO audit tools: These tools are designed primarily to perform analysis of one or more metrics related to search engine optimization efforts. Keyword research tools: The primary purpose of these tools is reporting on the search metrics of keywords or helping identify keywords to target. These don't necessarily measure ranking performance for specific webpages or domains. Rank trackers: Nearly all SEO rank trackers can perform general keyword research, but their main function is monitoring how well specific webpages or domains rank for individual keywords. They also tend to include suites of other tools for SEO-related tasks, though not as many as all-in-one tools. All-in-one tools: Similar to rank trackers, all-in-one SEO tools have many features, but their range of tools is more comprehensive. They can make tools from the other categories redundant and tend to include advanced features like automation and AI. I was able to dig into a number of tools myself, but I wasn't able to personally test each of them. When I couldn't, I looked to firsthand accounts from real users, software demos, aggregated reviews, and Reddit forums to fill in the blanks. Our best apps roundups are written by humans who've spent much of their careers using, testing, and writing about software. Unless explicitly stated, we spend dozens of hours researching and testing apps, using each app as it's intended to be used and evaluating it against the criteria we set for the category. We're never paid for placement in our articles from any app or for links to any site—we value the trust readers put in us to offer authentic evaluations of the categories and apps we review. For more details on our process, read the full rundown of how we select apps to feature on the Zapier blog. Since SEO tools can fall into distinct categories, nailing down what makes them great is a little complicated. To score them as objectively as possible, I reviewed dozens of products and whittled down a list of quality criteria that could apply to any category. SEO-centric functionality: Each tool has to have functionality that relates to some element of search engine optimization. They should fit into one of the categories above by specializing in a function like keyword analysis, on-page performance troubleshooting, website performance reporting, content ideation, or competitor analysis. Value: How well does the price represent the quality of the product? Tools with specific use cases should be effective enough to justify subscriptions for users with more comprehensive tools, just as comprehensive tools should have extensive feature suites, and paid tools in general should be more useful than free options. User experience: How easy is the tool to integrate, learn, and use? The learning curve should be low enough for users to reliably access any feature they need in complex tools without resorting to more familiar, less functional tools. Integrations: Since digital marketers tend to use many different software products, integration is key for SEO tools. Users should be able to integrate these tools readily into common platforms for related tasks like meetings, scheduling, reporting, and customer relationship management. In a sea of niche SEO products, seoClarity is about as close to an all-in-one tool as it gets. With a wide range of both general SEO and content optimization features and an AI assistant, it can likely replace several other tools for many users. On the SEO analysis end, seoClarity does a lot of what these other tools do. It offers rank monitoring, search trend insights, actionable diagnostic insights, pe"

# Preprocess query
query_processed = preprocess(query)

# Vectorize using trained vectorizer
query_vector = vectorizer.transform([query_processed])

# Get topic distribution
query_topic_dist = lda.transform(query_vector)

# Get dominant topic
query_dominant_topic = query_topic_dist.argmax(axis=1)[0]
query_topic_label = topic_labels.get(query_dominant_topic, "Unknown")

# ------------------- Generate Report -------------------

print("\n================ SEO INTENT ANALYSIS REPORT ================\n")

print("📌 Company Website Topic:")
print("→", query_topic_label)

# SERP Topic Distribution
print("\n📊 SERP Topic Distribution:")

serp_distribution = df["topic_label"].value_counts()

for topic, count in serp_distribution.items():
    print(f"{topic:<25} {count}")

# Dominant SERP Topic
dominant_serp_topic = serp_distribution.idxmax()

print("\n🎯 Dominant SERP Intent:")
print("→", dominant_serp_topic)

# Intent Alignment Check
if query_topic_label == dominant_serp_topic:
    print("\n✅ Your website matches dominant SERP intent.")
    print("Recommendation:")
    print("- Improve content depth")
    print("- Increase semantic keyword coverage")
    print("- Add internal linking and structured headings")
else:
    print("\n⚠️ Intent Misalignment Detected!")
    print(f"Google favors: {dominant_serp_topic}")
    print(f"Your page focuses on: {query_topic_label}")

    print("\n🔧 Improvement Recommendations:")

    if dominant_serp_topic == "Free SEO Tools":
        print("- Add educational sections explaining SEO tools")
        print("- Include free tool demos or comparisons")
        print("- Add FAQs about SEO tool usage")
        print("- Reduce heavy pricing-only focus")

    elif dominant_serp_topic == "Pricing / Plans":
        print("- Add detailed pricing tables")
        print("- Include feature comparison between plans")
        print("- Add testimonials and trust signals")
        print("- Highlight subscription benefits clearly")

    elif dominant_serp_topic == "Branded SEO Platforms":
        print("- Add detailed feature breakdown")
        print("- Compare with competitors (Semrush, Ahrefs, etc.)")
        print("- Include use-case examples")
        print("- Add case studies or performance metrics")

print("\n=============================================================\n")