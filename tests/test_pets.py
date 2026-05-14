"""
Tests for /api/v1/pets endpoints.

Coverage:
- GET  /pets/           list (empty and populated)
- GET  /pets/{id}       found and not found
- POST /pets/           success and validation errors
- PUT  /pets/{id}       success and not found
- DELETE /pets/{id}     success and not found
"""

import pytest


# ---------------------------------------------------------------------------
# GET /api/v1/pets/
# ---------------------------------------------------------------------------

class TestListPets:
    def test_empty_list(self, client):
        response = client.get("/api/v1/pets/")
        assert response.status_code == 200
        assert response.json() == []

    def test_returns_all_pets(self, client):
        client.post("/api/v1/pets/", json={"name": "Rex", "type": "dog", "age": 2})
        client.post("/api/v1/pets/", json={"name": "Luna", "type": "cat", "age": 4})

        response = client.get("/api/v1/pets/")
        assert response.status_code == 200
        names = [p["name"] for p in response.json()]
        assert "Rex" in names
        assert "Luna" in names


# ---------------------------------------------------------------------------
# GET /api/v1/pets/{id}
# ---------------------------------------------------------------------------

class TestGetPet:
    def test_get_existing_pet(self, client, sample_pet):
        pet_id = sample_pet["id"]
        response = client.get(f"/api/v1/pets/{pet_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == pet_id
        assert data["name"] == "Buddy"
        assert data["type"] == "dog"
        assert data["age"] == 3

    def test_get_nonexistent_pet_returns_404(self, client):
        response = client.get("/api/v1/pets/99999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


# ---------------------------------------------------------------------------
# POST /api/v1/pets/
# ---------------------------------------------------------------------------

class TestCreatePet:
    def test_create_pet_success(self, client):
        payload = {"name": "Milo", "type": "rabbit", "age": 1}
        response = client.post("/api/v1/pets/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Milo"
        assert data["type"] == "rabbit"
        assert data["age"] == 1
        assert "id" in data

    def test_create_pet_persisted(self, client):
        response = client.post("/api/v1/pets/", json={"name": "Cleo", "type": "cat", "age": 5})
        pet_id = response.json()["id"]
        fetched = client.get(f"/api/v1/pets/{pet_id}")
        assert fetched.status_code == 200
        assert fetched.json()["name"] == "Cleo"

    @pytest.mark.parametrize("payload, missing_field", [
        ({"type": "dog", "age": 2}, "name"),
        ({"name": "X", "age": 2}, "type"),
        ({"name": "X", "type": "dog"}, "age"),
    ])
    def test_create_pet_missing_required_field(self, client, payload, missing_field):
        response = client.post("/api/v1/pets/", json=payload)
        assert response.status_code == 422

    def test_create_pet_negative_age_rejected(self, client):
        response = client.post("/api/v1/pets/", json={"name": "Bad", "type": "dog", "age": -1})
        assert response.status_code == 422

    def test_create_pet_empty_name_rejected(self, client):
        response = client.post("/api/v1/pets/", json={"name": "", "type": "dog", "age": 2})
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# PUT /api/v1/pets/{id}
# ---------------------------------------------------------------------------

class TestUpdatePet:
    def test_update_existing_pet(self, client, sample_pet):
        pet_id = sample_pet["id"]
        updated = {"name": "Buddy Updated", "type": "dog", "age": 4}
        response = client.put(f"/api/v1/pets/{pet_id}", json=updated)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Buddy Updated"
        assert data["age"] == 4

    def test_update_nonexistent_pet_returns_404(self, client):
        response = client.put("/api/v1/pets/99999", json={"name": "Ghost", "type": "cat", "age": 1})
        assert response.status_code == 404

    def test_update_reflected_on_get(self, client, sample_pet):
        pet_id = sample_pet["id"]
        client.put(f"/api/v1/pets/{pet_id}", json={"name": "NewName", "type": "dog", "age": 5})
        fetched = client.get(f"/api/v1/pets/{pet_id}")
        assert fetched.json()["name"] == "NewName"


# ---------------------------------------------------------------------------
# DELETE /api/v1/pets/{id}
# ---------------------------------------------------------------------------

class TestDeletePet:
    def test_delete_existing_pet(self, client, sample_pet):
        pet_id = sample_pet["id"]
        response = client.delete(f"/api/v1/pets/{pet_id}")
        assert response.status_code == 204

    def test_deleted_pet_not_found_afterwards(self, client, sample_pet):
        pet_id = sample_pet["id"]
        client.delete(f"/api/v1/pets/{pet_id}")
        response = client.get(f"/api/v1/pets/{pet_id}")
        assert response.status_code == 404

    def test_delete_nonexistent_pet_returns_404(self, client):
        response = client.delete("/api/v1/pets/99999")
        assert response.status_code == 404

    def test_deleted_pet_removed_from_list(self, client, sample_pet):
        pet_id = sample_pet["id"]
        client.delete(f"/api/v1/pets/{pet_id}")
        ids = [p["id"] for p in client.get("/api/v1/pets/").json()]
        assert pet_id not in ids


# ---------------------------------------------------------------------------
# GET /api/v1/pets/ with filters
# ---------------------------------------------------------------------------

class TestFilterPets:
    def test_filter_by_name(self, client):
        client.post("/api/v1/pets/", json={"name": "Buddy", "type": "dog", "age": 3})
        client.post("/api/v1/pets/", json={"name": "Max", "type": "dog", "age": 5})
        client.post("/api/v1/pets/", json={"name": "Luna", "type": "cat", "age": 2})

        response = client.get("/api/v1/pets/?name=Buddy")
        assert response.status_code == 200
        names = [p["name"] for p in response.json()]
        assert "Buddy" in names
        assert "Max" not in names
        assert "Luna" not in names

    def test_filter_by_type(self, client):
        client.post("/api/v1/pets/", json={"name": "Buddy", "type": "dog", "age": 3})
        client.post("/api/v1/pets/", json={"name": "Luna", "type": "cat", "age": 2})

        response = client.get("/api/v1/pets/?type=cat")
        assert response.status_code == 200
        types = [p["type"] for p in response.json()]
        assert "cat" in types
        assert "dog" not in types

    def test_filter_by_age(self, client):
        client.post("/api/v1/pets/", json={"name": "Buddy", "type": "dog", "age": 3})
        client.post("/api/v1/pets/", json={"name": "Luna", "type": "cat", "age": 3})
        client.post("/api/v1/pets/", json={"name": "Max", "type": "dog", "age": 5})

        response = client.get("/api/v1/pets/?age=3")
        assert response.status_code == 200
        ages = [p["age"] for p in response.json()]
        assert all(a == 3 for a in ages)

    def test_filter_by_name_partial_match(self, client):
        client.post("/api/v1/pets/", json={"name": "Buddy", "type": "dog", "age": 3})
        client.post("/api/v1/pets/", json={"name": "Buddy2", "type": "dog", "age": 2})

        response = client.get("/api/v1/pets/?name=Buddy")
        assert response.status_code == 200
        names = [p["name"] for p in response.json()]
        assert "Buddy" in names
        assert "Buddy2" in names

    def test_filter_combined(self, client):
        client.post("/api/v1/pets/", json={"name": "Buddy", "type": "dog", "age": 3})
        client.post("/api/v1/pets/", json={"name": "Max", "type": "dog", "age": 5})

        response = client.get("/api/v1/pets/?type=dog&age=3")
        assert response.status_code == 200
        pets = response.json()
        assert len(pets) == 1
        assert pets[0]["name"] == "Buddy"
