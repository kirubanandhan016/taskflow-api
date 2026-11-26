# TaskFlow API — Database ER Diagram

```mermaid
erDiagram
  USERS ||--o{ TASKS : owns
  USERS {
    int id PK
    string email UK
    string hashed_password
  }
  TASKS {
    int id PK
    string title
    text description
    bool completed
    int owner_id FK
  }
```

The diagram captures the user-to-task ownership relationship represented by the application models. Check `app/models.py` and Alembic migrations for the authoritative column definitions.
