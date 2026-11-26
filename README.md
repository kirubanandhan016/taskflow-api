# TaskFlow API

[![Python tests](https://github.com/kirubanandhan016/taskflow-api/actions/workflows/tests.yml/badge.svg)](https://github.com/kirubanandhan016/taskflow-api/actions/workflows/tests.yml)

A task-management REST API built with Python and FastAPI. The project demonstrates user registration, JWT-based authentication, protected task CRUD endpoints, and user-level resource isolation.

## Features

- User registration and login
- JWT bearer authentication for protected endpoints
- Create, list, retrieve, update, and delete tasks
- User-specific task access and ownership checks
- SQLAlchemy ORM with SQLite by default and PostgreSQL configuration support
- Pydantic request validation and structured HTTP errors
- Interactive Swagger UI and OpenAPI documentation
- Pytest coverage for authentication, authorization, validation, and task workflows

## Technology stack

Python · FastAPI · SQLAlchemy · SQLite · PostgreSQL · JWT · Pydantic · Pytest · Uvicorn

## Project structure

```text
taskflow-api/
├── app/
│   ├── routers/
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── __init__.py
│   ├── config.py
│   ├── crud.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── security.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_tasks.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Request flow and architecture

```mermaid
flowchart TD
    C[API client] --> R[FastAPI routers]
    R --> A[JWT authentication dependency]
    R --> CRUD[CRUD operations]
    CRUD --> ORM[SQLAlchemy models]
    ORM --> DB[(SQLite / PostgreSQL)]
    T[Pytest suite] --> R
```

The routers define the HTTP interface, authentication dependencies identify the current user, and CRUD operations apply user-scoped database access through SQLAlchemy.

## Run locally

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/kirubanandhan016/taskflow-api.git
cd taskflow-api
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Environment configuration

Copy `.env.example` to `.env` and set a unique JWT secret. Generate one with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Set the generated secret using the variable name documented in `.env.example`. SQLite is the default local database. To use PostgreSQL, configure `DATABASE_URL` with a SQLAlchemy URL, for example:

```env
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/taskflow
```

Never commit `.env`, credentials, database passwords, or access tokens.

## Start the API

```bash
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Run with Docker Compose

Docker Compose starts PostgreSQL and the FastAPI application. The production application uses Alembic migrations. The Docker entrypoint runs `alembic upgrade head` before starting Uvicorn. The test app factory retains an explicit schema-creation option for isolated tests.

PowerShell:

```powershell
$env:POSTGRES_PASSWORD = "use-a-long-local-password"
$env:JWT_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(48))"
docker compose up --build
```

macOS/Linux:

```bash
export POSTGRES_PASSWORD='use-a-long-local-password'
export JWT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
docker compose up --build
```

Open `http://localhost:8000/docs`. Stop with `docker compose down`; add `-v` only when you intentionally want to delete the local PostgreSQL data volume. Use a URL-safe alphanumeric database password for this Compose example and never reuse local credentials in production.

## Database migrations

After setting `DATABASE_URL` and `JWT_SECRET_KEY`, apply the versioned schema:

```bash
alembic upgrade head
```

Inspect the current revision with `alembic current`. Generate a candidate migration after model changes with `alembic revision --autogenerate -m "describe change"`, then review the generated operations before committing.

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a user |
| POST | `/auth/login` | Authenticate and receive an access token |
| GET | `/auth/me` | Get the authenticated user |
| POST | `/tasks` | Create a task |
| GET | `/tasks` | List the authenticated user's tasks |
| GET | `/tasks/{task_id}` | Retrieve one of the user's tasks |
| PATCH | `/tasks/{task_id}` | Update one of the user's tasks |
| DELETE | `/tasks/{task_id}` | Delete one of the user's tasks |

Protected endpoints require an `Authorization: Bearer <access_token>` header. Refer to the generated OpenAPI documentation for exact request and response schemas.

## Run tests

```bash
python -m pytest -v
```

The repository's GitHub Actions workflow runs automated tests using isolated SQLite test data and performs a PostgreSQL connectivity/schema smoke check. Review the workflow file for the exact CI steps.

## Engineering concepts demonstrated

- RESTful API design and HTTP status handling
- Authentication and resource-level authorization
- ORM-based relational database access
- Request validation and error handling
- Automated API testing
- Environment-based configuration
- CI with GitHub Actions

## Scope and future improvements

This is a learning and portfolio project, not a production service. Potential next improvements include Alembic migrations, pagination and filtering, refresh-token rotation and revocation, rate limiting, structured logging, and deployment hardening.

## Author

**Kirubanandhan V**  
Entry-Level Python Backend Developer

- GitHub: https://github.com/kirubanandhan016
- Portfolio: https://kirubanandhan016.github.io/
- LinkedIn: https://www.linkedin.com/in/kirubanandhan-v-98bb83443/
- Email: kirubanandhan016@gmail.com


## Portfolio documentation

- [Architecture diagram](docs/ARCHITECTURE.md)
- [Database ER diagram](docs/ER_DIAGRAM.md)
- [API request examples](docs/API_EXAMPLES.md)
- Swagger/OpenAPI: run the API and open `/docs`; ReDoc is at `/redoc`.
- [Environment template](.env.example); copy to `.env` and never commit real secrets.
- Tests: `python -m pytest -v`; see `tests/` and GitHub Actions.

## Screenshots and deployment

A verified public deployment URL and committed screenshots are not available yet. Capture Swagger UI and representative successful/error API responses after running locally, redact tokens and personal data, and store approved images under `docs/screenshots/`. Add a live URL here only after deployment and health-check verification.


## Deploy to Render

This repository includes a Render Blueprint at [`render.yaml`](render.yaml).

1. Sign in to [Render](https://render.com/) and choose **New → Blueprint**.
2. Connect your GitHub account and select `kirubanandhan016/taskflow-api`.
3. Review the web service and PostgreSQL database defined in `render.yaml`, then apply the Blueprint.
4. Wait for the build and deployment to finish. Render runs Alembic migrations before starting Uvicorn.
5. Open the generated service URL and verify `/health`, `/docs`, and `/redoc`.
6. Copy the verified public URL into the Deployment section below.

Render generates `JWT_SECRET_KEY` and injects the managed PostgreSQL connection string. Do not paste secrets into GitHub or chat. The included free database plan is intended for a demonstration and may have provider-specific expiry or resource limits; use a paid persistent database plan for a portfolio deployment you need to keep available.

### Deployment status

- Provider configuration: committed in `render.yaml`.
- Public service URL: pending creation in the Render dashboard.
- Health check: `/health` (verify after deployment).
