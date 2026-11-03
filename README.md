# TaskFlow API

Task management REST API built with Python, FastAPI, SQLAlchemy, and SQLite. It demonstrates account registration, token-based authentication, protected task CRUD, resource ownership, and automated API tests.

## Features

- User registration and login
- Argon2 password hashing through pwdlib
- Signed JWT bearer access tokens with required `sub`, `iat`, and `exp` claims
- User-scoped task creation, retrieval, update, and deletion
- Task filtering by status and priority, with pagination
- SQLAlchemy ORM and request-scoped database sessions
- Pydantic request validation
- Consistent HTTP error responses
- Pytest API and authorization tests
- GitHub Actions test workflow

## Technology

Python 3.10+ · FastAPI · SQLAlchemy · SQLite · PyJWT · pwdlib/Argon2 · Pydantic · Pytest · HTTPX · Uvicorn

## Architecture

- `app/routers/`: HTTP route handlers
- `app/schemas.py`: Pydantic request and response models
- `app/models.py`: SQLAlchemy user and task entities
- `app/crud.py`: database operations, separated from HTTP concerns
- `app/security.py`: password hashing and JWT issuance
- `app/dependencies.py`: database session and bearer-token authentication dependencies
- `app/config.py`: environment-based configuration
- `app/database.py`: SQLAlchemy engine and session factory
- `tests/`: authentication, authorization, and task behavior tests

## Run locally

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/kirubanandhan016/taskflow-api.git
cd taskflow-api
python -m venv .venv
```

Activate the environment:

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Configuration

Copy the environment template:

```powershell
Copy-Item .env.example .env
```

Generate a unique signing secret:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Set `JWT_SECRET_KEY` in `.env` to the generated value. The application requires a unique secret of at least 32 characters and a positive token lifetime. Do not commit `.env`, passwords, or bearer tokens.

The default local database is `sqlite:///./taskflow.db`. Set `DATABASE_URL` to use another SQLAlchemy-compatible database URL.

## Start the API

```bash
uvicorn app.main:app --reload
```

- Base URL: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Authentication flow

1. Register using `POST /auth/register` with email and password.
2. Log in using `POST /auth/login` with the same JSON credential fields.
3. Read `access_token` from the response.
4. Send `Authorization: Bearer <access_token>` with protected requests.
5. The server verifies the signature and required `exp`, `sub`, and `iat` claims, resolves the user from the database, and then applies endpoint authorization.

Passwords are hashed using Argon2; plaintext passwords are not stored. JWTs use HS256 and the application-configured secret. Access tokens are stateless and short-lived (30 minutes by default). There is no refresh-token or server-side revocation endpoint in this project.

## API endpoints

### Authentication

| Method | Endpoint | Access | Purpose |
|---|---|---|---|
| POST | `/auth/register` | Public | Register a user |
| POST | `/auth/login` | Public | Exchange credentials for a bearer token |
| GET | `/auth/me` | Bearer token | Retrieve the current user |

### Tasks

| Method | Endpoint | Access | Purpose |
|---|---|---|---|
| POST | `/tasks` | Bearer token | Create a task |
| GET | `/tasks` | Bearer token | List and filter the current user's tasks |
| GET | `/tasks/{task_id}` | Bearer token | Retrieve an owned task |
| PATCH | `/tasks/{task_id}` | Bearer token | Update an owned task |
| DELETE | `/tasks/{task_id}` | Bearer token | Delete an owned task |

Task list supports `status`, `priority`, `offset`, and `limit` query parameters. A user cannot read, modify, or delete another user's task.

## Example request

Register:

```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "correct-horse-42"
}
```

Create a task:

```http
POST /tasks
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Prepare backend interview",
  "description": "Review FastAPI and SQLAlchemy",
  "priority": "high"
}
```

## Error handling

- `401 Unauthorized`: missing, invalid, malformed, or expired bearer token
- `403 Forbidden`: task exists but belongs to another user
- `404 Not Found`: task does not exist
- `409 Conflict`: duplicate account registration
- `422 Unprocessable Entity`: invalid request data

## Tests

Run:

```bash
python -m pytest -v
```

The tests cover registration, duplicate accounts, input validation, successful and unsuccessful login, missing/invalid/expired tokens, token claim requirements, task CRUD, and per-user access boundaries. GitHub Actions runs the suite on pushes and pull requests.

## Scope and limitations

This is a learning and portfolio project, not a production identity platform. Rate limiting, refresh-token rotation, immediate token revocation, structured security audit logging, and production deployment hardening are not currently implemented.

## Author

**Kirubanandhan V**

- GitHub: [@kirubanandhan016](https://github.com/kirubanandhan016)
- Portfolio: [kirubanandhan016.github.io](https://kirubanandhan016.github.io/)
- LinkedIn: [Kirubanandhan V](https://www.linkedin.com/in/kirubanandhan-v-98bb83443/)
