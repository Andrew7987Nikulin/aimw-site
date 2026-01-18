from __future__ import annotations

import math
import re
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.session import SessionLocal
from ..db.models import Document

def _tokenize(s: str) -> list[str]:
    s = s.lower()
    s = re.sub(r"[^a-z0-9а-яё\s]+", " ", s, flags=re.IGNORECASE)
    toks = [t for t in s.split() if len(t) > 2]
    return toks[:400]

def _tf(tokens: list[str]) -> dict[str, float]:
    d: dict[str, float] = {}
    for t in tokens:
        d[t] = d.get(t, 0.0) + 1.0
    n = max(1.0, float(len(tokens)))
    for k in list(d.keys()):
        d[k] /= n
    return d

def _cos(a: dict[str, float], b: dict[str, float]) -> float:
    dot = 0.0
    for k, v in a.items():
        dot += v * b.get(k, 0.0)
    na = math.sqrt(sum(v*v for v in a.values())) or 1.0
    nb = math.sqrt(sum(v*v for v in b.values())) or 1.0
    return dot / (na * nb)

class MemoryService:
    async def write(self, namespace: str, title: str, content: str) -> str:
        async with SessionLocal() as session:
            doc = Document(namespace=namespace, title=title, content=content)
            session.add(doc)
            await session.commit()
            await session.refresh(doc)
            return doc.id

    async def search(self, namespace: str, query: str, limit: int = 5) -> list[dict]:
        # Демо-поиск: cosine по TF (без эмбеддингов), чтобы работало из коробки.
        # Для pgvector: заменить на embedding + ORDER BY embedding <-> :query_vec
        qv = _tf(_tokenize(query))

        async with SessionLocal() as session:
            rows = (await session.execute(
                select(Document).where(Document.namespace == namespace)
            )).scalars().all()

        scored = []
        for d in rows:
            dv = _tf(_tokenize(d.title + " " + d.content))
            score = _cos(qv, dv)
            snippet = (d.content[:180] + "…") if len(d.content) > 180 else d.content
            scored.append({"id": d.id, "title": d.title, "score": float(score), "snippet": snippet})

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:limit]

memory = MemoryService()
