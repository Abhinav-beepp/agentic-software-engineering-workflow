from collections.abc import Generator
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.config import get_settings
from app.exceptions import NotFoundError
from app.models import AnalyticsResponse, CreateURLRequest, CreateURLResponse
from app.services.url_service import URLService
from app.storage.database import Database
from app.storage.models import URLRecord

router = APIRouter()
settings = get_settings()
database: Database | None = None


def get_database() -> Database:
    global database
    if database is None:
        database = Database(settings.database_url)
    return database


def get_db() -> Generator[Session, None, None]:
    yield from get_database().session()


@router.post(
    "/api/v1/urls",
    response_model=CreateURLResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_url(
    request: Request,
    payload: CreateURLRequest,
    db: Annotated[Session, Depends(get_db)],
) -> CreateURLResponse:
    try:
        record: URLRecord = URLService(db, settings.short_code_length).create(
            str(payload.original_url)
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return CreateURLResponse(
        id=record.id,
        original_url=record.original_url,
        short_code=record.short_code,
        short_url=str(request.base_url).rstrip("/") + f"/{record.short_code}",
        created_at=record.created_at,
    )


@router.get(
    "/api/v1/urls/{short_code}/analytics",
    response_model=AnalyticsResponse,
)
def analytics(
    short_code: str,
    db: Annotated[Session, Depends(get_db)],
) -> AnalyticsResponse:
    try:
        record: URLRecord = URLService(db, settings.short_code_length).analytics(short_code)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return AnalyticsResponse(
        short_code=record.short_code,
        click_count=record.click_count,
        created_at=record.created_at,
        last_clicked_at=record.last_clicked_at,
    )


@router.get("/{short_code}", include_in_schema=False)
def redirect(
    short_code: str,
    request: Request,
    db: Annotated[Session, Depends(get_db)],
) -> RedirectResponse:
    try:
        record: URLRecord = URLService(db, settings.short_code_length).resolve(
            short_code,
            request.headers.get("user-agent"),
            request.headers.get("referer"),
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return RedirectResponse(record.original_url, status_code=307)
