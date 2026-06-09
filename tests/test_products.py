"""
Tests for /api/v1/products endpoints.

Coverage:
- GET  /products/           list (empty and populated)
- GET  /products/{id}       found and not found
- POST /products/           success and validation errors
- PUT  /products/{id}       success and not found
- DELETE /products/{id}     success and not found
"""

import pytest


# ---------------------------------------------------------------------------
# GET /api/v1/products/
# ---------------------------------------------------------------------------

class TestListProducts:
    def test_empty_list(self, client, auth_headers):
        response = client.get("/api/v1/products/", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []

    def test_returns_all_products(self, client, auth_headers):
        client.post(
            "/api/v1/products/", 
            json={
                "name": "Dog Kibble",
                "description": "Tasty food for dogs",
                "price": 45.50,
                "stock": 10,
                "category": "food",
                "pet_type": "dog"
            }, 
            headers=auth_headers
        )
        client.post(
            "/api/v1/products/", 
            json={
                "name": "Cat Wand Toy",
                "description": "Feather wand toy for cats",
                "price": 5.99,
                "stock": 30,
                "category": "toys",
                "pet_type": "cat"
            }, 
            headers=auth_headers
        )

        response = client.get("/api/v1/products/", headers=auth_headers)
        assert response.status_code == 200
        names = [p["name"] for p in response.json()]
        assert "Dog Kibble" in names
        assert "Cat Wand Toy" in names


# ---------------------------------------------------------------------------
# GET /api/v1/products/{id}
# ---------------------------------------------------------------------------

class TestGetProduct:
    def test_get_existing_product(self, client, sample_product, auth_headers):
        product_id = sample_product["id"]
        response = client.get(f"/api/v1/products/{product_id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == product_id
        assert data["name"] == "Dog Toy Bone"
        assert data["category"] == "toys"
        assert data["price"] == 12.99
        assert data["stock"] == 25

    def test_get_nonexistent_product_returns_404(self, client, auth_headers):
        response = client.get("/api/v1/products/99999", headers=auth_headers)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


# ---------------------------------------------------------------------------
# POST /api/v1/products/
# ---------------------------------------------------------------------------

class TestCreateProduct:
    def test_create_product_success(self, client, auth_headers):
        payload = {
            "name": "Bird Seed Mix",
            "description": "Premium blend seeds",
            "price": 8.50,
            "stock": 15,
            "category": "food",
            "pet_type": "bird"
        }
        response = client.post("/api/v1/products/", json=payload, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Bird Seed Mix"
        assert data["category"] == "food"
        assert data["price"] == 8.50
        assert "id" in data

    def test_create_product_persisted(self, client, auth_headers):
        response = client.post(
            "/api/v1/products/", 
            json={
                "name": "Cat Collar",
                "description": "Safety collar with bell",
                "price": 4.99,
                "stock": 20,
                "category": "accessories",
                "pet_type": "cat"
            }, 
            headers=auth_headers
        )
        product_id = response.json()["id"]
        fetched = client.get(f"/api/v1/products/{product_id}", headers=auth_headers)
        assert fetched.status_code == 200
        assert fetched.json()["name"] == "Cat Collar"

    @pytest.mark.parametrize("payload, missing_field", [
        ({"description": "X", "price": 10.0, "stock": 5, "category": "toys", "pet_type": "dog"}, "name"),
        ({"name": "X", "description": "X", "stock": 5, "category": "toys", "pet_type": "dog"}, "price"),
        ({"name": "X", "description": "X", "price": 10.0, "category": "toys", "pet_type": "dog"}, "stock"),
        ({"name": "X", "description": "X", "price": 10.0, "stock": 5, "pet_type": "dog"}, "category"),
        ({"name": "X", "description": "X", "price": 10.0, "stock": 5, "category": "toys"}, "pet_type"),
    ])
    def test_create_product_missing_required_fields(self, client, auth_headers, payload, missing_field):
        response = client.post("/api/v1/products/", json=payload, headers=auth_headers)
        assert response.status_code == 422

    def test_create_product_negative_price_rejected(self, client, auth_headers):
        payload = {
            "name": "Invalid Price",
            "price": -1.0,
            "stock": 5,
            "category": "toys",
            "pet_type": "dog"
        }
        response = client.post("/api/v1/products/", json=payload, headers=auth_headers)
        assert response.status_code == 422

    def test_create_product_negative_stock_rejected(self, client, auth_headers):
        payload = {
            "name": "Invalid Stock",
            "price": 10.0,
            "stock": -5,
            "category": "toys",
            "pet_type": "dog"
        }
        response = client.post("/api/v1/products/", json=payload, headers=auth_headers)
        assert response.status_code == 422

    def test_create_product_invalid_category_rejected(self, client, auth_headers):
        payload = {
            "name": "Invalid Category",
            "price": 10.0,
            "stock": 5,
            "category": "invalid_category",  # must be food, toys, accessories, medicine
            "pet_type": "dog"
        }
        response = client.post("/api/v1/products/", json=payload, headers=auth_headers)
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# PUT /api/v1/products/{id}
# ---------------------------------------------------------------------------

class TestUpdateProduct:
    def test_update_existing_product(self, client, sample_product, auth_headers):
        product_id = sample_product["id"]
        updated = {
            "name": "Dog Toy Bone Modified",
            "description": "Even more durable rubber bone for dogs",
            "price": 14.99,
            "stock": 10,
            "category": "toys",
            "pet_type": "dog"
        }
        response = client.put(f"/api/v1/products/{product_id}", json=updated, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Dog Toy Bone Modified"
        assert data["price"] == 14.99
        assert data["stock"] == 10

    def test_update_nonexistent_product_returns_404(self, client, auth_headers):
        payload = {
            "name": "Ghost Product",
            "price": 9.99,
            "stock": 1,
            "category": "toys",
            "pet_type": "cat"
        }
        response = client.put("/api/v1/products/99999", json=payload, headers=auth_headers)
        assert response.status_code == 404

    def test_update_reflected_on_get(self, client, sample_product, auth_headers):
        product_id = sample_product["id"]
        payload = {
            "name": "New Name",
            "description": sample_product["description"],
            "price": sample_product["price"],
            "stock": 100,
            "category": sample_product["category"],
            "pet_type": sample_product["pet_type"]
        }
        client.put(f"/api/v1/products/{product_id}", json=payload, headers=auth_headers)
        fetched = client.get(f"/api/v1/products/{product_id}", headers=auth_headers)
        assert fetched.json()["name"] == "New Name"
        assert fetched.json()["stock"] == 100


# ---------------------------------------------------------------------------
# DELETE /api/v1/products/{id}
# ---------------------------------------------------------------------------

class TestDeleteProduct:
    def test_delete_existing_product(self, client, sample_product, auth_headers):
        product_id = sample_product["id"]
        response = client.delete(f"/api/v1/products/{product_id}", headers=auth_headers)
        assert response.status_code == 204

    def test_deleted_product_not_found_afterwards(self, client, sample_product, auth_headers):
        product_id = sample_product["id"]
        client.delete(f"/api/v1/products/{product_id}", headers=auth_headers)
        response = client.get(f"/api/v1/products/{product_id}", headers=auth_headers)
        assert response.status_code == 404

    def test_delete_nonexistent_product_returns_404(self, client, auth_headers):
        response = client.delete("/api/v1/products/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_deleted_product_removed_from_list(self, client, sample_product, auth_headers):
        product_id = sample_product["id"]
        client.delete(f"/api/v1/products/{product_id}", headers=auth_headers)
        ids = [p["id"] for p in client.get("/api/v1/products/", headers=auth_headers).json()]
        assert product_id not in ids


# ---------------------------------------------------------------------------
# GET /api/v1/products/ with filters
# ---------------------------------------------------------------------------

class TestFilterProducts:
    def test_filter_by_name(self, client, auth_headers):
        client.post(
            "/api/v1/products/", 
            json={"name": "Dog Food Super", "price": 20.0, "stock": 10, "category": "food", "pet_type": "dog"}, 
            headers=auth_headers
        )
        client.post(
            "/api/v1/products/", 
            json={"name": "Cat Nip Toy", "price": 5.0, "stock": 15, "category": "toys", "pet_type": "cat"}, 
            headers=auth_headers
        )

        response = client.get("/api/v1/products/?name=Super", headers=auth_headers)
        assert response.status_code == 200
        names = [p["name"] for p in response.json()]
        assert "Dog Food Super" in names
        assert "Cat Nip Toy" not in names

    def test_filter_by_category(self, client, auth_headers):
        client.post(
            "/api/v1/products/", 
            json={"name": "Dog Bone", "price": 10.0, "stock": 5, "category": "toys", "pet_type": "dog"}, 
            headers=auth_headers
        )
        client.post(
            "/api/v1/products/", 
            json={"name": "Dog Feed", "price": 30.0, "stock": 5, "category": "food", "pet_type": "dog"}, 
            headers=auth_headers
        )

        response = client.get("/api/v1/products/?category=food", headers=auth_headers)
        assert response.status_code == 200
        categories = [p["category"] for p in response.json()]
        assert "food" in categories
        assert "toys" not in categories

    def test_filter_by_pet_type(self, client, auth_headers):
        client.post(
            "/api/v1/products/", 
            json={"name": "Dog Chew", "price": 10.0, "stock": 5, "category": "toys", "pet_type": "dog"}, 
            headers=auth_headers
        )
        client.post(
            "/api/v1/products/", 
            json={"name": "Cat Chew", "price": 10.0, "stock": 5, "category": "toys", "pet_type": "cat"}, 
            headers=auth_headers
        )

        response = client.get("/api/v1/products/?pet_type=cat", headers=auth_headers)
        assert response.status_code == 200
        pet_types = [p["pet_type"] for p in response.json()]
        assert "cat" in pet_types
        assert "dog" not in pet_types
