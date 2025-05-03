import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.main import app

client = TestClient(app)

@pytest.fixture
def valid_user():
    return {
        "email": "pytestUser@example.com",
        "password": "pytestPassword123",
        "name": "pythonTester",
        "country": "Bolivia",
        "username": "testUser2025"
    }

def test_register_user_success(valid_user):
    mock_user = MagicMock()
    mock_user.id = "mocked_user_id"

    with patch("src.supabase.register.supabase") as mock_supabase:
        mock_supabase.auth.sign_up.return_value.user = mock_user

        response = client.post("api/auth/register", json=valid_user)
        assert response.status_code == 200
        assert "user_id" in response.json()

def test_register_fail_auth(valid_user):
    with patch("src.supabase.register.supabase") as mock_supabase:
        mock_supabase.auth.sign_up.return_value.user = None

        response = client.post("api/auth/register", json=valid_user)
        assert response.status_code == 400
        assert "No se pudo crear el usuario" in response.text

def test_register_invalid_user():
    payload = {
        "email": "invalid-email",
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 422
    assert "detail" in response.json()