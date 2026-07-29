import pytest
from fastapi.testclient import TestClient
from api.main import app

def test_websocket_stats(test_client):
    response = test_client.get("/ws/stats")
    assert response.status_code == 200
    data = response.json()
    assert "active_connections" in data
    assert "active_clients" in data
    assert "timestamp" in data

def test_websocket_chat_connect(test_client):
    # Test WebSocket connection
    with test_client.websocket_connect("/ws/chat/test-client-123") as websocket:
        # Send a message
        websocket.send_json({"type": "message", "content": "Hello", "agent_id": "general"})

        # Receive echo
        data = websocket.receive_json()
        assert data["type"] == "message"
        assert data["content"] == "Hello"
        assert data["client_id"] == "test-client-123"
        assert data["status"] == "received"

        # Receive AI response
        data2 = websocket.receive_json()
        assert data2["type"] == "ai_response"
        assert data2["status"] == "completed"

def test_websocket_agent_connect(test_client):
    with test_client.websocket_connect("/ws/agent/wolf-alpha/test-client-456") as websocket:
        websocket.send_json({"action": "ping", "data": "test"})

        data = websocket.receive_json()
        assert data["type"] == "agent_message"
        assert data["agent_id"] == "wolf-alpha"
        assert data["client_id"] == "test-client-456"

def test_websocket_multiple_clients(test_client):
    with test_client.websocket_connect("/ws/chat/client-1") as ws1:
        with test_client.websocket_connect("/ws/chat/client-2") as ws2:
            ws1.send_json({"type": "message", "content": "From client 1"})
            ws2.send_json({"type": "message", "content": "From client 2"})

            data1 = ws1.receive_json()
            assert data1["client_id"] == "client-1"

            data2 = ws2.receive_json()
            assert data2["client_id"] == "client-2"
