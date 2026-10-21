# TaskFlow API

TaskFlow API is a beginner-friendly REST API for managing personal tasks. It demonstrates user registration and login, hashed passwords, short-lived JWT bearer tokens, SQLAlchemy persistence, request validation, and automated API tests. Each account can access only its own tasks.

> This is a portfolio and learning project, not a production-ready service. Review the security and production improvements below before using it with real users or sensitive data.

## Features

- Register with a unique email and a validated password.
- Log in and receive a signed, expiring JWT access token.
- Read the authenticated user's profile.
- Create, list, read, update, complete/reopen, and delete tasks.
- Filter tasks by status and priority; paginate with `offset` and `limit`.
- Keep every task query scoped to the authenticated owner.
- Explore the API in Swagger UI or ReDoc.
- Run tests against a fresh SQLite database per test.

## Technology

- Python 3.11+
- FastAPI and Uvicorn
- SQLAlchemy 2.x and SQLite
- Pydantic 2
- PyJWT and pwdlib with Argon2
- python-dotenv, pytest, and FastAPI TestClient

## Architecture

```text
.
├── app/
│   ├── __init__.py
│   ├── config.py          # Environment configuration
│   ├── crud.py            # Database operations
│   ├── database.py        # SQLAlchemy engine and request sessions
│   ├── dependencies.py    # Authentication and session dependencies
│   ├── main.py            # FastAPI app factory and router registration
│   ├── models.py          # SQLAlchemy User and Task models
│   ├── schemas.py         # Pydantic request and response models
│   ├── security.py        # Password hashing and JWT creation
│   └── routers/
│       ├── __init__.py
│       ├── auth.py        # Registration, login, and /me
│       └── tasks.py       # User-scoped task endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py        # Isolated test app and helper
│   ├── test_auth.py
│   └── test_tasks.py
├── .env.example
├── .gitignore
├── main.py                # Optional `main:app` import shim
└── requirements.txt
```

Routes validate HTTP input and delegate persistence to `crud.py`. SQLAlchemy models define stored data and relationships; Pydantic schemas define the public API. The application factory permits tests to use their own database and signing key without touching development data.

### File-by-file guide

- `app/__init__.py` and `app/routers/__init__.py` make the source directories importable Python packages.
- `app/config.py` reads environment variables and validates token expiration.
- `app/database.py` creates a SQLAlchemy engine, enables SQLite foreign keys, and provides request-scoped sessions.
- `app/models.py` defines the database base, status/priority enums, and related `User` and `Task` tables.
- `app/schemas.py` validates API input and controls which user/task fields appear in responses.
- `app/security.py` hashes/verifies passwords and creates JWT access tokens.
- `app/crud.py` contains user and task database queries and writes.
- `app/dependencies.py` provides request sessions and validates bearer tokens to resolve the signed-in user.
- `app/routers/auth.py` implements registration, login, and the authenticated profile endpoint.
- `app/routers/tasks.py` implements task CRUD, filtering, pagination, and ownership checks.
- `app/main.py` builds the FastAPI app, initializes tables at startup, and registers routers.
- Root `main.py` is an optional import shim for running `uvicorn main:app`.
- `tests/conftest.py` creates a new temporary database for each test; `tests/test_auth.py` covers account and token flows; `tests/test_tasks.py` covers task CRUD, validation, pagination, and ownership.
- `requirements.txt` declares installable project and test dependencies; `.env.example` documents configuration with a deliberately unusable secret placeholder; `.gitignore` excludes local secrets, databases, environments, and caches.
- `README.md` documents setup, API usage, security notes, testing, and GitHub publishing steps.

## Setup (Windows PowerShell)

Run these commands from the project directory for a fresh checkout. If `.venv` already exists, keep it and skip the venv creation step:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Generate and save a fresh secret to `.env` without printing it. This replaces only the `JWT_SECRET_KEY` line and preserves the other settings:

```powershell
$secret = (& python -c "import secrets; print(secrets.token_urlsafe(48))").Trim()
$lines = Get-Content .env
$updated = $false
$lines = @($lines | ForEach-Object {
    if ($_ -match '^JWT_SECRET_KEY=') {
        $updated = $true
        "JWT_SECRET_KEY=$secret"
    } else {
        $_
    }
})
if (-not $updated) { $lines += "JWT_SECRET_KEY=$secret" }
Set-Content -Path .env -Value $lines -Encoding utf8
Remove-Variable secret
```

Alternatively, set the values for the current PowerShell window (run the API from that same window):

```powershell
$env:JWT_SECRET_KEY = (& python -c "import secrets; print(secrets.token_urlsafe(48))").Trim()
$env:ACCESS_TOKEN_EXPIRE_MINUTES = "30"
$env:DATABASE_URL = "sqlite:///./taskflow.db"
```

Do not commit `.env`. It is excluded by `.gitignore`. The API requires a configured secret with at least 32 characters and will fail at startup if it is missing or too short.

Optional environment settings:

| Variable | Default | Purpose |
|---|---|---|
| `JWT_SECRET_KEY` | No default | Secret used to sign and verify access tokens |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Positive integer token lifetime |
| `DATABASE_URL` | `sqlite:///./taskflow.db` | SQLAlchemy database URL |

## Run the API

With the virtual environment activated and `.env` configured:

```powershell
python -m uvicorn app.main:app --reload
```

Open:

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

Tables are created automatically when the application starts, using SQLAlchemy metadata. With the default URL, SQLite creates `taskflow.db` in the current project directory when the database is first used. The database file is ignored by Git. This project uses `create_all` for a simple local setup; use versioned migrations when changing an established schema.

## Example API workflow

### 1. Register

`POST /auth/register`

```json
{
  "email": "alex@example.com",
  "password": "a-strong-password-42"
}
```

Successful response (`201 Created`):

```json
{
  "id": 1,
  "email": "alex@example.com",
  "created_at": "2026-10-22T00:00:00Z"
}
```

### 2. Log in

`POST /auth/login`

```json
{
  "email": "alex@example.com",
  "password": "a-strong-password-42"
}
```

The response contains `access_token` and `token_type`. In Swagger, click **Authorize** and paste the token; use the `Bearer` authentication scheme shown in the dialog.

Paste only the `access_token` value into Swagger's **Authorize** dialog, without adding `Bearer `; Swagger adds that prefix to the `Authorization` header. The `/auth/register` and `/auth/login` endpoints accept JSON and do not require authorization. After authorizing, use the lock-marked protected endpoints.

### Authentication troubleshooting

| Response | Meaning | What to check |
|---|---|---|
| `401 Incorrect email or password.` from `/auth/login` | The submitted credentials did not match an account in the configured database. | Confirm registration returned `201`, use the same email and password, and check `DATABASE_URL` has not changed. |
| `401 Missing or invalid authentication credentials.` from `/auth/me` or `/tasks` | The protected request did not include a valid, unexpired bearer token. | Log in successfully, authorize Swagger with the returned token value (without `Bearer `), and log in again if the token expired or the secret was rotated. |
| `409 An account with this email already exists.` | That email is already registered in the configured database. | Log in with that account or use another email; do not delete the database to resolve the conflict. |

### 3. Create and manage tasks

`POST /tasks` (requires a bearer token):

```json
{
  "title": "Prepare backend portfolio",
  "description": "Review the API and write project notes",
  "status": "pending",
  "priority": "high",
  "due_date": "2026-11-01T12:00:00Z"
}
```

Useful endpoints:

| Method | Path | Description |
|---|---|---|
| `POST` | `/auth/register` | Create an account |
| `POST` | `/auth/login` | Obtain an access token |
| `GET` | `/auth/me` | Get the authenticated user |
| `POST` | `/tasks` | Create a task |
| `GET` | `/tasks?status=pending&priority=high&offset=0&limit=20` | List, filter, and paginate your tasks |
| `GET` | `/tasks/{task_id}` | Read one of your tasks |
| `PATCH` | `/tasks/{task_id}` | Update task fields, including status |
| `DELETE` | `/tasks/{task_id}` | Delete a task (`204 No Content`) |

For example, mark a task complete with `PATCH /tasks/1`:

```json
{
  "status": "completed"
}
```

An existing task belonging to another user returns `403 Forbidden`; a task ID that does not exist returns `404 Not Found`.

## Run tests

```powershell
.\.venv\Scripts\Activate.ps1
python -m pytest -q
```

Every test creates a separate database under pytest's temporary directory and supplies a test-only JWT secret. Test runs do not create or modify the development `taskflow.db`.

## Security notes and production improvements

- Passwords are hashed with pwdlib's recommended Argon2 configuration; plaintext passwords are never stored or returned.
- JWT secrets come from environment configuration, not source code; tokens expire after a configurable interval.
- Authentication failures use generic credential messages. Unknown-user login attempts still perform a password-hash verification.
- Task lookups and mutations include the authenticated owner ID.
- `.env`, database files, virtual environments, and caches are ignored by Git.
- For a production deployment, add HTTPS and secure secret storage/rotation, database migrations, rate limiting and abuse monitoring, operational logging/metrics, backups, and a deployment-specific database. Review password policy, token revocation/refresh requirements, CORS, and infrastructure hardening for the intended use case.

## Possible next steps

- Add Alembic migrations, task search, and sorting.
- Add refresh-token rotation or server-side token revocation.
- Add CI with supported Python-version tests and lint/type-check steps.
- Add deployment configuration after choosing a hosting provider and managed database.

## Publish to GitHub (manual)

Publishing is intentionally not performed automatically. Inspect your changes first and ensure no real secrets or database files are staged.

```powershell
# Initialize only when this folder is not already a Git repository.
if (-not (Test-Path .git)) { git init }

git status --short
git add README.md .gitignore .env.example requirements.txt main.py app tests
git diff --cached
git commit -m "Build TaskFlow task management API"
git branch -M main
```

If GitHub CLI is installed and authenticated, create the remote repository and configure `origin`:

```powershell
gh repo create taskflow-api --public --source . --remote origin
git remote -v
git push -u origin main
```

Alternatively, create an empty `taskflow-api` repository on GitHub without initializing it with a README or license, then connect it:

```powershell
# Inspect first and add origin only if it does not already exist.
git remote -v
git remote add origin https://github.com/<YOUR-USERNAME>/taskflow-api.git
git push -u origin main
```

Use one creation method, not both. If `origin` already exists, inspect it and use the correct remote rather than replacing it blindly. Replace `<YOUR-USERNAME>` with your GitHub username. The GitHub repository URL above is a command template, not a claim that a repository exists.
