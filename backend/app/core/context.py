from __future__ import annotations
from .memory import memory

async def assemble_context(text: str, session_id: str | None, namespace: str, retrieval_enabled: bool) -> dict:
    sources = []
    if retrieval_enabled:
        hits = await memory.search(namespace=namespace, query=text, limit=3)
        sources = [{"id": h["id"], "title": h["title"], "score": h["score"]} for h in hits]

    summary = {
        "session_id": session_id or "none",
        "namespace": namespace,
        "retrieval_enabled": retrieval_enabled,
        "sources": len(sources),
    }
    return {"summary": summary, "sources": sources}
