from __future__ import annotations

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .api.routes import api_router
from .core.settings import settings
from .db.session import init_db

app = FastAPI(title="AiMW", version="0.1.0")

# CORS (оставлено гибким, чтобы фронт можно было выносить отдельно)
allowed = [settings.public_origin] if settings.public_origin else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API
app.include_router(api_router, prefix="/api")

# Static frontend
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND_DIR, "static")), name="static")

@app.get("/", include_in_schema=False)
def index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.on_event("startup")
async def on_startup():
    await init_db()
