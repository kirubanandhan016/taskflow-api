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
