import pytest

def test_website_templates(test_client):
    response = test_client.get("/api/websites/templates")
    assert response.status_code == 200
    data = response.json()
    assert "templates" in data
    assert "count" in data
    assert data["count"] >= 5

def test_website_generate_portfolio(test_client):
    response = test_client.post("/api/websites/generate", json={
        "template_type": "portfolio",
        "title": "My Portfolio"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "site_id" in data
    assert "preview_url" in data
    assert data["type"] == "portfolio"

def test_website_generate_landing(test_client):
    response = test_client.post("/api/websites/generate", json={
        "template_type": "landing",
        "title": "Product Landing"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["type"] == "landing"

def test_website_generate_invalid_type(test_client):
    response = test_client.post("/api/websites/generate", json={
        "template_type": "nonexistent",
        "title": "Test Invalid"
    })
    assert response.status_code == 400

def test_website_list(test_client):
    response = test_client.get("/api/websites/list")
    assert response.status_code == 200
    data = response.json()
    assert "websites" in data
    assert "count" in data
