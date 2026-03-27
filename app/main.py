import asyncio
import sys
import json
import os
import uuid

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI
from pydantic import BaseModel
from src.seo_engine import submit
from seo_content_creater.mcp_agent import run_mcp_agent   # ✅ your agent

app = FastAPI(title="AI SEO Auditor API")

# Temporary storage (replace later with DB/Redis)
storage = {}

class URLRequest(BaseModel):
    keyword: str
    url: str


# ✅ STEP 1: Generate Report + Save JSON
@app.post("/seo-report")
async def generate_report(data: URLRequest):
    result = await submit(data.keyword, data.url)

    folder = r"D:\Documents\Github projects\SEO-AI-Auditor\data"
    os.makedirs(folder, exist_ok=True)

    file_path = f"{folder}/{data.keyword.replace(' ', '_')}.json"

    # Save JSON
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    task_id = str(uuid.uuid4())

    # Store file path + (optional website path if needed later)
    storage[task_id] = {
        "file_path": file_path,
        "website_path": r"D:\Documents\Github projects\Cricket-Website"  # you can make dynamic later
    }

    return {
        "message": "Report generated",
        "file_path": file_path,
        "task_id": task_id,
        "next_step": f"/proceed/{task_id}"
    }


# ✅ STEP 2: Proceed → Run MCP Agent using saved JSON
@app.post("/proceed/{task_id}")
async def proceed(task_id: str):
    task = storage.get(task_id)

    if not task:
        return {"error": "Invalid task_id"}

    file_path = task["file_path"]
    website_path = task["website_path"]

    # Validate file
    if not os.path.exists(file_path):
        return {"error": "Report file not found"}

    if not os.path.exists(website_path):
        return {"error": "Website path not found"}

    # 🚀 Run your MCP agent
    try:
        result = run_mcp_agent(
            website_path=website_path,
            report_path=file_path
        )
    except Exception as e:
        return {"error": str(e)}

    return {
        "message": "MCP agent executed successfully",
        "agent_result": result
    }