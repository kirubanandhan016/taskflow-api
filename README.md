# 🚀 TaskFlow API

### A Secure Task Management REST API Built with FastAPI

A backend application that provides secure user authentication and task management through RESTful APIs. Built with **FastAPI, SQLAlchemy, SQLite, and JWT authentication**, with automated tests covering authentication, authorization, and task operations.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-Framework-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge" alt="SQLAlchemy" />
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/Pytest-Testing-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" alt="Pytest" />
</p>

---

## 📌 Overview

**TaskFlow API** is a RESTful backend project designed to demonstrate core backend development concepts, including authentication, protected endpoints, database integration, input validation, and automated testing.

Users can register an account, log in to receive an access token, and manage their own tasks through authenticated API endpoints.

## ✨ Features

- 🔐 **User Authentication** — User registration and login.
- 🪪 **JWT Authorization** — Bearer-token authentication for protected endpoints.
- 👤 **User-Specific Access** — Users can access and manage only their own tasks.
- ✅ **Task Management** — Create, retrieve, update, and delete tasks.
- 🗄️ **Database Integration** — SQLAlchemy ORM with SQLite.
- 🛡️ **Input Validation** — Request validation and structured HTTP error responses.
- 📚 **Interactive API Documentation** — Swagger UI and OpenAPI documentation.
- 🧪 **Automated Testing** — Pytest coverage for authentication, authorization, and task operations.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API framework |
| SQLAlchemy | Database ORM |
| SQLite | Relational database |
| JWT | Token-based authentication |
| Pytest | Automated testing |
| Uvicorn | ASGI development server |

## 📂 Project Structure

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
├── main.py
├── requirements.txt
└── README.md
```

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/kirubanandhan016/taskflow-api.git
cd taskflow-api

### 2. Create a Virtual Environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a local `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

Generate a strong, unique JWT secret:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Add the generated value to your local `.env` file:

```env
JWT_SECRET_KEY=your_generated_secret_here
```

Use the other environment variables documented in `.env.example`, if required by your application.

**Security:** Never commit `.env`, access tokens, passwords, or secret keys to GitHub. Keep `.env.example` free of real credentials.

### 5. Start the API Server

From the project root, run:

```bash
uvicorn app.main:app --reload
```

The development server will be available at:

- **API Base URL:** http://127.0.0.1:8000
- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## 🔗 API Endpoints

### Authentication

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/auth/register` | Register a new user | Public |
| POST | `/auth/login` | Authenticate and receive an access token | Public |
| GET | `/auth/me` | Retrieve the current authenticated user | Protected |

### Task Management

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/tasks` | Create a task | Protected |
| GET | `/tasks` | List the current user's tasks | Protected |
| GET | `/tasks/{task_id}` | Retrieve a task by ID | Protected |
| PATCH | `/tasks/{task_id}` | Update a task | Protected |
| DELETE | `/tasks/{task_id}` | Delete a task | Protected |

*Protected endpoints require a valid Bearer access token.*

## 🧪 Running Tests

Run the automated test suite from the project root:

```bash
python -m pytest -v
```

The test suite covers:

- Successful and duplicate user registration
- Successful and unsuccessful login
- Missing and invalid authentication tokens
- Current-user retrieval
- Task creation and CRUD operations
- User-specific task isolation
- Unauthorized access to another user's tasks
- Request validation errors
- API documentation availability

The repository includes tests for registration, login, authentication, task CRUD, user isolation, validation, and API documentation. Run the command above in your environment to verify the current result.

## 🔒 Security Considerations

- JWT secrets are loaded through environment configuration.
- Protected endpoints require authentication.
- Task access is restricted to the authenticated user.
- Passwords should be stored using secure password hashing.
- Local environment files and database files are excluded from version control.

## 🎯 What This Project Demonstrates

This project showcases practical backend development skills:

- Designing RESTful API endpoints
- Implementing token-based authentication
- Integrating an ORM with a relational database
- Validating requests and handling HTTP errors
- Enforcing resource-level authorization
- Writing automated API tests
- Managing environment configuration and Git exclusions

## 👨‍💻 Author

**Kiruba Harish**

Aspiring Python Backend Developer

Interested in building secure, maintainable backend applications and REST APIs.

- GitHub: [@kirubanandhan016](https://github.com/kirubanandhan016)
- LinkedIn: [Connect with me](https://www.linkedin.com/in/kirubanandhan-v-98bb83443/)

---

<p align="center">
  <strong>Built with Python and FastAPI.</strong><br/>
  Learning, building, and improving one API at a time. 🚀
</p>
