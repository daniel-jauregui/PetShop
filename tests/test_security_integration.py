import pytest

def test_products_endpoints_require_authentication(client):
    """Verifies that all product endpoints return 401 if token is missing."""
    
    # 1. GET /products/
    response = client.get("/api/v1/products/")
    assert response.status_code == 401
    
    # 2. POST /products/
    response = client.post("/api/v1/products/", json={"name": "X", "description": "X", "price": 10.0, "stock": 5, "category": "toys", "pet_type": "dog"})
    assert response.status_code == 401
    
    # 3. GET /products/{id}
    response = client.get("/api/v1/products/1")
    assert response.status_code == 401
    
    # 4. PUT /products/{id}
    response = client.put("/api/v1/products/1", json={"name": "X", "description": "X", "price": 10.0, "stock": 5, "category": "toys", "pet_type": "dog"})
    assert response.status_code == 401
    
    # 5. DELETE /products/{id}
    response = client.delete("/api/v1/products/1")
    assert response.status_code == 401

