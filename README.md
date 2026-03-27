<div align="center">

# 🔍 SEO AI Auditor

**An AI-powered SEO auditing and content optimization engine**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![Ollama](https://img.shields.io/badge/Ollama-llama3-black?logo=ollama&logoColor=white)](https://ollama.ai/)

</div>

---

## 📖 Overview

**SEO AI Auditor** is a full-stack AI pipeline that audits any webpage against its top SERP (Search Engine Results Page) competitors, generates a detailed multi-dimensional SEO report, and then automatically rewrites your website's HTML to close every identified gap — all without leaving the command line.

The system combines classical NLP techniques (TF-IDF, LDA, NER) with modern AI models (Google Gemini, Sentence Transformers, Ollama/llama3) to produce actionable, data-driven insights.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🕷️ **Intelligent Web Crawler** | Crawls target URLs and the top 25 SERP results using `crawl4ai` + DuckDuckGo |
| 📊 **Semantic Similarity Analysis** | Measures how closely page content aligns with SERP competitors via `sentence-transformers` |
| 🔑 **TF-IDF Keyword Gap Analysis** | Identifies keywords present in top-ranking pages that your content is missing |
| 🧠 **Topic Modeling (LDA)** | Surfaces dominant SERP themes via Latent Dirichlet Allocation to reveal search intent |
| 🏷️ **Named Entity Recognition (NER)** | Compares entity coverage (brands, products, locations, people) against competitors using spaCy |
| 📈 **Content Strength Scoring** | Benchmarks your word count and estimated backlinks against SERP averages |
| 🤖 **AI Report Generation** | Translates every metric into plain-English insights powered by Google Gemini |
| ✍️ **Automated HTML Optimization** | An MCP agent (Ollama llama3 + Gemini) directly rewrites your website's HTML to fill every gap |
| 🚀 **REST API** | Clean two-step FastAPI interface: generate report → apply optimizations |

---

## 🏗️ Architecture

```
SEO AI Auditor
│
├── app/
│   └── main.py                   # FastAPI application (REST endpoints)
│
├── src/
│   ├── crawler.py                # Web crawling + SERP data collection
│   ├── numerical_feature_extraction.py  # Word count & backlink scoring
│   ├── similarity.py             # Semantic similarity via sentence-transformers
│   ├── topic_modeling.py         # LDA-based search intent analysis
│   ├── tfidf.py                  # TF-IDF keyword gap detection
│   └── ner.py                    # Named entity recognition & coverage
│
├── model/
│   └── report_generator.py       # Gemini-powered AI report generation
│
├── seo_content_creator/
│   ├── mcp_agent.py              # MCP agent: HTML optimizer (Ollama + Gemini)
│   ├── gemini_client.py          # Gemini API client with retry/backoff
│   ├── ollama_client.py          # Ollama (llama3) local LLM client
│   └── utils.py                  # File I/O utilities
│
├── data/
│   ├── crawl_results.json        # Cached SERP crawl data
│   └── topic_modeled_results.json # Cached topic modeling output
│
├── notebooks/
│   └── data_analysis.ipynb       # Exploratory data analysis notebook
│
└── requirements.txt
```

### Data Flow

```
User Input (keyword + URL)
        │
        ▼
  [1] Crawler ──────────── crawl4ai + DuckDuckGo
        │                  • Crawls target URL
        │                  • Crawls top 25 SERP results
        ▼
  [2] Analysis Engine ──── 5 parallel analyses
        ├── Numerical Feature Extraction   (word count, backlinks)
        ├── Semantic Similarity            (sentence-transformers)
        ├── Topic Modeling / LDA           (scikit-learn + spaCy)
        ├── TF-IDF Keyword Gap             (scikit-learn)
        └── NER Entity Coverage            (spaCy)
        │
        ▼
  [3] Report Generator ─── Google Gemini
        │                  • Converts metrics → plain-English insights
        ▼
  [4] MCP Agent ─────────── Ollama (llama3) + Gemini
                           • Reads generated report
                           • Rewrites website HTML to close every gap
                           • Backs up originals before modifying
```

---

## ⚙️ Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.10 or higher |
| [Ollama](https://ollama.ai/) | Latest (with `llama3` model pulled) |
| Google Gemini API key | Free tier available |
| Playwright browsers | Installed via CLI (see below) |

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/soham29640/SEO-AI-Auditor.git
cd SEO-AI-Auditor
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install spaCy language model

```bash
python -m spacy download en_core_web_sm
```

### 5. Install Playwright browsers

```bash
playwright install
```

### 6. Pull the Ollama model

```bash
ollama pull llama3
```

### 7. Configure environment variables

Create a file at `model/.env`:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

> **Tip:** Get a free Gemini API key at [Google AI Studio](https://aistudio.google.com/).

---

## 🖥️ Usage

### Start the API server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

---

### Step 1 — Generate an SEO Report

```bash
curl -X POST http://localhost:8000/seo-report \
  -H "Content-Type: application/json" \
  -d '{"keyword": "best cricket bats", "url": "https://yourwebsite.com/cricket-bats"}'
```

**Response:**

```json
{
  "message": "Report generated",
  "file_path": "/path/to/report.json",
  "task_id": "abc123-...",
  "next_step": "/proceed/abc123-..."
}
```

---

### Step 2 — Apply AI Optimizations

```bash
curl -X POST http://localhost:8000/proceed/abc123-...
```

**Response:**

```json
{
  "message": "MCP agent executed successfully",
  "agent_result": "Done — OK: index.html, OK: products.html"
}
```

The MCP agent will:
1. **Back up** every `.html` file before touching it
2. Use **Gemini** to improve `<title>` and `<meta>` tags
3. Use **Ollama (llama3)** to inject new `<section>` content blocks for every identified SEO gap

---

## 📊 Analysis Modules

### 🔢 Content Strength Report
Compares your page's word count and estimated backlinks against the SERP average.

| Metric | Description |
|---|---|
| `content_depth_score_percent` | Your word count as a % of the SERP average |
| `authority_score_percent` | Your backlinks as a % of the SERP average |

### 🧬 Semantic Similarity Report
Uses `all-MiniLM-L6-v2` to embed and compare your content against the average SERP embedding.

| Metric | Description |
|---|---|
| `semantic_similarity_percent` | Cosine similarity vs. average SERP embedding (0–100%) |
| `grade` | A / B / C / D letter grade |
| `better_than_percent_of_competitors` | Percentile rank within the SERP |

### 🎯 Topic Modeling Report
Runs LDA with 3 topics on SERP content; checks if your page targets the dominant topic.

| Metric | Description |
|---|---|
| `company_topic` | Dominant topic of your page |
| `dominant_serp_topic` | Most common topic across top SERP results |
| `serp_topic_distribution` | How topics are distributed across SERP pages |

### 🔑 Keyword Gap Report
Extracts top 50 TF-IDF keywords from SERP leaders and checks how many appear in your content.

| Metric | Description |
|---|---|
| `coverage_score_percent` | Percentage of SERP keywords found in your content |
| `gap_severity` | Low / Moderate / High |
| `missing_keywords_top20` | The 20 most important missing keywords |

### 🏷️ Entity Coverage Report
Uses spaCy NER to compare named entities (ORG, PRODUCT, PERSON, GPE) between your page and competitors.

| Metric | Description |
|---|---|
| `entity_coverage_score_percent` | % of competitor entities covered |
| `severity_level` | Strong / Moderate / Weak |
| `missing_entities_sample` | Up to 15 entities to add |

---

## 📁 Project Structure

```
SEO-AI-Auditor/
├── app/
│   └── main.py
├── data/
│   ├── crawl_results.json
│   ├── cricket_bats.json
│   └── topic_modeled_results.json
├── model/
│   ├── .env                  # ← your Gemini API key (git-ignored)
│   └── report_generator.py
├── notebooks/
│   └── data_analysis.ipynb
├── seo_content_creator/
│   ├── gemini_client.py
│   ├── mcp_agent.py
│   ├── ollama_client.py
│   └── utils.py
├── src/
│   ├── crawler.py
│   ├── ner.py
│   ├── numerical_feature_extraction.py
│   ├── similarity.py
│   ├── seo_engine.py
│   ├── tfidf.py
│   └── topic_modeling.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## 🛠️ Tech Stack

| Category | Library / Tool |
|---|---|
| **Web Framework** | FastAPI, Uvicorn |
| **Web Crawling** | crawl4ai, Playwright, BeautifulSoup4 |
| **Search** | DuckDuckGo Search (`ddgs`) |
| **NLP / ML** | spaCy, scikit-learn, sentence-transformers |
| **AI / LLMs** | Google Gemini (`google-genai`), Ollama (llama3) |
| **Data** | pandas, numpy, openpyxl |
| **Environment** | python-dotenv |
| **Notebooks** | Jupyter / ipykernel |

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to your fork: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please ensure your code follows the existing style and that any new modules include appropriate docstrings.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
Made with ❤️ by <a href="https://github.com/soham29640">soham29640</a>
</div>
