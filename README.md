# Protein Lab

A comprehensive protein database management platform with AI-powered analytics, visualization, and sequence analysis tools.

## Features

- **CRUD Operations**: Create, read, update, and delete protein records
- **Authentication**: Role-based access control (Admin, Researcher, Viewer)
- **Batch Processing**: Upload multiple proteins via CSV/Excel
- **Advanced Search**: Full-text search with filters
- **AI Chatbot**: Natural language to SQL query generation
- **Sequence Analysis**: BLAST integration, alignment, motif detection
- **3D Visualization**: Interactive protein structure viewer
- **Analytics Dashboard**: Statistics, trends, and insights
- **Data Quality**: Validation, duplicate detection, completeness checks
- **Export Options**: FASTA, GenBank, CSV, JSON formats
- **External Integration**: UniProt, PDB database connectivity
- **Audit Logging**: Track all data modifications
- **Version Control**: Historical tracking of protein records

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **AI**: OpenAI GPT-4
- **Visualization**: Plotly, py3Dmol
- **Deployment**: Docker, Docker Compose

## Quick Start

```bash
git clone <repository-url>
cd protein-lab
cp .env.example .env
docker-compose up -d
docker-compose exec api python scripts/init_db.py
```

Visit:
- Streamlit UI: http://localhost:8501
- API Docs: http://localhost:8000/docs

Default credentials: `admin` / `admin123`

## Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [API Documentation](docs/API.md)
- [User Guide](docs/USER_GUIDE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

## Project Structure

```
protein-lab/
├── app/
│   ├── api/           # FastAPI endpoints
│   ├── core/          # Config, database, security
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic
│   ├── utils/         # Utilities, validators
│   ├── ui/            # Streamlit pages
│   └── main.py        # Streamlit entry point
├── tests/             # Unit and integration tests
├── scripts/           # Database initialization
├── docs/              # Documentation
├── alembic/           # Database migrations
├── docker-compose.yml # Docker orchestration
└── requirements.txt   # Python dependencies
```

## Development

```bash
pytest                      # Run tests
black .                     # Format code
isort .                     # Sort imports
mypy .                      # Type checking
streamlit run app/main.py   # Run Streamlit
uvicorn app.api.main:app --reload  # Run API
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/name`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/name`)
5. Open Pull Request

## License

MIT
