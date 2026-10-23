# Job Application & Interview Management API

A RESTful backend API built with **Python and FastAPI** for managing job applications and interview schedules. The API provides JWT-based authentication, PostgreSQL persistence, user-level authorization, application search/filtering, interview management, automated tests, and Docker support.

## Features

- User registration and login
- JWT-based authentication
- Password hashing using Argon2
- Create, view, update, and delete job applications
- Search applications by company or role
- Filter applications by status
- Schedule interviews for job applications
- Retrieve interview schedules
- User-level authorization
- Protected API endpoints
- PostgreSQL database integration
- SQLAlchemy ORM
- Swagger/OpenAPI documentation
- Automated API testing with Pytest
- Docker and Docker Compose support

## Technology Stack

- **Language:** Python
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT
- **Password Hashing:** Argon2
- **Testing:** Pytest
- **Containerization:** Docker, Docker Compose
- **API Documentation:** Swagger/OpenAPI

## Project Structure

```text
job-application-api-complete/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   │
│   └── routes/
│       ├── __init__.py
│       ├── auth.py
│       ├── applications.py
│       └── interviews.py
│
├── tests/
│   ├── __init__.py
│   └── test_main.py
│
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Authenticate user and generate JWT |

### Job Applications

| Method | Endpoint | Description |
|---|---|---|
| POST | `/applications` | Create a job application |
| GET | `/applications` | Get the current user's applications |
| GET | `/applications/{application_id}` | Get a specific application |
| PUT | `/applications/{application_id}` | Update an application |
| DELETE | `/applications/{application_id}` | Delete an application |

The applications endpoint also supports:

```text
GET /applications?search=Amazon
GET /applications?status=Interview
```

### Interviews

| Method | Endpoint | Description |
|---|---|---|
| POST | `/interviews` | Schedule an interview |
| GET | `/interviews` | Get the current user's interviews |
| GET | `/interviews/{interview_id}` | Get a specific interview |

## Authentication

Protected endpoints require a JWT access token.

### 1. Register

Send a request to:

```text
POST /auth/register
```

Example:

```json
{
  "name": "Test User",
  "email": "test@example.com",
  "password": "Test@123"
}
```

### 2. Login

Send a request to:

```text
POST /auth/login
```

The API returns an access token.

### 3. Authorize in Swagger

Open the Swagger documentation and click **Authorize**.

Use the returned bearer token to access protected endpoints.

## Local Setup

### 1. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create the PostgreSQL database

Create a PostgreSQL database named:

```text
job_application_db
```

### 4. Configure environment variables

Create a `.env` file or configure the required environment variables:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/job_application_db
SECRET_KEY=replace-with-a-long-random-secret
```

Do not commit `.env` to GitHub.

### 5. Start the API

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Running with Docker

Docker Compose starts both the PostgreSQL database and FastAPI application.

```bash
docker compose up --build
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

The PostgreSQL service includes a health check so the API waits for the database to become ready before starting.

To stop the containers:

```bash
docker compose down
```

## Testing

The project includes automated API tests using Pytest.

Run:

```bash
pytest -v
```

The current test suite covers:

- API health check
- User registration
- Duplicate email handling
- Login and JWT generation
- Application creation
- Application retrieval
- Application search
- Authentication protection
- Application updates
- Application deletion
- Interview creation
- Interview retrieval
- User-level authorization

Current test result:

```text
14 passed
```

## Security

The API implements:

- JWT authentication for protected endpoints
- Password hashing using Argon2
- User-level authorization
- Protection against unauthorized access to applications and interviews
- Environment-based configuration for database credentials and secret keys

## API Documentation

FastAPI automatically provides interactive Swagger/OpenAPI documentation.

After starting the application, visit:

```text
http://127.0.0.1:8000/docs
```

The documentation can be used to register users, authenticate, authorize with JWT, and test the API endpoints interactively.