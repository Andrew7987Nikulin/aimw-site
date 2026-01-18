from __future__ import annotations
import re

def classify_intent(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["ошибка", "error", "traceback", "stack", "исключение"]):
        return "debug"
    if any(k in t for k in ["архитектура", "design", "проект", "system", "модуль", "pipeline"]):
        return "architecture"
    if re.search(r"\b(сделай|создай|написать|сгенерируй)\b", t):
        return "build"
    if any(k in t for k in ["объясни", "почему", "как работает", "что такое"]):
        return "explain"
    return "chat"

def decide_retrieval(text: str, intent: str) -> dict:
    t = text.lower()
    keywords = ["rag", "pgvector", "prometheus", "observability", "postgres", "vector", "embedding", "retrieval"]
    use = intent in {"architecture", "explain"} and any(k in t for k in keywords)
    return {
        "use_retrieval": bool(use),
        "use_session_memory": True,
        "use_canonical_memory": intent in {"architecture", "build"},
    }
