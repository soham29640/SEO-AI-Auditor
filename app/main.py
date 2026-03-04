import asyncio
import sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI
from pydantic import BaseModel
from src.seo_engine import submit

app = FastAPI(title="AI SEO Auditor API")

class URLRequest(BaseModel):
    keyword: str
    url: str
    
@app.post("/SEO report")
async def generate_report(data: URLRequest):
    return await submit(data.keyword, data.url)