"""Password hashing and JWT access-token helpers."""

from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

ALGORITHM = "HS256"
password_hash = PasswordHash.recommended()
_DUMMY_PASSWORD_HASH = password_hash.hash("not-a-real-user-password")


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def burn_password_verification(password: str) -> None:
    """Perform a password hash check for unknown accounts to reduce timing clues."""
    password_hash.verify(password, _DUMMY_PASSWORD_HASH)


def create_access_token(
    subject: str, secret_key: str, expires_in_minutes: int
) -> str:
    if not secret_key or len(secret_key) < 32:
        raise ValueError("JWT signing secret must contain at least 32 characters.")
    if expires_in_minutes <= 0:
        raise ValueError("Access-token lifetime must be a positive integer.")

    issued_at = datetime.now(timezone.utc)
    expires_at = issued_at + timedelta(minutes=expires_in_minutes)
    return jwt.encode(
        {
            "sub": str(subject),
            "iat": issued_at,
            "exp": expires_at,
        },
        secret_key,
        algorithm=ALGORITHM,
    )
