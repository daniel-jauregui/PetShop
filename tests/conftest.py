import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite://"  # pure in-memory, discarded after each test session


@pytest.fixture(scope="session")
def engine_fixture():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session(engine_fixture):
    """Each test gets a fresh, rolled-back transaction."""
    connection = engine_fixture.connect()
    transaction = connection.begin()
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = TestingSessionLocal()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db_session):
    """TestClient with the DB dependency overridden to use the test session."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def test_user(client):
    """Create a test user and return its data."""
    user_data = {"username": "testuser", "password": "testpassword123"}
    client.post("/api/v1/auth/register", json=user_data)
    return user_data


@pytest.fixture()
def auth_headers(client, test_user):
    """Return headers with a valid JWT token."""
    login_data = {"username": test_user["username"], "password": test_user["password"]}
    response = client.post("/api/v1/auth/token", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def sample_product(client, auth_headers) -> dict:
    """Create one product and return the response JSON."""
    response = client.post(
        "/api/v1/products/", 
        json={
            "name": "Dog Toy Bone",
            "description": "Durable rubber bone for dogs",
            "price": 12.99,
            "stock": 25,
            "category": "toys",
            "pet_type": "dog"
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    return response.json()
