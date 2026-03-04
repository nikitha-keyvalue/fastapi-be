# FastAPI Backend

FastAPI backend service with SQLAlchemy 2.0 ORM, PostgreSQL, and Alembic migrations.

## Tech Stack

- FastAPI
- SQLAlchemy 2.0 (`Mapped[]`, `mapped_column`, `DeclarativeBase`)
- PostgreSQL (`psycopg2-binary`)
- Alembic (schema migrations + seed migration)
- Pydantic Settings (`.env` based config)

## Project Structure

```text
fastapi-be/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── routes/
│   │   └── health.py
│   ├── controllers/
│   ├── services/
│   ├── models/
│   └── schemas/
|
├── .env
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Environment Configuration

The project reads settings from `.env` via `app/core/config.py`.

Required variables:

```env
APP_NAME
APP_VERSION
DATABASE_URL
```

### Common Commands

```bash
# create a new migration from model changes
alembic revision --autogenerate -m "describe changes"

# apply all migrations
alembic upgrade head

# rollback one revision
alembic downgrade -1

# show current revision
alembic current

# show migration history
alembic history
```

## Local Development

### 1) Start PostgreSQL (Docker)

```bash
docker compose up -d
```

### 2) Create virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3) Run migrations

```bash
alembic upgrade head
```

### 4) Start Server

```bash
uvicorn app.main:app --reload
```

