# FastShip Delivery Service API

A full-featured shipment management API built with FastAPI. Sellers create shipments, delivery partners handle fulfillment, and customers receive real-time notifications via email and SMS. Includes tracking pages, review collection, and background task processing with Celery.

## Tech Stack

| Layer            | Technology                              |
|------------------|-----------------------------------------|
| Framework        | FastAPI (async)                         |
| Database         | PostgreSQL 16 (asyncpg driver)          |
| Cache            | Redis 7 (token blacklisting + Celery broker) |
| ORM              | SQLAlchemy 2.0 + SQLModel               |
| Auth             | JWT (PyJWT) + bcrypt via passlib        |
| Task Queue       | Celery + Flower (monitoring)            |
| Email            | FastAPI-Mail (aiosmtplib)               |
| SMS              | Twilio                                  |
| Migrations       | Alembic                                 |
| API Docs         | Scalar (`/scalar`)                      |
| Containerization | Docker + Docker Compose                 |

## Project Structure

```
app/
├── main.py                          # FastAPI app, lifespan, CORS, middleware
├── config.py                        # Pydantic Settings (DB, Redis, JWT, Mail, Twilio)
│
├── api/
│   ├── router.py                    # Master router (includes all sub-routers)
│   ├── dependencies.py              # Dependency injection (auth, services, sessions)
│   ├── routers/
│   │   ├── seller.py                # Seller auth + password reset endpoints
│   │   ├── delivery_partner.py      # Delivery partner auth + profile endpoints
│   │   └── shipment.py              # Shipment CRUD, tracking, tags, reviews
│   └── schemas/
│       ├── seller.py                # Seller request/response schemas
│       ├── delivery_partner.py      # Partner request/response schemas
│       └── shipment.py              # Shipment request/response schemas
│
├── core/
│   ├── security.py                  # OAuth2 bearer scheme
│   └── exceptions.py               # Custom exception handlers
│
├── services/
│   ├── base.py                      # Base service class
│   ├── seller.py                    # Seller business logic
│   ├── delivery_partner.py          # Partner business logic
│   ├── shipment.py                  # Shipment business logic
│   ├── shipment_event.py            # Shipment event tracking
│   ├── notification.py              # Email + SMS notifications
│   ├── user.py                      # Shared user logic
│   └── utils.py                     # Service utilities
│
├── database/
│   ├── session.py                   # Async engine + session factory
│   ├── redis.py                     # Redis client (token blacklist)
│   └── models.py                    # SQLModel table definitions
│
├── worker/
│   └── tasks.py                     # Celery tasks (email, SMS, logging)
│
├── templates/                       # Jinja2 templates (email + web pages)
│   ├── mail_placed.html
│   ├── mail_out_for_delivery.html
│   ├── mail_delivered.html
│   ├── mail_cancelled.html
│   ├── mail_email_verify.html
│   ├── mail_password_reset.html
│   ├── track.html                   # Public shipment tracking page
│   ├── review.html                  # Shipment review form
│   └── password/                    # Password reset pages
│       ├── reset.html
│       ├── reset_success.html
│       └── reset_failed.html
│
└── tests/                           # Pytest suite (50 tests)
    ├── conftest.py                  # Shared fixtures
    ├── test_main.py
    ├── test_seller_router.py
    ├── test_seller_service.py
    ├── test_partner_router.py
    ├── test_shipment_router.py
    ├── test_shipment_service.py
    └── test_security_utils.py
```

## Getting Started

### Option A: Docker

```bash
cp .env.example .env
# Edit .env with your credentials
docker compose up --build
```

This starts five services:
- **API** on `http://localhost:8000`
- **Celery Worker** (background tasks: email, SMS, logging)
- **Flower** (Celery task monitor) on `http://localhost:5555`
- **PostgreSQL** on port `5433`
- **Redis** on port `6380`

### Option B: Local Development

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# 4. Start PostgreSQL and Redis
# (ensure both are running locally, or use Docker for just the services)

# 5. Run database migrations
alembic upgrade head

# 6. Start the Celery worker (separate terminal)
celery -A app.worker.tasks worker --loglevel=info

# 7. Start the dev server
fastapi dev app/main.py
```

To generate a strong JWT secret:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Environment Variables

Copy `.env.example` to `.env` and fill in your values:

| Variable              | Description                              | Example                    |
|-----------------------|------------------------------------------|----------------------------|
| `POSTGRES_SERVER`     | PostgreSQL host                          | `localhost`                |
| `POSTGRES_PORT`       | PostgreSQL port                          | `5433`                     |
| `POSTGRES_USER`       | PostgreSQL username                      | `postgres`                 |
| `POSTGRES_PASSWORD`   | PostgreSQL password                      | `your-db-password`         |
| `POSTGRES_DB`         | Database name                            | `fastship`                 |
| `REDIS_HOST`          | Redis host                               | `localhost`                |
| `REDIS_PORT`          | Redis port                               | `6379`                     |
| `JWT_SECRET_KEY`      | Secret key for signing JWT tokens        | (use a long random string) |
| `JWT_ALGORITHM`       | JWT signing algorithm                    | `HS256`                    |
| `MAIL_USERNAME`       | SMTP email address (Gmail app password)  | `you@gmail.com`            |
| `MAIL_PASSWORD`       | SMTP password / app password             | `your-app-password`        |
| `MAIL_FROM`           | Sender email address                     | `you@gmail.com`            |
| `MAIL_FROM_NAME`      | Sender display name                      | `FastShip`                 |
| `MAIL_SERVER`         | SMTP server                              | `smtp.gmail.com`           |
| `MAIL_PORT`           | SMTP port                                | `587`                      |
| `TWILIO_SID`          | Twilio Account SID                       | `ACxxxxxxxxxxxxxxxx`       |
| `TWILIO_AUTH_TOKEN`   | Twilio Auth Token                        | `your-twilio-auth-token`   |
| `TWILIO_PHONE_NUMBER` | Twilio sender phone number               | `+15551234567`             |

## API Endpoints

### Seller (Authentication)

| Method | Path                          | Auth | Description                   |
|--------|-------------------------------|------|-------------------------------|
| POST   | `/seller/signup`              | No   | Register a new seller         |
| POST   | `/seller/token`               | No   | Login and receive a JWT token |
| GET    | `/seller/verify`              | No   | Verify seller email           |
| GET    | `/seller/forgot-password`     | No   | Send password reset email     |
| GET    | `/seller/reset-password-form` | No   | Render password reset form    |
| POST   | `/seller/reset-password`      | No   | Submit new password           |
| GET    | `/seller/logout`              | Yes  | Logout (blacklists the JWT)   |

### Delivery Partner

| Method | Path              | Auth | Description                     |
|--------|-------------------|------|---------------------------------|
| POST   | `/partner/signup` | No   | Register a new delivery partner |
| POST   | `/partner/token`  | No   | Login and receive a JWT token   |
| GET    | `/partner/verify` | No   | Verify partner email            |
| POST   | `/partner/`       | Yes  | Update delivery partner profile |
| GET    | `/partner/logout` | Yes  | Logout (blacklists the JWT)     |

### Shipments

| Method | Path                | Auth    | Description                    |
|--------|---------------------|---------|--------------------------------|
| POST   | `/shipments/`       | Seller  | Create a new shipment          |
| GET    | `/shipments/{id}`   | Seller  | Get shipment details by ID     |
| PATCH  | `/shipments/{id}`   | Partner | Update shipment status/location|
| DELETE | `/shipments/{id}`   | Seller  | Cancel a shipment              |
| GET    | `/shipments/track`  | No      | Public tracking page (HTML)    |
| GET    | `/shipments/tagged` | No      | Get shipments by tag           |
| GET    | `/shipments/tag`    | No      | Add a tag to a shipment        |
| DELETE | `/shipments/tag`    | No      | Remove a tag from a shipment   |
| GET    | `/shipments/review` | No      | Render review form             |
| POST   | `/shipments/review` | No      | Submit a shipment review       |

### Other

| Method | Path      | Description                  |
|--------|-----------|------------------------------|
| GET    | `/`       | Health check                 |
| GET    | `/scalar` | Scalar interactive API docs  |
| GET    | `/docs`   | Swagger UI (FastAPI default) |

## Running Tests

```bash
python -m pytest app/tests/ -v
```

50 tests covering routers, services, and security utilities. Tests are mock-based and do not require external services (no DB, Redis, or SMTP needed).

## Roadmap

- Add rate limiting
- Add structured logging
- Use slim Docker base image to reduce image size
- Add CI/CD pipeline with automated test runs
