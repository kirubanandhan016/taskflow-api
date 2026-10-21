from datetime import datetime, timedelta, timezone

import jwt

from app.security import ALGORITHM
from tests.conftest import register_and_login


def test_successful_registration_returns_safe_user(client):
    response = client.post(
        "/auth/register",
        json={"email": "new@example.com", "password": "correct-horse-42"},
    )

    assert response.status_code == 201
    assert response.json()["email"] == "new@example.com"
    assert "hashed_password" not in response.json()
    assert "password" not in response.json()


def test_duplicate_registration_returns_conflict(client):
    register_and_login(client, "same@example.com")

    response = client.post(
        "/auth/register",
        json={"email": "same@example.com", "password": "correct-horse-42"},
    )

    assert response.status_code == 409


def test_duplicate_registration_is_case_insensitive(client):
    register_and_login(client, "same@example.com")

    response = client.post(
        "/auth/register",
        json={"email": "SAME@example.com", "password": "another-password-42"},
    )

    assert response.status_code == 409


def test_invalid_registration_data_returns_validation_errors(client):
    invalid_email = client.post(
        "/auth/register",
        json={"email": "not-an-email", "password": "correct-horse-42"},
    )
    short_password = client.post(
        "/auth/register",
        json={"email": "short@example.com", "password": "short"},
    )

    assert invalid_email.status_code == 422
    assert short_password.status_code == 422


def test_successful_login_returns_bearer_token(client):
    register_and_login(client, "login@example.com")

    response = client.post(
        "/auth/login",
        json={"email": "login@example.com", "password": "correct-horse-42"},
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


def test_invalid_login_returns_unauthorized(client):
    register_and_login(client, "login@example.com")

    response = client.post(
        "/auth/login",
        json={"email": "login@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password."


def test_protected_route_rejects_missing_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_protected_route_rejects_invalid_token(client):
    response = client.get(
        "/auth/me", headers={"Authorization": "Bearer not-a-valid-token"}
    )

    assert response.status_code == 401


def test_protected_route_rejects_expired_token(client):
    expired_token = jwt.encode(
        {
            "sub": "1",
            "exp": datetime.now(timezone.utc) - timedelta(seconds=1),
        },
        client.app.state.jwt_secret_key,
        algorithm=ALGORITHM,
    )

    response = client.get(
        "/auth/me", headers={"Authorization": f"Bearer {expired_token}"}
    )

    assert response.status_code == 401


def test_current_user_endpoint_returns_authenticated_user(client):
    headers = register_and_login(client, "me@example.com")

    response = client.get("/auth/me", headers=headers)

    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"


def test_api_documentation_routes_are_available(client):
    assert client.get("/docs").status_code == 200
    assert client.get("/redoc").status_code == 200
    schema_response = client.get("/openapi.json")
    assert schema_response.status_code == 200
    schema = schema_response.json()
    assert schema["components"]["securitySchemes"]["HTTPBearer"]["scheme"] == "bearer"
    assert schema["paths"]["/tasks"]["post"]["security"] == [{"HTTPBearer": []}]
