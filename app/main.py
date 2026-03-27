import asyncio
import sys
import json
import os

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI
from pydantic import BaseModel
from src.seo_engine import submit

app = FastAPI(title="AI SEO Auditor API")

class URLRequest(BaseModel):
    keyword: str
    url: str

@app.post("/seo-report")
async def generate_report(data: URLRequest):
    result = await submit(data.keyword, data.url)

    # Define file path
    folder = r"D:\Documents\Github projects\SEO-AI-Auditor\data"
    os.makedirs(folder, exist_ok=True)
    file_path = f"{folder}/{data.keyword.replace(' ', '_')}.json"

    # Save JSON
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    return {
        "message": "Report generated",
        "file_path": file_path,
        "data": result
    }