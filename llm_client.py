import json
from typing import Any, Dict, List

import requests


class LLMClient:
    def __init__(
        self,
        base_url: str = "http://localhost:1234/v1/chat/completions",
        model: str = "qwen/qwen3-vl-8b",
        temperature: float = 0.2,
    ) -> None:
        self.base_url = base_url
        self.model = model
        self.temperature = temperature

    def chat(self, messages: List[Dict[str, Any]]) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
        }
        response = requests.post(self.base_url, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        if "choices" not in data or not data["choices"]:
            raise RuntimeError("No choices returned from LLM.")
        content = data["choices"][0]["message"].get("content")
        if content is None:
            raise RuntimeError("Empty response from LLM.")
        if isinstance(content, list):
            return json.dumps(content)
        return content.strip()
