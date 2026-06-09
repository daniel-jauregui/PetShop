# PetShop API

A FastAPI-based REST API for managing products in a pet shop application.

## Project Structure

```
PetShop/
├── app/                        # Main application code
│   ├── api/                    # API endpoints
│   │   └── v1/products.py      # Product endpoints (CRUD operations)
│   ├── core/
│   │   └── config.py           # Configuration and settings
│   ├── db/
│   │   └── session.py          # Database session setup
│   ├── models/
│   │   └── product.py          # Product database model (SQLAlchemy)
│   ├── schemas/
│   │   └── product.py          # Pydantic request/response schemas
│   ├── services/
│   │   └── product_service.py  # Business logic layer
│   └── main.py                 # FastAPI app entry point
├── tests/                      # Test suite (pytest)
│   ├── conftest.py             # Test fixtures and configuration
│   └── test_products.py        # Product endpoint tests
├── scripts/                    # Utility scripts
│   └── seed_products.py        # Seed database with sample products
├── static/                     # Static files (HTML, CSS, JS)
│   └── favicon.ico             # Website favicon
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
├── render.yaml                 # Render deployment config
├── start.sh                    # Application startup script
└── petshop.db                  # SQLite database file
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
- **Validation**: Pydantic V2
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
## 🔒 Authentication

The API uses JSON Web Tokens (JWT) and `bcrypt` for secure user authentication.

### Security Constraints
* **Password Hashing:** Handled via `passlib` using the `bcrypt` algorithm.
* **Password Length:** Strictly validated between 8 and 72 characters at the schema level to match `bcrypt` byte boundaries and prevent silent truncation.
* **Token Lifetime:** Access tokens expire after 30 minutes.

The API exposes the following endpoints under the `/api/v1/auth` prefix:
* `POST /register`: Registers a new user, hashes the password, and stores it in the database. Returns a `400 Bad Request` if the username is taken.
* `POST /token`: Validates user credentials using standard OAuth2 form data (`application/x-www-form-urlencoded`). Returns a signed JWT access token on success, or a `401 Unauthorized` error on failure.

## Seeding the Database

To add sample products to the database, run the seed script:

```bash
python scripts/seed_products.py
```

This will clear existing products and add a realistic catalog of products across various categories (food, toys, accessories, medicine) and pet types (dogs, cats, birds, rabbits, fish, etc.).

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/products/` | List all products (supports filtering by name, category, pet_type) |
| GET | `/api/v1/products/{id}` | Get a product by ID |
| POST | `/api/v1/products/` | Create a new product |
| PUT | `/api/v1/products/{id}` | Update a product |
| DELETE | `/api/v1/products/{id}` | Delete a product |
| GET | `/` | Health check |

## Deployment

The application is deployed on Render: **https://petshop-0jtd.onrender.com**

API Documentation (Swagger UI): **https://petshop-0jtd.onrender.com/docs**

## Running Tests

```bash
pytest
```

## License

MIT