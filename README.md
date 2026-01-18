# AiMW Minimal Site (Frontend + FastAPI Backend)

Минималистичный сайт с мягкой палитрой и лёгкими киберпанк-акцентами + backend на FastAPI.
Есть демо-пайплайн обработки запроса и простая память (SQLite по умолчанию). Под PostgreSQL+pgvector предусмотрены заготовки.

## Быстрый старт (SQLite по умолчанию)
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Открой: http://127.0.0.1:8000

## Docker (Postgres + pgvector)
```bash
docker compose up --build
```
Открой: http://127.0.0.1:8000

### Переменные окружения
- `AIMW_DB_URL` — если не задано, используется SQLite: `sqlite:///./aimw.db`
- `AIMW_PUBLIC_ORIGIN` — для CORS (например, `http://localhost:8000`)

## API
- `GET /api/health`
- `POST /api/chat` — демо-обработка запроса + trace пайплайна
- `POST /api/memory/write` — запись документа в память
- `POST /api/memory/search` — семантический поиск (простая реализация для демо)

> В проекте пока нет реального провайдера LLM (чтобы не тянуть ключи). Место подключения — `app/core/execution.py`. Добавим в течение 1-2 недель
