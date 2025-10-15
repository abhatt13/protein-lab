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

## Setup

```bash
# Clone repository
git clone <repository-url>
cd protein-lab

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start the application
docker-compose up
```

## Development

```bash
# Run tests
pytest

# Run with hot reload
streamlit run app/main.py

# Format code
black .
isort .

# Type checking
mypy .
```

## License

MIT
