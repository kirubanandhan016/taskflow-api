"""Shared fixtures using a fresh SQLite file for each test."""

import secrets
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client(tmp_path: Path) -> Iterator[TestClient]:
    database_file = tmp_path / "taskflow-test.db"
    application = create_app(
        database_url=f"sqlite:///{database_file.as_posix()}",
        secret_key=secrets.token_urlsafe(48),
    )
    with TestClient(application) as test_client:
        yield test_client


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
