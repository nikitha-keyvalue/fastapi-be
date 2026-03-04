# FastAPI Backend

Basic FastAPI project scaffold with a health checkpoint.

## Project Structure

```text
fastapi-be/
|
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

## Run Locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run with Docker

```bash
docker compose up --build
```

## Health Check

- Endpoint: `GET /api/health`
- Expected response:

```json
{"status":"ok"}
```
