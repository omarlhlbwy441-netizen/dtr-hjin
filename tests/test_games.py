import pytest

def test_game_templates(test_client):
    response = test_client.get("/api/games/templates")
    assert response.status_code == 200
    data = response.json()
    assert "templates" in data
    assert "count" in data
    assert data["count"] >= 5

def test_game_generate_platformer(test_client):
    response = test_client.post("/api/games/generate", json={
        "game_type": "platformer",
        "title": "Test Platformer"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "game_id" in data
    assert "play_url" in data
    assert data["type"] == "platformer"

def test_game_generate_shooter(test_client):
    response = test_client.post("/api/games/generate", json={
        "game_type": "shooter",
        "title": "Test Shooter"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["type"] == "shooter"

def test_game_generate_invalid_type(test_client):
    response = test_client.post("/api/games/generate", json={
        "game_type": "nonexistent",
        "title": "Test Invalid"
    })
    assert response.status_code == 400

def test_game_list(test_client):
    response = test_client.get("/api/games/list")
    assert response.status_code == 200
    data = response.json()
    assert "games" in data
    assert "count" in data

def test_game_get_by_id(test_client):
    # First generate a game
    gen = test_client.post("/api/games/generate", json={
        "game_type": "puzzle",
        "title": "Test Puzzle"
    })
    game_id = gen.json()["game_id"]

    response = test_client.get(f"/api/games/{game_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["game_id"] == game_id

def test_game_get_not_found(test_client):
    response = test_client.get("/api/games/nonexistent-id")
    assert response.status_code == 404
