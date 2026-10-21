"""Application factory and FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import load_settings
from app.database import create_database
from app.models import Base
from app.routers import auth, tasks


def create_app(
    *,
    database_url: str | None = None,
    secret_key: str | None = None,
    access_token_expire_minutes: int | None = None,
) -> FastAPI:
    settings = load_settings()
    selected_database_url = (
        settings.database_url if database_url is None else database_url
    )
    selected_secret_key = (
        settings.jwt_secret_key if secret_key is None else secret_key
    )
    expiration = (
        settings.access_token_expire_minutes
        if access_token_expire_minutes is None
        else access_token_expire_minutes
    )
    if expiration <= 0:
        raise ValueError("Access-token expiration must be a positive integer.")
    engine, session_factory = create_database(selected_database_url)

    @asynccontextmanager
    async def lifespan(application: FastAPI):
        try:
            if not selected_secret_key or len(selected_secret_key) < 32:
                raise RuntimeError(
                    "Set JWT_SECRET_KEY to a randomly generated value of at least 32 characters."
                )
            application.state.jwt_secret_key = selected_secret_key
            application.state.access_token_expire_minutes = expiration
            application.state.session_factory = session_factory
            Base.metadata.create_all(bind=engine)
            yield
        finally:
            engine.dispose()

    application = FastAPI(
        title="TaskFlow API",
        description=(
            "A user-scoped task management REST API with JWT authentication.\n\n"
            "**Swagger authentication:** Register at `POST /auth/register`, then "
            "log in at `POST /auth/login`. Copy the `access_token` value from the "
            "response, click **Authorize**, and paste the token value without the "
            "`Bearer ` prefix. Swagger adds the bearer prefix to protected requests."
        ),
        version="1.0.0",
        lifespan=lifespan,
    )
    application.include_router(auth.router)
    application.include_router(tasks.router)
    return application


app = create_app()
