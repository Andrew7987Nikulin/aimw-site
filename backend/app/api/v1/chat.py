from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

from ...core.pipeline import run_pipeline

router = APIRouter()

class ChatIn(BaseModel):
    text: str = Field(..., min_length=1, max_length=4000)
    session_id: str | None = Field(default=None, max_length=128)
    namespace: str = Field(default="default", max_length=64)

class ChatOut(BaseModel):
    response: str
    trace: list[dict]

@router.post("/chat", response_model=ChatOut)
async def chat(payload: ChatIn):
    result = await run_pipeline(
        text=payload.text,
        session_id=payload.session_id,
        namespace=payload.namespace,
    )
    return ChatOut(response=result["response"], trace=result["trace"])
