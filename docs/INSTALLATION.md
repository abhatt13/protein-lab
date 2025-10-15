# Installation Guide

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL 15+ (if running locally)
- Redis 7+ (if running locally)

## Quick Start with Docker

1. **Clone the repository**
```bash
git clone <repository-url>
cd protein-lab
```

2. **Set up environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your configuration:
- `OPENAI_API_KEY`: Your OpenAI API key
- `JWT_SECRET_KEY`: Generate a secure secret key
- Other settings as needed

3. **Start services with Docker Compose**
```bash
docker-compose up -d
```

4. **Initialize the database**
```bash
docker-compose exec api python scripts/init_db.py
docker-compose exec api python scripts/seed_data.py
```

5. **Access the application**
- Streamlit UI: http://localhost:8501
- FastAPI: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Local Development Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up PostgreSQL

```bash
createdb proteinlab
```

### 4. Set Up Redis

```bash
redis-server
```

### 5. Run Database Migrations

```bash
alembic upgrade head
python scripts/init_db.py
python scripts/seed_data.py
```

### 6. Start the API Server

```bash
uvicorn app.api.main:app --reload --port 8000
```

### 7. Start Streamlit

```bash
streamlit run app/main.py
```

## Default Credentials

After running `init_db.py`, you can log in with:

- **Admin**: `admin` / `admin123`
- **Researcher**: `researcher` / `researcher123`
- **Viewer**: `viewer` / `viewer123`

## Troubleshooting

### Port Already in Use

If ports 8000 or 8501 are in use:

```bash
docker-compose down
lsof -ti:8000 | xargs kill -9
lsof -ti:8501 | xargs kill -9
```

### Database Connection Issues

Check PostgreSQL is running:
```bash
docker-compose ps
```

Reset database:
```bash
docker-compose down -v
docker-compose up -d postgres
```

### Redis Connection Issues

Check Redis is running:
```bash
docker-compose exec redis redis-cli ping
```
