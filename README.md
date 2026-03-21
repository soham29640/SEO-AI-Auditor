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
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────────────┐ │
│  │  Crawler     │  │  Similarity   │  │  Topic Modeling      │ │
│  │  crawler.py  │  │  similarity.py│  │  topic_modeling.py   │ │
│  └──────────────┘  └───────────────┘  └──────────────────────┘ │
│  ┌──────────────┐  ┌───────────────┐                           │
│  │  NER         │  │  Depth /      │                           │
│  │  ner.py      │  │  Authority    │                           │
│  └──────────────┘  └───────────────┘                           │
└────────────────────────────┬────────────────────────────────────┘
                             │  Structured metrics
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│            Report Generator  (model/report_generator.py)       │
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

```json
{
  "final_seo_score": 72.4,
  "semantic_similarity_report": "Your content covers ~68% of the semantic space occupied by top competitors...",
  "topic_coverage_report": "Missing topics identified: cushioning technology, trail vs road comparison...",
  "entity_coverage_report": "Key brands not mentioned: Nike, Asics, Brooks...",
  "content_depth_report": "Word count (840) is 43% below the SERP average (1470)...",
  "authority_report": "Estimated backlink count is below average. Consider a link-building campaign..."
}
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