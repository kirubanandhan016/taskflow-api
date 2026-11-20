"""Shared fixtures using isolated SQLite locally and PostgreSQL in CI."""

import os
import secrets
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from app.main import create_app
from app.models import Base


@pytest.fixture
def client(tmp_path: Path) -> Iterator[TestClient]:
    test_database_url = os.getenv("TEST_DATABASE_URL")
    if test_database_url:
        engine = create_engine(test_database_url, pool_pre_ping=True)
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        database_url = test_database_url
    else:
        database_file = tmp_path / "taskflow-test.db"
        database_url = f"sqlite:///{database_file.as_posix()}"
        engine = None

    application = create_app(
        database_url=database_url,
        secret_key=secrets.token_urlsafe(48),
        create_schema=engine is None,
    )
    try:
        with TestClient(application) as test_client:
            yield test_client
    finally:
        if engine is not None:
            Base.metadata.drop_all(bind=engine)
            engine.dispose()


def register_and_login(
    client: TestClient,
    email: str,
    password: str = "correct-horse-42",
) -> dict[str, str]:
    registration = client.post(
        "/auth/register", json={"email": email, "password": password}
    )
    assert registration.status_code == 201
    login = client.post("/auth/login", json={"email": email, "password": password})
    assert login.status_code == 200
    return {"Authorization": f"Bearer {login.json()['access_token']}"}
