from __future__ import annotations

import datetime as dt
import uuid
from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: uuid.uuid4().hex)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=lambda: dt.datetime.now(dt.timezone.utc))
    namespace: Mapped[str] = mapped_column(String(64), index=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    # embedding хранится отдельно/опционально в pgvector. Для SQLite-демо не используем.
