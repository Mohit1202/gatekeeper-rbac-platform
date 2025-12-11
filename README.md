# Gatekeeper RBAC Service

**Gatekeeper RBAC Service** is a FastAPI-based Role-Based Access Control (RBAC) backend service. It provides user authentication, role validation, and asynchronous task execution.

---

## Table of Contents

- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Setup](#setup)  
- [API Endpoints](#api-endpoints)    
- [Implementation Notes](#implementation-notes)

---

## Features

- User management (create, list)  
- Role-based access control (`admin`, `manager`, etc.)  
- JWT-based authentication  
- Asynchronous task execution  
- Health check endpoint  
- Production-ready FastAPI app with CORS enabled  

---

## Tech Stack

- **Backend**: FastAPI  
- **Database**: PostgreSQL  
- **ORM**: SQLAlchemy (sync)  
- **Authentication**: JWT + OAuth2 Password Bearer  
- **Password Hashing**: Bcrypt via Passlib  
- **Background Tasks**: `asyncio`  
- **CORS**: FastAPI CORS middleware (allow all origins)  

---

## Setup

1. **Clone repository**  
```bash
git clone <repo-url>
cd gatekeeper_backend_service
```

2. **Create virtual environment**  
```bash
python -m venv test_env
source test_env/bin/activate
```

3. **Install dependencies**  
```bash
pip install -r requirements.txt
```

4. **Configure environment variables** (e.g., `.env`)  
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=<your_secret_key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

5. **Run the service**  
```bash
uvicorn app.main:app --reload
```

---

## API Endpoints

### Auth
- `POST /auth/login` – Login with username/password, returns JWT token  
- `POST /auth/init` – Initialize default admin user  

### Users
- `POST /users/` – Create a new user (admin-only)  
- `GET /users/` – List all users (admin/manager roles)  

### Tasks
- `POST /tasks/execute` – Execute a background task (manager-only)  
- `GET /tasks/{task_id}` – Fetch task status/results (authenticated)  

### Health
- `GET /health` – Returns `{"status": "ok"}`


## Implementation Notes

1. **Password Handling**  
   - Bcrypt hashing via `passlib.context.CryptContext`  
   - Passwords are never stored in plaintext  

2. **JWT Token**  
   - `sub` contains `user.id`  
   - `role` is included in payload  
   - Expiration configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`  

3. **Role Validation**  
   - `validate_roles` dependency checks `user.role`  
   - Raises `403 Forbidden` if role does not match  

4. **CORS**  
   - Currently allows **all origins**  

5. **Database Table Creation**  
   - Tables are created on startup using `Base.metadata.create_all(bind=engine)`  

6. **FastAPI Lifespan**  
   - Async context manager handles startup/shutdown hooks  
   - Safe for async background tasks  

7. **Swagger / OpenAPI**  
   - JWT token must be set in Swagger **Authorize** dialog  
   - Use `Bearer <access_token>` format  

---
