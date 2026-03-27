import requests
import os
from dotenv import load_dotenv

load_dotenv()

class OllamaClient:
    def __init__(self, model: str = None):
        self.url   = "http://localhost:11434/api/generate"
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3")

    def generate(self, prompt: str, timeout: int = 120) -> str:
        try:
            response = requests.post(
                self.url,
                json={
                    "model":  self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_ctx":     4096,   # explicit llama3 context limit
                        "temperature": 0.2,    # low = consistent, no hallucination
                        "top_p":       0.9,
                        "num_predict": 1024,   # cap output tokens so it finishes fast
                    }
                },
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()["response"]

        except requests.exceptions.Timeout:
            raise RuntimeError(
                f"Ollama timed out after {timeout}s. "
                "The prompt may still be too large — check mcp_agent.py limits."
            )
        except Exception as e:
            raise RuntimeError(f"Ollama error: {e}")