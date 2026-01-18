from __future__ import annotations

from .routing import classify_intent, decide_retrieval
from .context import assemble_context
from .execution import execute
from .postprocess import postprocess

async def run_pipeline(text: str, session_id: str | None, namespace: str):
    trace: list[dict] = []

    # 1) parse & normalize
    normalized = " ".join(text.strip().split())
    trace.append({"step": "parse_normalize", "input": text, "output": normalized})

    # 2) classify intent / task type
    intent = classify_intent(normalized)
    trace.append({"step": "classify_intent", "intent": intent})

    # 3) decide on retrieval & memory usage
    decision = decide_retrieval(normalized, intent)
    trace.append({"step": "decide_retrieval_memory", **decision})

    # 4) assemble execution context
    ctx = await assemble_context(
        text=normalized,
        session_id=session_id,
        namespace=namespace,
        retrieval_enabled=decision["use_retrieval"],
    )
    trace.append({"step": "assemble_context", "context_summary": ctx["summary"], "sources": ctx["sources"]})

    # 5) execute via agent or LLM adapter
    raw = await execute(text=normalized, intent=intent, context=ctx)
    trace.append({"step": "execute", "raw": raw})

    # 6) postprocess and return response
    final = postprocess(raw)
    trace.append({"step": "postprocess", "final": final})

    return {"response": final, "trace": trace}
