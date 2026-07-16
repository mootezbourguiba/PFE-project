# Testing Instructions

## Backend Foundation Testing Guide

This document provides instructions for testing the backend authentication system that has been implemented in Phase 1.

## Prerequisites

1. Python 3.9 or higher installed
2. Virtual environment created and activated
3. Dependencies installed: `pip install -r requirements.txt`
4. Environment variables configured (copy `.env.example` to `.env`)

## Setup Steps

### 1. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# Set SECRET_KEY to a secure random string
```

### 4. Apply Database Migrations

```bash
# Initialize Alembic (first time only)
alembic upgrade head
```

## Running the Application

### Start the FastAPI Server

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Testing Authentication

### Method 1: Using Swagger UI (Recommended)

1. Open http://localhost:8000/docs in your browser
2. Click on `POST /api/v1/auth/login`
3. Click "Try it out"
4. Enter username and password (you'll need to create a user first)
5. Click "Execute"
6. View the response containing the access token

### Method 2: Using cURL

```bash
# Login request
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=yourpassword"
```

### Method 3: Using Python

```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    data={
        "username": "admin",
        "password": "yourpassword"
    }
)

token = response.json()["access_token"]
print(f"Access token: {token}")
```

## Creating a Test User

Since we don't have a user registration endpoint yet, you can create a test user directly in the database:

### Method 1: Using Python Script

Create a file `create_user.py`:

```python
from backend.database import SessionLocal, init_db
from backend.crud.user import crud_user
from backend.models.user import UserRole

# Initialize database
init_db()

# Create database session
db = SessionLocal()

# Create test user
try:
    user = crud_user.create_user(
        db=db,
        username="admin",
        email="admin@example.com",
        password="admin123",
        role="administrator"
    )
    db.commit()
    print(f"User created: {user.username} (ID: {user.id})")
except Exception as e:
    db.rollback()
    print(f"Error creating user: {e}")
finally:
    db.close()
```

Run the script:
```bash
python create_user.py
```

### Method 2: Using SQLite CLI

```bash
# Open database
sqlite3 avionics.db

# Insert user (password must be bcrypt hashed)
# For testing, you can generate a hash using Python:
# from backend.core.security import get_password_hash
# print(get_password_hash("admin123"))
```

## Validation Checklist

### Database Validation

- [ ] `avionics.db` file created in project root
- [ ] `user` table exists in database
- [ ] `alembic_version` table exists in database
- [ ] User can be created and retrieved

### API Validation

- [ ] Server starts without errors
- [ ] Root endpoint returns API information
- [ ] Health check returns healthy status
- [ ] Swagger UI is accessible at /docs
- [ ] Login endpoint accepts POST requests
- [ ] Login returns 401 for invalid credentials
- [ ] Login returns token for valid credentials

### Authentication Validation

- [ ] Password hashing works (bcrypt)
- [ ] Password verification works
- [ ] JWT token is generated
- [ ] JWT token contains user claims
- [ ] JWT token has expiration time

### Security Validation

- [ ] Passwords are hashed, not plain text
- [ ] JWT tokens are signed with SECRET_KEY
- [ ] CORS is configured for allowed origins
- [ ] Generic error messages (no information leak)

## Troubleshooting

### Server won't start

**Error:** `ModuleNotFoundError: No module named 'backend'`

**Solution:** Ensure you're running from the project root directory, not inside the backend directory.

```bash
# Correct
uvicorn backend.main:app --reload

# Incorrect
cd backend
uvicorn main:app --reload
```

### Database connection error

**Error:** `sqlite3.OperationalError: unable to open database file`

**Solution:** Ensure the directory where the database file will be created has write permissions.

### Migration error

**Error:** `alembic.util.exc.CommandError: Target database is not up to date`

**Solution:** Run migrations:
```bash
alembic upgrade head
```

### Import error

**Error:** `ImportError: cannot import name 'User' from 'backend.models.user'`

**Solution:** Ensure all `__init__.py` files exist in the package directories.

## Next Steps

After validating the authentication system, the next development steps are:

1. Create user registration endpoint
2. Create user management endpoints (CRUD)
3. Implement protected endpoints with JWT validation
4. Create FlightSession model
5. Create TelemetryReading model
6. Create AnomalyEvent model
7. Implement telemetry ingestion endpoints
8. Implement anomaly detection pipeline

## Performance Considerations

- SQLite is suitable for prototype but has limits on concurrent writes
- For production, consider PostgreSQL
- JWT tokens are stateless but cannot be easily revoked
- Consider implementing token refresh mechanism for production

## Security Notes

- Never commit `.env` file to version control
- Use strong SECRET_KEY in production
- Use HTTPS in production
- Implement rate limiting for authentication endpoints
- Consider implementing account lockout after failed attempts
