import pytest
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Test environment — no real services needed
os.environ["ENVIRONMENT"] = "testing"
os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"
os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL", "postgresql://postgres:test@localhost:5432/rafeeq_test")
# REDIS_URL intentionally NOT set — app must work without Redis
os.environ.pop("REDIS_URL", None)
os.environ["RATE_LIMIT_ENABLED"] = "false"


@pytest.fixture(scope="session")
def test_client():
    from fastapi.testclient import TestClient
    from api.main import app
    return TestClient(app)


@pytest.fixture
def auth_headers(test_client):
    """Get auth headers by logging in. Uses email (not username) per LoginRequest schema."""
    response = test_client.post("/auth/login", json={
        "email": "admin@rafeeq.ai",
        "password": "admin123"
    })
    if response.status_code == 200:
        token = response.json().get("token") or response.json().get("access_token")
        if token:
            return {"Authorization": f"Bearer {token}"}
    return {}
