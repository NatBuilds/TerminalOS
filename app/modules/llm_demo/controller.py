from __future__ import annotations

from app.libraries.llm.llm_chat import LLMChat
from app.core import status


def run() -> None:
    prompt = status.info_input("\nEnter prompt: ", show_prefix=False).strip()
    if not prompt:
        status.warning("Prompt cannot be empty.")
        return

    chat = LLMChat()
    if not chat.check_endpoint():
        status.warning("LM Studio endpoint is unavailable.")
        return

    response = chat.send_chat(prompt)
    if response:
        status.success(response)
        return

    status.warning("No response from LM Studio.")


def register(menu) -> None:
    menu.add("LLM Demo", run)
