"""Small environment-based application settings."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    database_url: str
    jwt_secret_key: str | None
    access_token_expire_minutes: int


def load_settings() -> Settings:
    """Read settings from the environment, using only a local SQLite default."""
    raw_expiration = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    try:
        expiration = int(raw_expiration)
    except ValueError as exc:
        raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be a positive integer.") from exc
    if expiration <= 0:
        raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be a positive integer.")

    return Settings(
        database_url=os.getenv("DATABASE_URL", "sqlite:///./taskflow.db"),
        jwt_secret_key=os.getenv("JWT_SECRET_KEY"),
        access_token_expire_minutes=expiration,
    )
