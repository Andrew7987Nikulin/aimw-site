from __future__ import annotations

def postprocess(raw: dict) -> str:
    # единая точка форматирования/фильтрации/редакции
    msg = raw.get("message", "")
    return msg.strip()
