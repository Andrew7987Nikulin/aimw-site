from __future__ import annotations

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text as sql_text

from ..core.settings import settings
from .base import Base

engine = create_async_engine(settings.db_url, echo=False, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        if settings.db_url.startswith("postgresql"):
            try:
                await conn.execute(sql_text("CREATE EXTENSION IF NOT EXISTS vector;"))
            except Exception:
                pass
