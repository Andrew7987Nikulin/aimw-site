from __future__ import annotations

async def execute(text: str, intent: str, context: dict) -> dict:
    # TODO: adapter.generate(messages=[...], model=..., temperature=...)
    sources = context.get("sources", [])
    hint = ""
    if sources:
        hint = " Я учёл найденные источники из памяти."

    if intent == "debug":
        return {
            "message": "Похоже, это запрос на дебаг. Пришли лог/traceback и укажи окружение (OS, версия Python, зависимости) — разберём по шагам." + hint,
            "kind": "assistant",
        }

    if intent == "architecture":
        return {
            "message": "Если кратко: AiMW берёт на себя маршрутизацию, память и retrieval, чтобы клиенты говорили с одним API, а внутри можно свободно менять модели/агентов/хранилища." + hint,
            "kind": "assistant",
        }

    if intent == "build":
        return {
            "message": "Ок. Я могу разложить задачу на компоненты (API, пайплайн, память, адаптеры, метрики) и выдать план + структуру репозитория." + hint,
            "kind": "assistant",
        }

    return {
        "message": "Принято. Это демо-ответ AiMW. Для реального исполнения подключи LLM адаптер в execution.py и добавь правила маршрутизации." + hint,
        "kind": "assistant",
    }
