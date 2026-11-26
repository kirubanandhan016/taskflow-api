# TaskFlow API — Request Examples

Start the API with `uvicorn app.main:app --reload`, then use the interactive schema at [Swagger UI](http://127.0.0.1:8000/docs).

## Register
```http
POST /auth/register
Content-Type: application/json

{"email":"dev@example.com","password":"ChangeThisPassword123"}
```

## Authenticate
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=dev%40example.com&password=ChangeThisPassword123
```

## Create a task
```http
POST /tasks
Authorization: Bearer <access_token>
Content-Type: application/json

{"title":"Prepare backend interview","description":"Revise FastAPI and SQLAlchemy"}
```

Use the exact field names and required fields shown by the running OpenAPI schema; examples are illustrative and use no real credentials.
