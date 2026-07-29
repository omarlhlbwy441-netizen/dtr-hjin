import pytest

def test_video_templates(test_client):
    response = test_client.get("/api/videos/templates")
    assert response.status_code == 200
    data = response.json()
    assert "templates" in data
    assert "count" in data
    assert "ffmpeg_available" in data
    assert data["count"] >= 4

def test_video_generate_explainer(test_client):
    response = test_client.post("/api/videos/generate", json={
        "template_type": "explainer",
        "title": "Test Explainer"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "video_id" in data
    assert "files" in data
    assert data["type"] == "explainer"

def test_video_generate_with_script(test_client):
    response = test_client.post("/api/videos/generate", json={
        "template_type": "tutorial",
        "title": "Test Tutorial",
        "script": "هذا نص تجريبي للفيديو التعليمي"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "script.txt" in data["files"] or any("script" in f for f in data["files"])

def test_video_generate_invalid_type(test_client):
    response = test_client.post("/api/videos/generate", json={
        "template_type": "nonexistent",
        "title": "Test Invalid"
    })
    assert response.status_code == 400

def test_video_list(test_client):
    response = test_client.get("/api/videos/list")
    assert response.status_code == 200
    data = response.json()
    assert "videos" in data
    assert "count" in data
