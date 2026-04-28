from __future__ import annotations

from typing import Any

import requests

from app.core import config, status


class LLMChat:
    def __init__(self) -> None:
        self.provider = config.get_llm_provider()
        self.base_url = config.get_llm_base_url()
        self.chat_endpoint = config.get_llm_chat_endpoint()
        self.model = config.get_llm_model()
        self.api_key = config.get_llm_api_key()
        self.timeout = config.get_llm_timeout()
        self.endpoint = self.endpoint_setup()

    def endpoint_setup(self) -> str:
        base_url = self.base_url.rstrip("/")
        endpoint_path = self.chat_endpoint.strip()
        if not endpoint_path.startswith("/"):
            endpoint_path = f"/{endpoint_path}"

        self.endpoint = f"{base_url}{endpoint_path}"
        return self.endpoint

    def check_endpoint(self) -> bool:
        models_url = f"{self.base_url.rstrip('/')}/models"
        headers = {"Content-Type": "application/json"}

        api_key = self.api_key.strip()
        if api_key and api_key != "not-needed":
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = requests.get(models_url, headers=headers, timeout=self.timeout)
        except requests.RequestException as exc:
            status.error(f"LLM endpoint check failed: {exc}")
            return False

        if response.status_code >= 400:
            status.error(f"LLM endpoint check failed with status {response.status_code}.")
            return False

        return True

    def send_chat(self, message: str) -> str:
        prompt = (message or "").strip()
        if not prompt:
            return ""

        return self.send_messages([{"role": "user", "content": prompt}])

    def send_messages(self, messages: list) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
        }
        headers = {"Content-Type": "application/json"}

        api_key = self.api_key.strip()
        if api_key and api_key != "not-needed":
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            response = requests.post(
                self.endpoint,
                headers=headers,
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
            data: Any = response.json()
        except requests.RequestException as exc:
            status.error(f"LLM request failed: {exc}")
            return ""
        except ValueError as exc:
            status.error(f"LLM returned invalid JSON: {exc}")
            return ""

        if not isinstance(data, dict):
            status.error("LLM response format is invalid.")
            return ""

        choices = data.get("choices")
        if not isinstance(choices, list) or not choices:
            status.error("LLM response did not contain choices.")
            return ""

        first_choice = choices[0]
        if not isinstance(first_choice, dict):
            status.error("LLM response choice format is invalid.")
            return ""

        message_data = first_choice.get("message")
        if not isinstance(message_data, dict):
            status.error("LLM response message format is invalid.")
            return ""

        content = message_data.get("content", "")
        if content is None:
            return ""

        return str(content).strip()
