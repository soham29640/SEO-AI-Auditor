"""
gemini_client.py

Handles all Gemini API calls with:
  - Fixed model: gemini-3-flash-preview, loaded from model/.env
  - Exponential backoff on 429 / RESOURCE_EXHAUSTED
"""

import os
import re
import time

from google import genai
from google.genai.errors import ClientError
from dotenv import load_dotenv

# ---------------- LOAD ENV ----------------
load_dotenv("model/.env")

api_key = os.getenv("GEMINI_API_KEY")

model = "gemini-3-flash-preview"

client = genai.Client(api_key=api_key)

MAX_RETRIES   = 3
BASE_WAIT_SEC = 15    # 60s / 5 RPM = 12s minimum; 15s adds margin


def _parse_retry_delay(error_str: str) -> int | None:
    """Extract the retryDelay value from a 429 error message if present."""
    match = re.search(r"retryDelay.*?(\d+)s", error_str)
    return int(match.group(1)) + 2 if match else None


class GeminiClient:
    def __init__(self):
        self.client = client

    def _call(self, prompt: str) -> str:
        """Single raw API call. Raises ClientError on any API failure."""
        response = self.client.models.generate_content(
            model=model,
            contents=prompt
        )
        text = response.text or ""
        if "```" in text:
            text = re.sub(r"```[a-z]*", "", text).replace("```", "").strip()
        return text

    def call_with_retry(self, prompt: str) -> str:
        """
        Public method — called directly from mcp_agent.py.
        Retries with exponential backoff on 429 / RESOURCE_EXHAUSTED.
        Raises RuntimeError if all attempts fail.
        """
        wait = BASE_WAIT_SEC

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                print(f"   🤖 Gemini [{model}] attempt {attempt}/{MAX_RETRIES}...")
                return self._call(prompt)

            except ClientError as e:
                err = str(e)
                if "429" in err or "RESOURCE_EXHAUSTED" in err:
                    if attempt < MAX_RETRIES:
                        sleep_sec = _parse_retry_delay(err) or wait
                        print(f"   ⏳ Rate limited — waiting {sleep_sec}s...")
                        time.sleep(sleep_sec)
                        wait *= 2
                    else:
                        raise RuntimeError(f"Gemini quota exhausted after {MAX_RETRIES} attempts: {e}")
                else:
                    raise  # non-quota error — don't retry

        raise RuntimeError("Exceeded max retries without a successful response.")
