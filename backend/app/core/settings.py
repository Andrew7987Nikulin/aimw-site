from __future__ import annotations
import os
from pydantic import BaseModel

class Settings(BaseModel):
    db_url: str = os.getenv("AIMW_DB_URL", "sqlite+aiosqlite:///./aimw.db")
    public_origin: str | None = os.getenv("AIMW_PUBLIC_ORIGIN")

settings = Settings()
