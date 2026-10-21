"""Registration, login, and current-user endpoints."""

from fastapi import APIRouter, HTTPException, Request, status

from app import crud
from app.dependencies import CurrentUser, DatabaseSession
from app.schemas import TokenResponse, UserCreate, UserLogin, UserRead
from app.security import (
    burn_password_verification,
    create_access_token,
    hash_password,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register a user",
    description="Create an account using a unique email address and a password of at least 8 characters.",
    responses={409: {"description": "An account with this email already exists."}},
)
def register(payload: UserCreate, session: DatabaseSession) -> UserRead:
    email = str(payload.email).lower()
    if crud.get_user_by_email(session, email) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )
    try:
        user = crud.create_user(session, email, hash_password(payload.password))
    except crud.UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        ) from None
    return UserRead.model_validate(user)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Log in",
    description="Exchange valid account credentials for a short-lived bearer access token.",
    responses={401: {"description": "Incorrect email or password."}},
)
def login(
    payload: UserLogin,
    request: Request,
    session: DatabaseSession,
) -> TokenResponse:
    email = str(payload.email).lower()
    user = crud.get_user_by_email(session, email)
    if user is None:
        burn_password_verification(payload.password)
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(
        subject=str(user.id),
        secret_key=request.app.state.jwt_secret_key,
        expires_in_minutes=request.app.state.access_token_expire_minutes,
    )
    return TokenResponse(access_token=token)


@router.get(
    "/me",
    response_model=UserRead,
    summary="Get the current user",
    description="Return the account associated with the supplied bearer access token.",
    responses={401: {"description": "Missing or invalid bearer token."}},
)
def read_current_user(current_user: CurrentUser) -> UserRead:
    return UserRead.model_validate(current_user)
