# Python Reference — Live Developer Stack

## Runtime & Environment

- Python **3.11+** required. Use `pyproject.toml` with `[project]` table (PEP 517).
- Virtual environments: `python -m venv .venv`. Always activate before running.
- Dependency pinning: `pip-compile` (pip-tools) or `uv` for fast resolution.
- For Proxmox/Ubuntu VM deployments: use `--break-system-packages` only when outside a venv.

## Preferred Libraries

| Purpose | Library |
|---|---|
| HTTP API server | FastAPI + uvicorn |
| HTTP client | `httpx` (async-first) |
| Data validation | Pydantic v2 |
| CLI tools | Typer |
| Database (PostgreSQL) | SQLAlchemy 2 + asyncpg |
| Background tasks | Celery + Redis, or ARQ |
| Testing | pytest + pytest-asyncio |
| Env management | python-dotenv |
| Logging | `structlog` |

## Code Patterns

### Async FastAPI Endpoint

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import structlog

logger = structlog.get_logger()
app = FastAPI()

class ItemRequest(BaseModel):
    name: str
    value: float

@app.post("/items", status_code=201)
async def create_item(body: ItemRequest) -> dict:
    try:
        result = await item_service.create(body.name, body.value)
        return {"id": result.id, "status": "created"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.exception("Unexpected error in create_item")
        raise HTTPException(status_code=500, detail="Internal error")
```

### Agent Step Function (MCP / pipeline context)

```python
from dataclasses import dataclass
from typing import Any

@dataclass
class StepResult:
    success: bool
    data: Any
    error: str | None = None

async def process_step(input_data: dict) -> StepResult:
    """Single agent step. Receives structured input, returns StepResult."""
    try:
        # --- processing logic here ---
        output = await transform(input_data)
        return StepResult(success=True, data=output)
    except Exception as e:
        return StepResult(success=False, data=None, error=str(e))
```

### SQLAlchemy 2 Async Query

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Project

async def get_project(session: AsyncSession, project_id: int) -> Project | None:
    result = await session.execute(
        select(Project).where(Project.id == project_id)
    )
    return result.scalar_one_or_none()
```

## Testing Conventions

```python
# tests/test_items.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_create_item_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/items", json={"name": "widget", "value": 9.99})
    assert response.status_code == 201
    assert response.json()["status"] == "created"
```

## Project Layout

```
project/
├── pyproject.toml
├── .env.example
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app factory
│   ├── config.py        # Settings via pydantic-settings
│   ├── models/          # SQLAlchemy models
│   ├── services/        # Business logic
│   ├── routes/          # FastAPI routers
│   └── agents/          # Agent step functions
└── tests/
    ├── conftest.py
    └── test_*.py
```

## Common Pitfalls

- Never use `asyncio.run()` inside an async context — use `await`.
- Don't mix sync DB drivers with async code; use `asyncpg` not `psycopg2` for async.
- Always close `httpx.AsyncClient` via context manager or `aclose()`.
- Pydantic v2 models: use `model_config = ConfigDict(from_attributes=True)` for ORM mode.
