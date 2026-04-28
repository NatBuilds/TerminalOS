from __future__ import annotations


class TextTools:
    def uppercase(self, text: str) -> str:
        return text.upper()

    def lowercase(self, text: str) -> str:
        return text.lower()

    def title_case(self, text: str) -> str:
        return text.title()

    def word_count(self, text: str) -> int:
        return len(text.split())

    def character_count(self, text: str) -> int:
        return len(text)
