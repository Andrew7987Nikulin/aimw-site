from __future__ import annotations

def postprocess(raw: dict) -> str:
    msg = raw.get("message", "")
    return msg.strip()
