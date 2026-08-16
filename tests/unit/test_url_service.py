import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.services.url_service import URLService
from app.storage.database import Base


def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def test_create_and_resolve_records_click():
    db = session()
    service = URLService(db, 7)
    record = service.create("https://example.com/path")
    assert record.short_code
    resolved = service.resolve(record.short_code, "pytest", "https://ref.example")
    assert resolved.original_url == "https://example.com/path"
    assert resolved.click_count == 1


def test_invalid_url_is_rejected():
    db = session()
    with pytest.raises(ValueError):
        URLService(db).create("javascript:alert(1)")
