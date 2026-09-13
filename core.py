"""
NanoCoT Core Engine: Complexity Classification, Reasoning Injection, Response Sanitization
"""

import re
import json
from typing import List, Dict, Any, Tuple, AsyncGenerator


class ComplexityClassifier:
    """
    Evaluates request complexity to route simple and complex queries differently.
    Simple requests bypass reasoning. Complex requests receive reasoning budget.
    """
    
    SIMPLE_PATTERNS = [
        r"^(hi|hello|hey|greetings|terima kasih|thanks)\b",
        r"^(translate|terjemahkan)\b",
        r"^(format|reformat|json|convert)\b",
        r"^(summarize|ringkas)\b",
    ]

    COMPLEX_PATTERNS = [
        r"\b(code|function|debug|algorithm|refactor|optimize|class|async|sql|db|schema)\b",
        r"\b(calculate|proof|math|logic|reason|analyze|compare|evaluate|why|how)\b",
        r"\b(architecture|system|design|pipeline|middleware|proxy)\b",
    ]

    def classify(self, messages: List[Dict[str, Any]]) -> bool:
        if not messages:
            return False
            
        last_user_msg = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                content = msg.get("content", "")
                if isinstance(content, str):
                    last_user_msg = content
                elif isinstance(content, list):
                    last_user_msg = " ".join([item.get("text", "") for item in content if isinstance(item, dict)])
                break

        text_lower = last_user_msg.lower().strip()
        
        for pat in self.SIMPLE_PATTERNS:
            if re.search(pat, text_lower) and len(text_lower.split()) < 15:
                return False
                
        for pat in self.COMPLEX_PATTERNS:
            if re.search(pat, text_lower):
                return True

        return len(text_lower.split()) > 20


class MicroCoTInjector:
    """
    Adds a reasoning budget to system prompt for complex tasks.
    Limits reasoning to 80 words to keep response time fast.
    """

    SYSTEM_PROMPT = (
        "\n\n[SYSTEM DIRECTIVE: NANOCOT REASONING ENGINE]\n"
        "To achieve maximum output accuracy, perform internal reasoning inside <nanocot_think>...</nanocot_think> tags.\n"
        "Rules:\n"
        "1. Keep reasoning concise (under 80 words, bullet points only).\n"
        "2. Do not write full sentences or prose inside <nanocot_think>.\n"
        "3. Immediately close </nanocot_think> and provide the direct, clean answer.\n"
    )

    def inject(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        new_messages = [msg.copy() for msg in messages]
        
        system_idx = -1
        for idx, msg in enumerate(new_messages):
            if msg.get("role") == "system":
                system_idx = idx
                break
                
        if system_idx != -1:
            content = new_messages[system_idx]["content"]
            if isinstance(content, str):
                new_messages[system_idx]["content"] = content + self.SYSTEM_PROMPT
        else:
            new_messages.insert(0, {
                "role": "system",
                "content": "You are a helpful, precise AI assistant." + self.SYSTEM_PROMPT
            })
            
        return new_messages


class PhysicalResponseSanitizer:
    """
    Removes reasoning tags from model responses.
    Operates on both standard and streaming responses.
    """

    THINK_REGEX = re.compile(r"<nanocot_think>.*?</nanocot_think>", re.DOTALL | re.IGNORECASE)
    UNCLOSED_THINK_START = re.compile(r"<nanocot_think>.*$", re.DOTALL | re.IGNORECASE)

    def sanitize_text(self, text: str) -> str:
        if not text:
            return ""
        cleaned = self.THINK_REGEX.sub("", text)
        cleaned = self.UNCLOSED_THINK_START.sub("", cleaned)
        return cleaned.lstrip()

    async def sanitize_stream(self, stream_generator: AsyncGenerator[str, None]) -> AsyncGenerator[str, None]:
        full_text = ""
        async for chunk in stream_generator:
            full_text += chunk

        clean_text = self.sanitize_text(full_text)
        if clean_text:
            yield clean_text
