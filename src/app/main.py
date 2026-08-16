from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import url_routes
from app.config import get_settings
from app.logging import configure_logging

settings = get_settings()
configure_logging(settings.log_level)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    try:
        yield
    finally:
        if url_routes.database is not None:
            url_routes.database.close()
            url_routes.database = None


app = FastAPI(
    title="Agentic URL Shortener",
    version="1.0.0",
    description=("Runnable URL shortener plus agentic software-engineering workflow prototype."),
    lifespan=lifespan,
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(url_routes.router)
