# TaskFlow API — Architecture

```mermaid
flowchart TD
  Client[Browser / API client] --> API[FastAPI application]
  API --> Router[Auth and task routers]
  Router --> Auth[JWT dependency and current-user lookup]
  Router --> CRUD[CRUD operations]
  CRUD --> ORM[SQLAlchemy models]
  ORM --> DB[(SQLite / PostgreSQL)]
  Tests[Pytest + HTTPX] --> API
```

## Responsibilities
- **Routers:** HTTP endpoints, status codes, and request/response handling.
- **Dependencies/security:** bearer-token validation and authenticated-user resolution.
- **CRUD layer:** task persistence and owner-scoped queries.
- **Models/schemas:** relational mapping and input/output validation.
- **Database:** SQLAlchemy sessions against the configured database.

This diagram describes the current repository structure; it is not a claim of a separately deployed service.
