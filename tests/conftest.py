from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.api import url_routes
from app.main import app
from app.storage.database import Database


@pytest.fixture()
def client(tmp_path, monkeypatch) -> Generator[TestClient, None, None]:
    db = Database(f"sqlite:///{tmp_path / 'test.db'}")
    monkeypatch.setattr(url_routes, "database", db)
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        db.close()
