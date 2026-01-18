from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

from ...core.memory import memory

router = APIRouter()

class MemoryWriteIn(BaseModel):
    namespace: str = Field(default="default", max_length=64)
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=20000)

class MemoryWriteOut(BaseModel):
    id: str

@router.post("/memory/write", response_model=MemoryWriteOut)
async def write(payload: MemoryWriteIn):
    doc_id = await memory.write(namespace=payload.namespace, title=payload.title, content=payload.content)
    return MemoryWriteOut(id=doc_id)

class MemorySearchIn(BaseModel):
    namespace: str = Field(default="default", max_length=64)
    query: str = Field(..., min_length=1, max_length=2000)
    limit: int = Field(default=5, ge=1, le=20)

class MemorySearchHit(BaseModel):
    id: str
    title: str
    score: float
    snippet: str

class MemorySearchOut(BaseModel):
    hits: list[MemorySearchHit]

@router.post("/memory/search", response_model=MemorySearchOut)
async def search(payload: MemorySearchIn):
    hits = await memory.search(namespace=payload.namespace, query=payload.query, limit=payload.limit)
    return MemorySearchOut(hits=hits)
