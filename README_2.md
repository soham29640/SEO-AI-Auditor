# 🚀 SEO MCP Agent (Gemini + Ollama)

An AI-powered SEO optimization engine that automatically enhances HTML websites using Google Gemini and LLM-driven content generation.

This project takes:
- 📁 A website folder (HTML files)
- 📄 An SEO report (`report.json`)

…and automatically updates the website by:
- Improving meta tags (title, description, keywords)
- Injecting SEO-optimized content sections
- Creating backup files before modification

---

## ✨ Features

- 🔑 Secure API key management via `.env`
- 🤖 Gemini-powered `<head>` optimization
- 🦙 LLM-based content generation (Ollama / llama3)
- 💾 Automatic backup of original HTML files
- 🔄 Retry logic with exponential backoff for API limits
- 📦 Clean modular architecture

---

## 🏗️ Project Structure

```
├── main.py              # Entry point — run this file
├── mcp_agent.py         # Core SEO optimization pipeline
├── gemini_client.py     # Gemini API integration
├── ollama_client.py     # Local LLM (llama3) client
├── utils.py             # File utilities
├── requirements.txt     # Dependencies
├── model/.env           # API keys (NOT pushed to GitHub)
```

---

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/seo-mcp-agent.git
cd seo-mcp-agent
```

### 2. Create & Activate Environment
```bash
conda create -n myenv python=3.10
conda activate myenv
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

Dependencies include: `google-genai`, `python-dotenv`, `requests`

### 4. Setup Environment Variables

Create `model/.env` and add:
```
GEMINI_API_KEY=your_api_key_here
```

### 5. Start Ollama (llama3 must be running locally)
```bash
ollama serve
ollama pull llama3
```

---

## ▶️ Running

### 1. Set your paths in `main.py`

Open `main.py` and update these two lines to point to your files:

```python
WEBSITE_PATH = "./website"   # folder containing your HTML files
REPORT_PATH  = "./report.json"  # your SEO report
```

### 2. Run
```bash
python main.py
```

---

## 🔄 Workflow

```
python main.py
        │
        ▼
MCP Agent Execution
        │
        ├── Backup HTML files
        │
        ├── Pass 1: Gemini
        │     └── Optimize <head> (title, description, keywords)
        │
        ├── Pass 2: Ollama / llama3
        │     └── Generate SEO content <section> blocks
        │
        ▼
Updated HTML files saved to <website_path>
```