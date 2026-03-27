# SEO AI Auditor

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-deployment%20ready-0078D4?logo=microsoftazure&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-AI%20Powered-4285F4?logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

> **An NLP-driven SEO intelligence engine** that benchmarks your webpage against the top 10 SERP competitors using semantic embeddings, topic modeling, named entity recognition, and content depth metrics — then delivers a composite SEO Score (0 – 100) with actionable, AI-generated insights powered by Google Gemini.

---

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Architecture](#architecture)
4. [Tech Stack](#tech-stack)
5. [Prerequisites](#prerequisites)
6. [Local Setup](#local-setup)
7. [Docker Deployment](#docker-deployment)
8. [Azure Deployment](#azure-deployment)
9. [API Reference](#api-reference)
10. [Project Structure](#project-structure)
11. [Contributing](#contributing)
12. [License](#license)

---

## Overview

SEO AI Auditor automates the tedious process of competitive SEO analysis. Given a target URL and a primary keyword, it:

- Crawls the target page and the top 10 organic SERP results automatically.
- Runs five independent NLP/ML analysis modules across all pages.
- Aggregates the results into a single **Final SEO Score**.
- Asks Google Gemini to generate human-readable, module-level improvement reports.

The entire pipeline is exposed as a single REST endpoint, making it trivial to integrate with content management systems, CI/CD pipelines, or internal tooling.

---

## Key Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Automated SERP Crawling** | Fetches top 10 competitor pages via DuckDuckGo — no API key required |
| 2 | **Semantic Similarity Scoring** | Measures content alignment using `SentenceTransformer` cosine similarity |
| 3 | **Topic Gap Detection** | LDA + KMeans clustering identifies themes you're missing |
| 4 | **Entity Coverage Analysis** | spaCy NER compares ORG, PRODUCT, PERSON, and GPE entity coverage |
| 5 | **Content Depth & Authority** | Word count and backlink metrics vs. SERP average |
| 6 | **AI-Generated Insights** | Google Gemini produces concise, actionable reports per module |
| 7 | **FastAPI REST Interface** | Clean async API with auto-generated OpenAPI/Swagger docs |
| 8 | **Streamlit Dashboard** | Interactive UI for non-technical users |
| 9 | **Container-First Design** | Docker & Docker Compose ready; Azure Container Apps compatible |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client / Streamlit UI                    │
└────────────────────────────┬────────────────────────────────────┘
                             │  POST /SEO report
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI  (app/main.py)                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SEO Engine  (src/seo_engine.py)                │
│                                                                 │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────────────┐  │
│  │  Crawler     │  │  Similarity   │  │  Topic Modeling      │  │
│  │  crawler.py  │  │  similarity.py│  │  topic_modeling.py   │  │
│  └──────────────┘  └───────────────┘  └──────────────────────┘  │
│  ┌──────────────┐  ┌───────────────┐                            │
│  │  NER         │  │  Depth /      │                            │
│  │  ner.py      │  │  Authority    │                            │
│  └──────────────┘  └───────────────┘                            │
└────────────────────────────┬────────────────────────────────────┘
                             │  Structured metrics
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│            Report Generator  (model/report_generator.py)        │
│                    ↕  Google Gemini API                         │
└─────────────────────────────────────────────────────────────────┘
```

### Analysis Pipeline

| Step | Module | Output |
|------|--------|--------|
| 1. Data Collection | `src/crawler.py` | Target page + top 10 SERP pages |
| 2. Semantic Analysis | `src/similarity.py` | Semantic Coverage Score |
| 3. Topic Modeling | `src/topic_modeling.py` | Topic Coverage Score |
| 4. Entity Coverage | `src/ner.py` | Entity Coverage Score |
| 5. Content Depth | `src/numerical_feature_extraction.py` | Depth Score + Authority Score |
| 6. AI Reports | `model/report_generator.py` | Per-module Gemini insights |

---

## Tech Stack

| Category | Libraries / Tools |
|----------|-------------------|
| Language | Python 3.10+ |
| API Framework | FastAPI, Uvicorn |
| UI | Streamlit |
| NLP & ML | SentenceTransformers, spaCy (`en_core_web_sm`), scikit-learn |
| Data | pandas, NumPy |
| Web Crawling | Crawl4ai, DDGS, BeautifulSoup, Playwright |
| AI Reports | Google Gemini API (`google-genai`) |
| Configuration | python-dotenv |
| Containerization | Docker, Docker Compose |
| Cloud Platform | Microsoft Azure (Container Apps / App Service) |

---

## Prerequisites

- **Python 3.10+**
- **Google Gemini API key** — [Get one here](https://aistudio.google.com/app/apikey)
- **Docker & Docker Compose** — required for containerized or cloud deployment
- **Azure CLI** — required for Azure deployment (`az` v2.50+)

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/soham29640/SEO-AI-Auditor.git
cd SEO-AI-Auditor
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install the spaCy language model

```bash
python -m spacy download en_core_web_sm
```

### 5. Install Playwright browsers

```bash
playwright install
```

### 6. Configure environment variables

Create a `.env` file in the `model/` directory:

```env
# model/.env
GEMINI_API_KEY=your_gemini_api_key_here
```

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

### 7. Start the API server

```bash
uvicorn app.main:app --loop asyncio
```

API available at → `http://localhost:8000`  
Interactive docs → `http://localhost:8000/docs`

---

## Docker Deployment

### Run with Docker Compose (recommended)

Before starting, ensure your `GEMINI_API_KEY` is available as an environment variable or add it to a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Then start the stack:

```bash
docker compose up --build
```

The application will be available at `http://localhost:8000`.

### Build and run manually

```bash
docker build -t seo-ai-auditor .
docker run -p 8000:8000 --env-file model/.env seo-ai-auditor
```

### Build for a specific platform (e.g., Azure / amd64)

```bash
docker build --platform=linux/amd64 -t seo-ai-auditor .
```

---

## Azure Deployment

This section covers deploying SEO AI Auditor to **Azure Container Apps** — a fully managed, serverless container platform ideal for API workloads.

### Prerequisites

- An active Azure subscription
- [Azure Container Registry (ACR)](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-get-started-azure-cli) created

### Step 1 — Set environment variables

```bash
RESOURCE_GROUP="rg-seo-ai-auditor"
LOCATION="eastus"
ACR_NAME="seoacr$(date +%s)"      # timestamp suffix ensures global uniqueness
CONTAINER_APP_ENV="seo-env"
CONTAINER_APP_NAME="seo-ai-auditor"
IMAGE_NAME="seo-ai-auditor:latest"
export GEMINI_API_KEY="your_gemini_api_key_here"
```

### Step 2 — Create a Resource Group

```bash
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION
```

### Step 3 — Create an Azure Container Registry

```bash
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled true
```

### Step 4 — Build and push the image to ACR

```bash
az acr build \
  --registry $ACR_NAME \
  --image $IMAGE_NAME \
  --platform linux/amd64 \
  .
```

> **Tip:** `az acr build` streams the Docker build directly into Azure — no local Docker daemon required.

### Step 5 — Create a Container Apps environment

```bash
az containerapp env create \
  --name $CONTAINER_APP_ENV \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION
```

### Step 6 — Retrieve ACR credentials

```bash
ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --query loginServer -o tsv)
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)
```

### Step 7 — Deploy the Container App

```bash
az containerapp create \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $CONTAINER_APP_ENV \
  --image "$ACR_LOGIN_SERVER/$IMAGE_NAME" \
  --registry-server $ACR_LOGIN_SERVER \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --target-port 8000 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 3 \
  --cpu 1.0 \
  --memory 2.0Gi \
  --secrets gemini-api-key="$GEMINI_API_KEY" \
  --env-vars GEMINI_API_KEY=secretref:gemini-api-key
```

### Step 8 — Retrieve the public URL

```bash
az containerapp show \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn \
  -o tsv
```

Your API will be live at `https://<fqdn>/docs`.

### Alternative: Azure App Service (Web App for Containers)

```bash
# Create an App Service plan (Linux)
az appservice plan create \
  --name seo-ai-plan \
  --resource-group $RESOURCE_GROUP \
  --is-linux \
  --sku B2

# Create the Web App
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan seo-ai-plan \
  --name seo-ai-auditor-app \
  --deployment-container-image-name "$ACR_LOGIN_SERVER/$IMAGE_NAME"

# Configure ACR credentials
az webapp config container set \
  --name seo-ai-auditor-app \
  --resource-group $RESOURCE_GROUP \
  --docker-registry-server-url "https://$ACR_LOGIN_SERVER" \
  --docker-registry-server-user $ACR_USERNAME \
  --docker-registry-server-password $ACR_PASSWORD

# Set the Gemini API key as an app setting
az webapp config appsettings set \
  --name seo-ai-auditor-app \
  --resource-group $RESOURCE_GROUP \
  --settings GEMINI_API_KEY="$GEMINI_API_KEY"
```

### Azure Cost Estimate

| Resource | SKU | Approx. monthly cost |
|----------|-----|----------------------|
| Container Apps (1 replica, 1 vCPU / 2 GiB, always-on) | Consumption | ~$45–55 |
| Azure Container Registry | Basic | ~$5 |
| **Total** | | **~$50–60 / month** |

> Costs are estimates for continuous operation in `eastus`. Container Apps on the Consumption plan scales to zero when idle, which can significantly reduce costs for low-traffic workloads. Use the [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/) for accurate estimates based on your expected traffic and region.

---

## API Reference

### Base URL

| Environment | URL |
|-------------|-----|
| Local | `http://localhost:8000` |
| Docker | `http://localhost:8000` |
| Azure | `https://<your-fqdn>` |

### Interactive Documentation

FastAPI auto-generates interactive API docs:

- **Swagger UI** → `GET /docs`
- **ReDoc** → `GET /redoc`

### Endpoint

#### `POST /SEO report`

Runs the full SEO analysis pipeline for the given URL and keyword.

**Request Body**

```json
{
  "keyword": "string",
  "url": "string"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `keyword` | string | ✅ | The primary search keyword to benchmark against |
| `url` | string | ✅ | The fully qualified URL of the page to audit |

**Example Request**

```bash
curl -X POST "http://localhost:8000/SEO%20report" \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "best running shoes",
    "url": "https://example.com/running-shoes"
  }'
```

**Example Response**

As example we take "Best WWE player" as keyword but as url we take WWE official website to show how this url is not alligned with the keyword and what to improve in report .

```json
[
  "https://www.wwe.com/superstars",
  "Content Depth Analysis\n• Severe content deficit: The page contains less than 10% of the information or topical coverage found in top-ranking competitors.\n• High risk of \"thin content\" labeling: The page likely fails to satisfy user intent or address common follow-up queries.\n• Poor topical relevance: Lack of depth suggests the page is missing key entities and semantic terms required to be seen as an authority on the subject.\n\nAuthority Analysis\n• Dominant off-page profile: With over 8x the average authority, the page possesses massive ranking power compared to its peers.\n• Brute-force ranking: Current visibility is likely sustained by domain strength and backlink equity rather than content merit.\n• Significant competitive advantage: The page has the \"trust\" needed to rank #1 easily if the content quality is improved.\n\nRanking Potential\n• Fragile positioning: The page is highly vulnerable to \"Helpful Content\" or quality-centric algorithm updates.\n• Underperformance: Despite massive authority, the content gap creates a \"ranking ceiling\" that prevents the page from reaching its full potential.\n• High volatility: Rankings may fluctuate significantly as Google balances authority signals against poor user experience metrics (e.g., high bounce rates).\n\nSEO Recommendations\n• Immediate content expansion: Conduct a gap analysis to identify and integrate missing subtopics, headings, and data points found in competitor pages.\n• Improve information density: Increase the word count and utility of the page to at least match the SERP average.\n• Leverage authority for long-tail: Use the high authority score to target more complex, high-volume keywords that competitors cannot rank for due to their lower link profiles.",
  "Semantic Alignment\n• The content demonstrates a significant gap in topical depth, missing several key sub-themes and entities that search engines expect for this query.\n• The current structure is fragmented, failing to establish the dense network of related concepts found in high-performing authority sites.\n• Substantial thematic omissions suggest the copy may be too general or focused on the wrong attributes of the subject matter.\n\nCompetitor Comparison\n• While the page outperforms the bottom half of the SERP, it falls notably short of the \"Gold Standard\" established by the top three ranking leaders.\n• Top competitors are successfully utilizing a richer vocabulary and more specific industry entities that this content currently lacks.\n• The gap between the page and the leaders indicates that the competition is providing a more comprehensive \"information journey\" for the user.\n\nRanking Impact\n• Weak semantic alignment acts as a performance ceiling, likely preventing the page from reaching the top five positions.\n• Search engines may struggle to categorize the page as a definitive resource, leading to lower relevance scores and diminished organic reach.\n• Low topical completeness increases the risk of higher bounce rates, as users find more exhaustive answers on competing sites.\n\nSEO Recommendations\n• Conduct a gap analysis of the top three competitors to identify missing \"Entity\" nodes, such as specific career milestones, technical terminology, or historical eras.\n• Expand the content to include highly relevant sub-topics that provide context, such as specialized techniques, championship histories, or peer influence.\n• Improve the internal linking architecture by connecting this page to broader \"hub\" pages to strengthen its position within the site's topical cluster.\n• Implement specific schema markup to explicitly define the relationships between the subjects mentioned and their significance within the industry niche.",
  "**SERP Intent Overview**\n• The primary search intent is centered on comparisons and performance quality, dominated by Topic 2 (\"great, like,\" \"main,\" \"work,\" \"flair\").\n• There is a secondary, nearly equal intent focused on aesthetic or regional characteristics, represented by Topic 0 (\"great, style,\" \"american\").\n• A minor segment of the SERP addresses industry-specific business news related to professional wrestling (\"smackdown,\" \"aew\").\n\n**Content Intent Match**\n• The page (\"great, style\") aligns with the second most prominent intent in the SERP distribution (Topic 0).\n• While the content is relevant to 8 out of 20 top-ranking instances, it is not currently aligned with the absolute dominant intent (Topic 2), which holds 9 instances.\n• The match is strong but slightly skewed toward \"style\" rather than the \"work/main\" focus favored by the top intent.\n\n**Ranking Implications**\n• The page is well-positioned to compete for the secondary cluster of high-ranking results.\n• To achieve a #1 position, the content may struggle if it ignores the \"work\" and \"flair\" keywords that define the primary intent.\n• The high density of \"great, style\" in the SERP (8/20) suggests a \"split intent\" SERP where multiple angles can rank.\n\n**Optimization Suggestions**\n• Incorporate keywords from the dominant topic, specifically \"main,\" \"work,\" and \"flair,\" to bridge the gap between style and performance.\n• Shift the narrative from purely aesthetic \"style\" to include comparative \"like\" elements to satisfy the \"great, like\" intent.\n• Ensure the content addresses the \"work\" aspect of the subject matter, as this is a core differentiator for the top-performing topic.",
  "**Keyword Coverage Overview**\n* The analyzed content currently has **zero alignment** with the top-ranking SERP competitors, indicating a total disconnect between the page's vocabulary and the terms search engines associate with this topic.\n* The data suggests the page is likely missing the necessary semantic depth, industry jargon, and entity mentions required to rank for professional wrestling or sports entertainment analysis.\n\n**Keyword Gaps**\n* **Entity & Personality Cluster:** Significant absence of key industry figures and performers, specifically **Paul Levesque (Triple H), Zayn, Claudio, Gable,** and **Swerve**.\n* **Technical & Industry Jargon:** Failure to use standard terminology such as **\"booking,\" \"spot,\" \"bell,\"** and **\"wrestles,\"** which are essential for establishing topical authority.\n* **Qualitative & Descriptive Language:** Lack of sentiment-driven modifiers and comparative terms like **\"excellent,\" \"awesome,\" \"actually,\" \"looks,\"** and **\"feels\"** that competitors use to describe match quality or production.\n\n**Ranking Impact**\n* **Low Relevance Scoring:** Search engines will likely struggle to categorize this page within the wrestling/sports entertainment niche due to the absence of core entities.\n* **Poor Semantic Density:** Without these specific keywords, the content lacks the \"contextual tissue\" that connects it to the broader search intent, resulting in suppressed visibility for long-tail queries.\n\n**Content Optimization Suggestions**\n* **Integrate Key Entities:** Update the copy to explicitly mention the performers (e.g., Sami Zayn, Chad Gable) and management figures (Paul Levesque) central to the current narrative.\n* **Adopt Industry Vernacular:** Incorporate \"insider\" terms like \"the booking of the match\" or \"high-profile spots\" to better mirror the language used by high-ranking editorial or review sites.\n* **Enhance Descriptive Analysis:** Transition from neutral descriptions to more evaluative language, using terms like \"it feels,\" \"looks like,\" and \"excellent range\" to match the conversational and critical tone of the SERP leaders.",
  "**Entity Coverage Overview**\n* **Critically Low Coverage:** With a coverage score of only **0.32%**, the page lacks the semantic depth required to be considered a topical authority.\n* **Surface-Level Content:** The page only identifies broad brand entities (WWE, NXT) and a single primary subject (Stephanie Vaquer), suggesting the content is likely thin or overly focused on a single news beat without context.\n* **Weak Authority Signal:** Search engines use entity density to categorize content; currently, this page fails to trigger the \"Wrestling/Sports Entertainment\" knowledge graph nodes effectively compared to competitors.\n\n**Entity Gaps**\n* **Lack of Contextual Peers:** Missing key contemporary figures like **Bron Breakker** and **Natalya** prevents the page from ranking for \"related search\" queries or being surfaced in broader \"NXT\" news feeds.\n* **Missing Infrastructure Entities:** Failure to mention the **WWE Performance Center**—a critical location entity for this topic—indicates a lack of \"where/how\" details that provide comprehensive coverage.\n* **Historical and Global Context Gaps:** Missing entities such as the **American Wrestling Association** or international references (Ishii, Hazuki) suggests the content ignores the subject's professional lineage and global appeal.\n\n**Ranking Implications**\n* **Poor Keyword Reach:** Because the page lacks related entities, it will likely only rank for narrow, exact-match queries and fail to capture \"long-tail\" traffic driven by the missing entities.\n* **Low Semantic Relevance:** Google’s Hummingbird and RankBrain algorithms may struggle to validate the page's expertise, leading to lower rankings in favor of competitors who provide a richer \"entity map\" of the wrestling industry.\n* **Featured Snippet Exclusion:** The absence of specific nouns and related figures makes it nearly impossible to win \"People Also Ask\" or Knowledge Panel placements.\n\n**SEO Recommendations**\n* **Expand Biographical Context:** Incorporate mentions of Stephanie Vaquer’s rivals, trainers, and peers (e.g., mention her transition relative to established stars like Natalya or Bron Breakker).\n* **Reference Key Locations:** Explicitly mention the **WWE Performance Center** and regional territories to anchor the content in a physical and organizational context.\n* **Improve Semantic Density:** Use natural language to describe her career path, mentioning relevant organizations (e.g., her work in Mexico or Japan) to capture the \"missing\" international entities.\n* **Implement Entity-Based Schema:** Use **Person, Occupation, and Organization schema** to explicitly tell search engines which entities this page is about, bridging the gap between the text and the knowledge graph."
]
```

**HTTP Status Codes**

| Code | Meaning |
|------|---------|
| `200 OK` | Analysis completed successfully |
| `422 Unprocessable Entity` | Invalid request body |
| `500 Internal Server Error` | Upstream crawl or AI API failure |

---

## Project Structure

```
SEO-AI-Auditor/
├── app/
│   ├── main.py                          # FastAPI entry point & route definitions
│   └── streamlit_app.py                 # Streamlit interactive UI
├── src/
│   ├── crawler.py                       # Async web crawler & SERP data extraction
│   ├── similarity.py                    # SentenceTransformer semantic scoring
│   ├── topic_modeling.py                # LDA + KMeans topic gap detection
│   ├── ner.py                           # spaCy Named Entity Recognition
│   ├── tfidf.py                         # TF-IDF keyword gap analysis
│   ├── numerical_feature_extraction.py  # Content depth & backlink authority metrics
│   └── seo_engine.py                    # Main pipeline orchestrator
├── model/
│   ├── report_generator.py              # Google Gemini AI report generation
│   └── .env                             # API keys — not committed to version control
├── data/
│   ├── crawl_results.json               # Sample SERP competitor data
│   └── topic_modeled_results.json       # Sample topic modeling output
├── notebooks/
│   └── data_analysis.ipynb              # Exploratory data analysis
├── Dockerfile                           # Multi-stage production container image
├── compose.yaml                         # Docker Compose configuration
├── requirements.txt                     # Python package dependencies
└── README.md
```

---

## Contributing

Contributions, issues, and feature requests are welcome!

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature-name`
3. **Commit** your changes: `git commit -m "feat: add your feature"`
4. **Push** to your branch: `git push origin feature/your-feature-name`
5. **Open** a Pull Request against `main`

Please follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages and keep PRs focused on a single concern.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Built with ❤️ using FastAPI, spaCy, SentenceTransformers, and Google Gemini</sub>
</div>
