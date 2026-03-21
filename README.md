# 🧠 SEO AI Auditor

An NLP-driven SEO intelligence engine that analyzes your webpage against top-ranking competitors using semantic embeddings, topic modeling, entity extraction, and content depth metrics. Generates a Final SEO Score (0–100) with AI-powered, actionable optimization insights via Google Gemini.

**Version:** 1.0 &nbsp;|&nbsp; **Status:** Prototype

---

## ✨ Features

- 🔍 Crawls your target URL and fetches top 10 SERP competitor pages automatically
- 📐 Semantic similarity scoring using `SentenceTransformer` embeddings
- 🗂 Topic modeling with LDA + KMeans clustering to surface missing content themes
- 🏷 Named Entity Recognition (NER) with spaCy to detect entity coverage gaps
- 📊 Content depth and backlink authority scoring
- 🤖 AI-generated reports for each metric via Google Gemini API
- 🌐 REST API built with FastAPI
- 🐳 Docker-ready for local and cloud deployment

---

## 🚀 Workflow

1. **Data Collection** (`src/crawler.py`)
   - Crawls the target URL and retrieves the top 10 SERP results via DuckDuckGo
   - Extracts title, meta description, headings (H1–H3), full content, and estimated backlinks
   - Cleans and standardizes all text

2. **Semantic Analysis** (`src/similarity.py`)
   - Encodes all content with `SentenceTransformer("all-MiniLM-L6-v2")`
   - Computes cosine similarity between the target page and the average competitor vector
   - Generates a **Semantic Coverage Score**

3. **Topic Modeling** (`src/topic_modeling.py`)
   - Embeds competitor headings and clusters them with KMeans
   - Identifies dominant SERP themes and detects missing topics in the target page
   - Generates a **Topic Coverage Score**

4. **Entity Coverage** (`src/ner.py`)
   - Extracts entities (ORG, PRODUCT, PERSON, GPE) using spaCy NER
   - Compares entity sets between the target page and competitors
   - Generates an **Entity Coverage Score**

5. **Content Depth Analysis** (`src/numerical_feature_extraction.py`)
   - Compares word count and backlink count against the SERP average
   - Generates a **Content Depth Score** and **Authority Score**

6. **AI-Powered Reports** (`model/report_generator.py`)
   - Sends structured metrics to Google Gemini API
   - Returns concise, actionable SEO insights for each analysis module

---

## 🛠 Tech Stack

| Category | Libraries / Tools |
|---|---|
| Language | Python 3.10+ |
| API Framework | FastAPI, Uvicorn |
| UI | Streamlit |
| NLP & ML | SentenceTransformers, spaCy, scikit-learn |
| Data | pandas, NumPy |
| Web Crawling | Crawl4ai, DDGS, BeautifulSoup, Playwright |
| AI Reports | Google Gemini API (`google-genai`) |
| Config | python-dotenv |
| Deployment | Docker, Docker Compose |

---

## 📋 Prerequisites

- Python 3.10+
- [Google Gemini API key](https://aistudio.google.com/app/apikey)
- Docker & Docker Compose (for containerized deployment)

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/soham29640/SEO-AI-Auditor.git
cd SEO-AI-Auditor
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install spaCy language model

```bash
python -m spacy download en_core_web_sm
```

### 4. Install Playwright browsers

```bash
playwright install
```

### 5. Configure environment variables

Create a `.env` file inside the `model/` directory:

```bash
# model/.env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 6. Run the API server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

---

## 📡 API Usage

### Endpoint

```
POST /SEO report
```

### Request body

```json
{
  "keyword": "your target keyword",
  "url": "https://your-website.com/page"
}
```

### Example with curl

```bash
curl -X POST "http://localhost:8000/SEO%20report" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "best running shoes", "url": "https://example.com/running-shoes"}'
```

The response contains AI-generated analysis reports for each module (semantic similarity, topic modeling, keyword gaps, entity coverage, and content depth).

---

## 🐳 Docker Deployment

### Run locally with Docker Compose

```bash
docker compose up --build
```

The application will be available at `http://localhost:8000`.

### Build and run manually

```bash
docker build -t seo-ai-auditor .
docker run -p 8000:8000 seo-ai-auditor
```

### Deploy to the cloud

Build for your cloud platform's CPU architecture (e.g., `amd64` on an Apple M-series Mac):

```bash
docker build --platform=linux/amd64 -t seo-ai-auditor .
docker push myregistry.com/seo-ai-auditor
```

See Docker's [getting started guide](https://docs.docker.com/go/get-started-sharing/) for details on building and pushing images, and the [Python guide](https://docs.docker.com/language/python/) for Python-specific best practices.

---

## 📁 Project Structure

```
SEO-AI-Auditor/
├── app/
│   ├── main.py                          # FastAPI entry point
│   └── streamlit_app.py                 # Streamlit UI
├── src/
│   ├── crawler.py                       # Web crawler & SERP data extraction
│   ├── similarity.py                    # Semantic analysis
│   ├── topic_modeling.py                # Topic modeling (LDA + KMeans)
│   ├── ner.py                           # Named Entity Recognition
│   ├── tfidf.py                         # Keyword gap analysis (TF-IDF)
│   ├── numerical_feature_extraction.py  # Content depth & authority metrics
│   └── seo_engine.py                    # Main orchestrator
├── model/
│   ├── report_generator.py              # Google Gemini AI report generation
│   └── .env                             # API keys (not committed)
├── data/
│   ├── crawl_results.json               # Sample SERP competitor data
│   └── topic_modeled_results.json       # Sample topic modeling output
├── notebooks/
│   └── data_analysis.ipynb              # Exploratory data analysis
├── Dockerfile
├── compose.yaml
├── requirements.txt
└── README.md
```