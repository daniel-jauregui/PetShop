# PetShop API

A FastAPI-based REST API for managing pets in a pet shop application.

## Project Structure

```
PetShop/
├── app/                    # Main application code
│   ├── api/                # API endpoints
│   │   └── v1/pets.py      # Pet endpoints (CRUD operations)
│   ├── core/
│   │   └── config.py       # Configuration and settings
│   ├── db/
│   │   └── session.py      # Database session setup
│   ├── models/
│   │   └── pet.py          # Pet database model (SQLAlchemy)
│   ├── schemas/
│   │   └── pet.py          # Pydantic request/response schemas
│   ├── services/
│   │   └── pet_service.py  # Business logic layer
│   └── main.py             # FastAPI app entry point
├── tests/                  # Test suite (pytest)
│   ├── conftest.py         # Test fixtures and configuration
│   └── test_pets.py        # Pet endpoint tests
├── static/                 # Static files (HTML, CSS, JS)
│   └── favicon.ico         # Website favicon
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment config
├── start.sh                # Application startup script
└── petshop.db              # SQLite database file
```

## Architecture

The project follows a layered architecture pattern:

- **Models** (`app/models/`) - Database entities using SQLAlchemy ORM
- **Schemas** (`app/schemas/`) - Request/response validation using Pydantic
- **Services** (`app/services/`) - Business logic layer
- **API** (`app/api/`) - HTTP endpoints exposing the API

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Testing**: pytest

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment (copy `.env.example` to `.env` if needed)

3. Run the application:
```bash
python -m uvicorn app.main:app --reload
```

Or use the startup script:
```bash
./start.sh
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/pets/` | List all pets |
| GET | `/api/v1/pets/{id}` | Get a pet by ID |
| POST | `/api/v1/pets/` | Create a new pet |
| PUT | `/api/v1/pets/{id}` | Update a pet |
| DELETE | `/api/v1/pets/{id}` | Delete a pet |
| GET | `/` | Health check |

## Running Tests

```bash
pytest
```

## License

MIT