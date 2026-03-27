from mcp_agent import run_mcp_agent
 
# ── Configure paths here ──────────────────────────────────────────────────
WEBSITE_PATH = r"D:\Documents\Github projects\Cricket-Website"
REPORT_PATH  = r"D:\Documents\Github projects\SEO-AI-Auditor\data\cricket_bats.json"
# ─────────────────────────────────────────────────────────────────────────
 
print("🚀 Running MCP agent (Gemini + Ollama)...")
result = run_mcp_agent(website_path=WEBSITE_PATH, report_path=REPORT_PATH)
print(f"✅ MCP agent finished: {result}")