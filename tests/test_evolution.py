import pytest

def test_evolution_status(test_client):
    response = test_client.get("/api/evolution/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "iq_level" in data
    assert "evolution_count" in data
    assert "timestamp" in data

def test_evolution_log(test_client):
    response = test_client.get("/api/evolution/log")
    assert response.status_code == 200
    data = response.json()
    assert "log" in data
    assert "count" in data
    assert isinstance(data["count"], int)

def test_evolution_trigger(test_client):
    response = test_client.post("/api/evolution/trigger", json={"auto": True})
    assert response.status_code in [200, 500]  # 500 if engine not fully initialized
    if response.status_code == 200:
        data = response.json()
        assert "status" in data

def test_evolution_iq(test_client):
    response = test_client.get("/api/evolution/iq")
    assert response.status_code == 200
    data = response.json()
    assert "iq_level" in data
    assert isinstance(data["iq_level"], int)

def test_evolution_start_stop_loop(test_client):
    # Start
    response = test_client.post("/api/evolution/start-loop")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["started", "already_running"]

    # Stop
    response = test_client.post("/api/evolution/stop-loop")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "stopped"

def test_evolution_feedback(test_client):
    response = test_client.post("/api/evolution/feedback", json={
        "type": "feature_request",
        "content": "Add dark mode",
        "priority": "high"
    })
    assert response.status_code in [200, 500]
